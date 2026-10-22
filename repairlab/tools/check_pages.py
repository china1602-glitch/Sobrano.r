"""Verify the static preview under the real GitHub repository subpath."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import shutil
import tempfile
import threading

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[2]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

with tempfile.TemporaryDirectory() as temporary:
    shutil.copytree(ROOT / '_site', Path(temporary) / 'codex-workspace')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=temporary))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    origin = f'http://127.0.0.1:{server.server_port}/codex-workspace/'
    try:
        with sync_playwright() as playwright:
            options = {'headless': True}
            if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
                options['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
            browser = playwright.chromium.launch(**options)
            page = browser.new_page()
            errors, failed, api = [], [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: failed.append(response.url) if response.status >= 400 else None)
            page.on('request', lambda request: api.append(request.url) if '/api/' in request.url else None)
            for width in (360, 390, 768, 1440):
                page.set_viewport_size({'width': width, 'height': 1000})
                for route in ('', 'privacy.html'):
                    response = page.goto(origin + route)
                    assert response.status == 200
                    if not route:
                        expect(page.locator('.service')).to_have_count(4)
                        expect(page.locator('.preview-banner')).to_contain_text('Онлайн-заявки отключены')
                    assert page.locator('form').count() == 0
                    page.locator('img').evaluate_all('images=>Promise.all(images.map(i=>i.decode().catch(()=>null)))')
                    assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (width, route)
            page.goto(origin)
            expect(page.locator('.service')).to_have_count(4)
            page.locator('[data-filter="Мобильные"]').click()
            expect(page.locator('.service')).to_have_count(2)
            page.locator('[data-filter="Компьютеры"]').click()
            expect(page.locator('.service')).to_have_count(2)
            page.locator('[data-filter="Все"]').click()
            expect(page.locator('.service')).to_have_count(4)
            page.get_by_role('button', name='Подробнее: Ноутбуки', exact=True).click()
            expect(page.locator('#selected-service')).to_contain_text('Ноутбуки')
            expect(page.locator('#selected-service')).to_contain_text('не принимаются')
            page.get_by_role('link', name='Обработка данных →', exact=True).click()
            expect(page).to_have_url(origin + 'privacy.html')
            page.get_by_role('link', name='← На главную', exact=True).click()
            expect(page).to_have_url(origin)
            assert not api, api
            assert not errors, errors
            assert not failed, failed
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
print('Static preview passed: 8 page/viewport checks; filters, selection, links, images; no forms, API calls or JS errors.')

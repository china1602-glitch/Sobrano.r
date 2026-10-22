"""Build a static preview without changing the local Python application."""
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / "_site"

def build():
    sys.path.insert(0, str(ROOT))
    from app import SERVICES
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT / "static", OUTPUT)
    document = (ROOT / "static/index.html").read_text(encoding="utf-8")
    start = document.index('<form id="booking-form"')
    end = document.index("</form>", start) + len("</form>")
    document = document[:start] + '''<aside class="preview-notice" aria-labelledby="preview-title">
      <h3 id="preview-title">О демонстрации</h3>
      <p>Это учебная версия RepairLab для просмотра. Здесь работают каталог, фильтры и переходы по странице.</p>
      <p><strong>Онлайн-заявки отключены: данные не отправляются и не сохраняются.</strong> Реальные услуги не оказываются.</p>
      <p id="selected-service" tabindex="-1" aria-live="polite">Выберите устройство в каталоге, чтобы посмотреть информацию.</p>
    </aside>''' + document[end:]
    document = document.replace('<body>', '<body><div class="preview-banner">Учебный проект · Просмотр сайта · Онлайн-заявки отключены</div>', 1)
    document = document.replace('<link rel="stylesheet" href="styles.css" />', '<link rel="stylesheet" href="styles.css" /><link rel="stylesheet" href="preview.css" />', 1)
    document = document.replace("Выберите услугу и оставьте заявку онлайн.", "Каталог услуг и демонстрация учебного проекта.")
    document = document.replace("Записаться на диагностику", "Посмотреть условия")
    document = document.replace("Записаться <span>", "О проекте <span>")
    document = document.replace("Пара минут на заявку —<br />и одним вопросом меньше.", "Познакомьтесь с возможностями<br />учебного проекта.")
    document = re.sub(r"После отправки вы получите номер заявки\.\s+Мастер уточнит детали и\s+время\.", "В полной версии заявка получает номер и подтверждается оператором. Здесь доступен просмотр проекта.", document)
    document = re.sub(r"Форма сохраняет заявку в\s+базе данных, но реальный ремонт не выполняется\. Для демонстрации\s+используйте вымышленные данные\.", "В этой опубликованной версии форма отключена и заявки не сохраняются. Реальный ремонт не выполняется.", document)
    assert '<form' not in document
    assert "Форма сохраняет заявку" not in document
    (OUTPUT / "index.html").write_text(document, encoding="utf-8")
    shutil.copyfile(ROOT / "pages/app.js", OUTPUT / "app.js")
    shutil.copyfile(ROOT / "pages/preview.css", OUTPUT / "preview.css")
    (OUTPUT / "catalog.json").write_text(json.dumps(SERVICES, ensure_ascii=False), encoding="utf-8")
    privacy = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Обработка данных — RepairLab</title><link rel="stylesheet" href="styles.css"></head>
    <body><main class="privacy"><a href="./">← На главную</a><p class="eyebrow">REPAIRLAB · УЧЕБНЫЙ ПРОЕКТ</p><h1>Обработка данных</h1>
    <p>Это статическая демонстрация сайта. Формы отправки заявок нет: имя, телефон и описание проблемы через сайт не собираются и не сохраняются.</p>
    <p>Реальные услуги не оказываются. Сайт размещён на GitHub Pages; сведения о техническом журналировании доступны в <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages">документации GitHub Pages</a>.</p>
    <a class="button" href="./#services">Посмотреть услуги →</a></main></body></html>'''
    (OUTPUT / "privacy.html").write_text(privacy, encoding="utf-8")
    (OUTPUT / ".nojekyll").touch()
    assert not list(OUTPUT.rglob("*.py"))
    assert not list(OUTPUT.rglob("*.sqlite3"))
    print(f"Ready: {OUTPUT}; {len(SERVICES)} catalogue items; no forms or API.")

if __name__ == "__main__":
    build()

# GitHub Pages: сайт без локального терминала

На GitHub Pages размещается версия для просмотра: главная, каталог с четырьмя устройствами, фильтры и страница обработки данных. Форма отключена и данные заявок не отправляются. Исходный Python-сервер, форма и SQLite сохранены для локальной демонстрации на защите.

## Включить один раз

1. Откройте https://github.com/china1602-glitch/codex-workspace/settings/pages . Это репозиторий RepairLab, не Mira Beauty.
2. В Build and deployment → Source выберите **GitHub Actions**.
3. Откройте Actions → **Publish RepairLab on GitHub Pages** → **Run workflow** → main → **Run workflow**.
4. Дождитесь зелёных build и deploy. Адрес после успешной публикации: https://china1602-glitch.github.io/codex-workspace/ .

Если первый deploy завершился ошибкой из-за не включённого Pages, сначала выберите Source: GitHub Actions и повторите workflow.

## Обновления

После изменений исходников в main сайт собирается заново и публикуется автоматически. Страницы берутся из repairlab/static, каталог — из SERVICES в repairlab/app.py, поведение опубликованного каталога — из repairlab/pages/app.js. Публикуется только созданная папка _site: базы и исходники Python в неё не попадают.

Загрузка ZIP-файла в репозиторий не заменяет исходники. Локальная копия на компьютере также не обновляется автоматически от изменений GitHub.

## Как показать backend

Для демонстрации цепочки браузер → POST → Python → SQLite → результат запустите полную версию через python app.py и оператор через python operator_app.py. Публичная страница Pages не выполняет Python и не связана с локальной базой.

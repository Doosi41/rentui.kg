<!-- Этот файл собирается автоматически: python3 scripts/readme.py. Правки вручную перезапишутся. -->
<p align="center"><a href="README.md">English</a> &nbsp;|&nbsp; <b>Русский</b></p>

<a href="https://www.rentui.it.com"><img src="images/readme/ru/banner.svg" alt="Rent Ui — аренда жилья в Кыргызстане. Напрямую. Просто. Везде." width="100%"></a>

<p align="center">
  <a href="#features">Возможности&nbsp;›</a>&emsp;
  <a href="#screens">Экраны&nbsp;›</a>&emsp;
  <a href="#stack">Стек&nbsp;›</a>&emsp;
  <a href="#run">Запуск&nbsp;›</a>&emsp;
  <a href="#settings">Настройки&nbsp;›</a>&emsp;
  <a href="#structure">Структура&nbsp;›</a>
</p>

<br>

<img src="images/readme/ru/stats.svg" alt="Без комиссии. Тестов: 16. Работает на любом экране." width="100%">

<br>
<br>

<p align="center">
  <i>“Simplicity is the ultimate sophistication.”</i><br>
  <sub>— брошюра Apple II, 1977</sub>
</p>

<br>

<a name="features"></a>
<img src="images/readme/ru/titles/features.svg" alt="Возможности" width="100%">

<a href="anons/models.py"><img src="images/readme/ru/rows/listings.svg" alt="Объявления — Заголовок, описание, цена в сомах, адрес и телефон" width="100%"></a>
<a href="anons/forms.py"><img src="images/readme/ru/rows/photos.svg" alt="Фотогалерея — Первое фото — обложка, остальные идут в галерею" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/ru/rows/accounts.svg" alt="Аккаунты — Регистрация, вход, выход и возврат на ту же страницу" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/ru/rows/search.svg" alt="Поиск — По заголовку и описанию, 20 объявлений на странице" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/ru/rows/owner-only.svg" alt="Только владелец — Менять и удалять объявление может только автор или админ" width="100%"></a>
<a href="anons/models.py"><img src="images/readme/ru/rows/storage.svg" alt="Облачное хранилище — Фото лежат в DigitalOcean Spaces и удаляются вместе с объявлением" width="100%"></a>

<br>
<br>

<a name="screens"></a>
<img src="images/readme/ru/titles/screens.svg" alt="Экраны" width="100%">

<a href="https://www.rentui.it.com"><img src="images/readme/screens.webp" alt="Главная, «О нас» и регистрация на iPhone" width="100%"></a>

<br>
<br>

<a name="stack"></a>
<img src="images/readme/ru/titles/stack.svg" alt="Стек" width="100%">

<img src="images/readme/ru/stack.svg" alt="Сделано на Python, Django, PostgreSQL, SQLite, DigitalOcean и Vercel" width="100%">

<br>
<br>

<a name="run"></a>
<img src="images/readme/ru/titles/run.svg" alt="Запуск" width="100%">

<img src="images/readme/ru/run.svg" alt="Установка, запуск и тесты проекта в терминале" width="100%">

<details>
<summary>Скопировать команды</summary>
<br>

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
# вставь ключ в SECRET_KEY в .env

python manage.py migrate
python manage.py runserver

# Тесты: локально держи DATABASE_URL на SQLite
python manage.py test

# Пересобрать этот README
python3 scripts/readme.py
```

</details>

<br>

<a name="settings"></a>
<img src="images/readme/ru/titles/settings.svg" alt="Настройки" width="100%">

<img src="images/readme/ru/settings.svg" alt="Переменные окружения: SECRET_KEY, DATABASE_URL, ключи AWS, почта, DEBUG" width="100%">

<br>
<br>

<a name="structure"></a>
<img src="images/readme/ru/titles/structure.svg" alt="Структура" width="100%">

<img src="images/readme/ru/structure.svg" alt="Структура репозитория" width="100%">

<br>
<br>

<img src="images/readme/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">

<p align="center">
  <sub>Сделано командой Fidea &nbsp;·&nbsp; <a href="https://github.com/a1tvv">@a1tvv</a> &nbsp;·&nbsp; <a href="LICENSE">Лицензия MIT</a></sub>
</p>

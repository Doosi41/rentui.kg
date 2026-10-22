<p align="center"><a href="README.md">English</a> &nbsp;|&nbsp; <b>Русский</b></p>

<p align="center">
  <a href="https://www.rentui.it.com">
    <img src="images/readme/banner.webp" alt="Rent Ui — аренда жилья в Кыргызстане: напрямую, просто, везде" width="100%">
  </a>
</p>

<p align="center">
  <a href="https://www.rentui.it.com"><img src="https://img.shields.io/badge/%D0%9E%D1%82%D0%BA%D1%80%D1%8B%D1%82%D1%8C_%D1%81%D0%B0%D0%B9%D1%82-rentui.it.com-703BF7?style=for-the-badge&labelColor=141414" alt="Открыть сайт"></a>
  <img src="https://img.shields.io/badge/Python-3.12-703BF7?style=for-the-badge&logo=python&logoColor=white&labelColor=141414" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Django-5.0-703BF7?style=for-the-badge&logo=django&logoColor=white&labelColor=141414" alt="Django 5.0">
  <a href="LICENSE"><img src="https://img.shields.io/badge/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F-MIT-703BF7?style=for-the-badge&labelColor=141414" alt="Лицензия MIT"></a>
</p>

<p align="center">
  <b>Rent Ui</b> — площадка объявлений об аренде жилья в Кыргызстане.<br>
  Хозяева публикуют квартиры и дома, арендаторы находят их и звонят владельцу напрямую — без агентов и комиссий.
</p>

<p align="center">
  <img src="images/readme/highlights.png" alt="Прямой контакт · Весь Кыргызстан · Ежедневные обновления" width="100%">
</p>

## Как выглядит

<p align="center">
  <img src="images/readme/showcase.webp" alt="Главная страница Rent Ui на компьютере и на телефоне" width="100%">
</p>

<p align="center">
  <img src="images/readme/pages.webp" alt="Страницы «О нас» и регистрации" width="100%">
</p>

## Возможности

- **Аккаунты.** Регистрация, вход, выход. После входа ты возвращаешься на страницу, с которой пришёл.
- **Объявления.** Заголовок, описание, цена в сомах, адрес, телефон и фото.
- **Фотогалерея.** Первое фото становится обложкой, остальные идут в галерею. Принимаются только картинки до 5 МБ.
- **Права владельца.** Редактировать и удалять объявление может только автор или админ.
- **Поиск.** По заголовку и описанию, с пагинацией.
- **Аккуратное хранение.** Фото лежат в DigitalOcean Spaces и удаляются вместе с объявлением.
- **Мобильная вёрстка.** Адаптивные страницы, на телефонах — нижняя панель вкладок.
- **Админка.** Django-админка, где галерея фото видна прямо внутри объявления.

## Стек

<p>
  <img src="https://img.shields.io/badge/Django-703BF7?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-703BF7?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/DigitalOcean_Spaces-703BF7?style=flat-square&logo=digitalocean&logoColor=white" alt="DigitalOcean Spaces">
  <img src="https://img.shields.io/badge/WhiteNoise-703BF7?style=flat-square" alt="WhiteNoise">
  <img src="https://img.shields.io/badge/Vercel-703BF7?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">
</p>

| Слой | Технология |
|---|---|
| Бэкенд | Python 3.12, Django 5.0 |
| База данных | PostgreSQL на Neon или любая база через `DATABASE_URL` |
| Фото | DigitalOcean Spaces через django-storages и boto3 |
| Статика | WhiteNoise |
| Хостинг | Vercel |
| Фронтенд | Шаблоны Django, обычный CSS, Font Awesome |

## Быстрый старт

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
# вставь выведенный ключ в SECRET_KEY в .env

python manage.py migrate
python manage.py runserver
```

Потом открой http://127.0.0.1:8000.

## Настройки

Локально настройки берутся из `.env`, в продакшене — из переменных окружения (см. [`.env.example`](.env.example)).

| Переменная | Что это |
|---|---|
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | `True` для локальной разработки. В продакшене не задавай |
| `DATABASE_URL` | Локально `sqlite:///db.sqlite3`, в продакшене — URL PostgreSQL |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | Ключи DigitalOcean Spaces для фото. Без них сайт не запустится |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Адрес Gmail и пароль приложения для формы обратной связи |

## Тесты

```bash
python manage.py test
```

Тесты используют базу из `DATABASE_URL`, поэтому локально держи там SQLite. Загруженные файлы хранятся в памяти и не попадают в Spaces.

## Деплой

Сайт работает на Vercel ([`vercel.json`](vercel.json)). В **Project → Settings → Environment Variables** добавь все переменные из таблицы выше, кроме `DEBUG`. Новый домен нужно также добавить в `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` в [`config/settings.py`](config/settings.py).

## Структура проекта

```
rentui.kg/
├── anons/         # объявления, фото, регистрация и вход
├── main/          # главная, «О нас», услуги и контакты
├── config/        # настройки и URL
├── templates/     # шаблоны Django
├── static/        # CSS и картинки
└── images/        # картинки для этого README
```

---

<p align="center">
  <img src="images/readme/logo.png" width="72" alt="Логотип Rent Ui"><br><br>
  Сделано в Кыргызстане командой <b>Fidea</b>
</p>

<p align="center">
  <a href="https://www.instagram.com/fidea.312/"><img src="https://img.shields.io/badge/Instagram-141414?style=for-the-badge&logo=instagram&logoColor=946CF9" alt="Instagram"></a>
  <a href="https://t.me/fidea_kg"><img src="https://img.shields.io/badge/Telegram-141414?style=for-the-badge&logo=telegram&logoColor=946CF9" alt="Telegram"></a>
  <a href="https://wa.me/+996999888615"><img src="https://img.shields.io/badge/WhatsApp-141414?style=for-the-badge&logo=whatsapp&logoColor=946CF9" alt="WhatsApp"></a>
</p>

<p align="center"><sub>Распространяется по <a href="LICENSE">лицензии MIT</a></sub></p>

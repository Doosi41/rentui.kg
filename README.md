<p align="center"><b>English</b> &nbsp;|&nbsp; <a href="README.ru.md">Русский</a></p>

<p align="center">
  <a href="https://www.rentui.it.com">
    <img src="images/readme/banner.webp" alt="Rent Ui — rentals in Kyrgyzstan: direct, simple, everywhere" width="100%">
  </a>
</p>

<p align="center">
  <a href="https://www.rentui.it.com"><img src="https://img.shields.io/badge/Open_site-rentui.it.com-703BF7?style=for-the-badge&labelColor=141414" alt="Open site"></a>
  <img src="https://img.shields.io/badge/Python-3.12-703BF7?style=for-the-badge&logo=python&logoColor=white&labelColor=141414" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Django-5.0-703BF7?style=for-the-badge&logo=django&logoColor=white&labelColor=141414" alt="Django 5.0">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-703BF7?style=for-the-badge&labelColor=141414" alt="MIT license"></a>
</p>

<p align="center">
  <b>Rent Ui</b> is a website with rental listings in Kyrgyzstan.<br>
  Owners post flats and houses. People who need a home find them and call the owner directly — no agents and no fees.
</p>

<p align="center">
  <img src="images/readme/highlights.png" alt="Direct contact · All of Kyrgyzstan · Daily updates" width="100%">
</p>

## Preview

<p align="center">
  <img src="images/readme/showcase.webp" alt="Rent Ui home page on a computer and on a phone" width="100%">
</p>

<p align="center">
  <img src="images/readme/pages.webp" alt="About and sign-up pages" width="100%">
</p>

## Features

- **Accounts.** Sign up, log in, log out. After you log in, you go back to the page you came from.
- **Listings.** Title, description, price in som, address, phone number and photos.
- **Photo gallery.** The first photo becomes the cover, the other photos go to the gallery. Only images up to 5 MB are allowed.
- **Owner rights.** Only the author or an admin can edit or delete a listing.
- **Search.** By title and description, with pages.
- **Clean storage.** Photos are kept in DigitalOcean Spaces and are deleted together with the listing.
- **Mobile layout.** Pages fit any screen, and phones get a tab bar at the bottom.
- **Admin panel.** Django admin where you can see the photo gallery inside the listing.

## Tech stack

<p>
  <img src="https://img.shields.io/badge/Django-703BF7?style=flat-square&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-703BF7?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/DigitalOcean_Spaces-703BF7?style=flat-square&logo=digitalocean&logoColor=white" alt="DigitalOcean Spaces">
  <img src="https://img.shields.io/badge/WhiteNoise-703BF7?style=flat-square" alt="WhiteNoise">
  <img src="https://img.shields.io/badge/Vercel-703BF7?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">
</p>

| Part | Technology |
|---|---|
| Backend | Python 3.12, Django 5.0 |
| Database | PostgreSQL on Neon, or any database through `DATABASE_URL` |
| Photos | DigitalOcean Spaces through django-storages and boto3 |
| Static files | WhiteNoise |
| Hosting | Vercel |
| Frontend | Django templates, plain CSS, Font Awesome |

## Quick start

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
# paste the printed key into SECRET_KEY in .env

python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000.

## Configuration

On your computer, the settings come from `.env`. In production, they come from environment variables (see [`.env.example`](.env.example)).

| Variable | What it is |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development. Do not set it in production |
| `DATABASE_URL` | `sqlite:///db.sqlite3` on your computer, a PostgreSQL URL in production |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | DigitalOcean Spaces keys for photos. The site needs them to start |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail address and app password for the contact form |

## Tests

```bash
python manage.py test
```

Tests use the database from `DATABASE_URL`, so keep it on SQLite on your computer. Uploaded files stay in memory and are never sent to Spaces.

## Deploy

The site runs on Vercel ([`vercel.json`](vercel.json)). In **Project → Settings → Environment Variables** add every variable from the table above, except `DEBUG`. If you add a new domain, also add it to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in [`config/settings.py`](config/settings.py).

## Project structure

```
rentui.kg/
├── anons/         # listings, photos, sign up and log in
├── main/          # home, about, services and contact pages
├── config/        # settings and URLs
├── templates/     # Django templates
├── static/        # CSS and images
└── images/        # pictures for this README
```

---

<p align="center">
  <img src="images/readme/logo.png" width="72" alt="Rent Ui logo"><br><br>
  Made in Kyrgyzstan by the <b>Fidea</b> team
</p>

<p align="center">
  <a href="https://www.instagram.com/fidea.312/"><img src="https://img.shields.io/badge/Instagram-141414?style=for-the-badge&logo=instagram&logoColor=946CF9" alt="Instagram"></a>
  <a href="https://t.me/fidea_kg"><img src="https://img.shields.io/badge/Telegram-141414?style=for-the-badge&logo=telegram&logoColor=946CF9" alt="Telegram"></a>
  <a href="https://wa.me/+996999888615"><img src="https://img.shields.io/badge/WhatsApp-141414?style=for-the-badge&logo=whatsapp&logoColor=946CF9" alt="WhatsApp"></a>
</p>

<p align="center"><sub>Released under the <a href="LICENSE">MIT License</a></sub></p>

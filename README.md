# rentui.kg

Rental listings platform for Kyrgyzstan — tenants find homes directly from landlords, without agents or extra fees.

<p align="center">
  <img src="images/preview.png" width="800" alt="rentui.kg preview">
</p>

**Live:** [rentui.it.com](https://rentui.it.com)

## Features

- Sign up, log in and log out
- Landlords publish listings with price, address, phone number and a photo gallery
- Owners can edit and delete their listings
- Browse all listings and open a detailed property page
- Photos are stored in DigitalOcean Spaces (S3-compatible storage)
- Responsive layout for desktop, tablet and phone

## Tech stack

Python 3.12 · Django · PostgreSQL (any database via `DATABASE_URL`) · django-storages + boto3 (DigitalOcean Spaces) · WhiteNoise · Gunicorn · Vercel

## Quick start

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env            # fill in the values
python manage.py migrate && python manage.py runserver
```

Then open http://127.0.0.1:8000.

## Configuration

Settings are read from `.env` (see [`.env.example`](.env.example)):

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development; leave unset in production |
| `DATABASE_URL` | Database connection string, e.g. `sqlite:///db.sqlite3` locally or a PostgreSQL URL in production |
| `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | DigitalOcean Spaces keys for photo storage (required at startup) |
| `AWS_BUCKET_NAME`, `AWS_ENDPOINT_URL` | Spaces bucket and endpoint used by the upload helper |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail SMTP credentials for outgoing email |

## License

[MIT](LICENSE)

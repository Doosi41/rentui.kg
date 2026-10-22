<!-- This file is built automatically: python3 scripts/readme.py. Edits by hand will be lost. -->
<p align="center"><b>English</b> &nbsp;|&nbsp; <a href="README.ru.md">Русский</a></p>

<a href="https://www.rentui.it.com"><img src="images/readme/banner.svg" alt="Rent Ui — homes for rent in Kyrgyzstan. Direct. Simple. Everywhere." width="100%"></a>

<p align="center">
  <a href="#features">Features&nbsp;›</a>&emsp;
  <a href="#screens">Screens&nbsp;›</a>&emsp;
  <a href="#stack">Stack&nbsp;›</a>&emsp;
  <a href="#run">Run&nbsp;›</a>&emsp;
  <a href="#settings">Settings&nbsp;›</a>&emsp;
  <a href="#structure">Structure&nbsp;›</a>
</p>

<br>

<img src="images/readme/stats.svg" alt="No fees. 16 tests. Works on any screen." width="100%">

<br>
<br>

<p align="center">
  <i>“Simplicity is the ultimate sophistication.”</i><br>
  <sub>— Apple II brochure, 1977</sub>
</p>

<br>

<a name="features"></a>
<img src="images/readme/titles/features.svg" alt="Features" width="100%">

<a href="anons/models.py"><img src="images/readme/rows/listings.svg" alt="Listings — Title, description, price in som, address and phone" width="100%"></a>
<a href="anons/forms.py"><img src="images/readme/rows/photos.svg" alt="Photo gallery — The first photo is the cover, the other photos go to the gallery" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/rows/accounts.svg" alt="Accounts — Sign up, log in, log out and go back to the page you were on" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/rows/search.svg" alt="Search — By title and description, 20 listings per page" width="100%"></a>
<a href="anons/views.py"><img src="images/readme/rows/owner-only.svg" alt="Owner only — Only the author or an admin can edit or delete a listing" width="100%"></a>
<a href="anons/models.py"><img src="images/readme/rows/storage.svg" alt="Cloud storage — Photos are kept in DigitalOcean Spaces and are deleted with the listing" width="100%"></a>

<br>
<br>

<a name="screens"></a>
<img src="images/readme/titles/screens.svg" alt="Screens" width="100%">

<a href="https://www.rentui.it.com"><img src="images/readme/screens.webp" alt="Home, about and sign-up pages on iPhone" width="100%"></a>

<br>
<br>

<a name="stack"></a>
<img src="images/readme/titles/stack.svg" alt="Stack" width="100%">

<img src="images/readme/stack.svg" alt="Built with Python, Django, PostgreSQL, SQLite, DigitalOcean and Vercel" width="100%">

<br>
<br>

<a name="run"></a>
<img src="images/readme/titles/run.svg" alt="Run" width="100%">

<img src="images/readme/run.svg" alt="Install, run and test the project in the terminal" width="100%">

<details>
<summary>Copy the commands</summary>
<br>

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
# paste the key into SECRET_KEY in .env

python manage.py migrate
python manage.py runserver

# Tests: use SQLite in DATABASE_URL on your computer
python manage.py test

# Rebuild this README
python3 scripts/readme.py
```

</details>

<br>

<a name="settings"></a>
<img src="images/readme/titles/settings.svg" alt="Settings" width="100%">

<img src="images/readme/settings.svg" alt="Environment variables: SECRET_KEY, DATABASE_URL, AWS keys, email, DEBUG" width="100%">

<br>
<br>

<a name="structure"></a>
<img src="images/readme/titles/structure.svg" alt="Structure" width="100%">

<img src="images/readme/structure.svg" alt="Repository structure" width="100%">

<br>
<br>

<img src="images/readme/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">

<p align="center">
  <sub>Made by the Fidea team &nbsp;·&nbsp; <a href="https://github.com/a1tvv">@a1tvv</a> &nbsp;·&nbsp; <a href="LICENSE">MIT License</a></sub>
</p>

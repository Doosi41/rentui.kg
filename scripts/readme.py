#!/usr/bin/env python3
"""Собирает README и картинки в images/readme/ — в том же стиле iOS, что профиль и olymp.

Две версии: английская (README.md, картинки в images/readme) открывается на GitHub по умолчанию,
русская — README.ru.md, картинки в images/readme/ru. Сверху у обеих — ссылка-переключатель.

Число тестов и версии Python и Django берутся из самого проекта,
поэтому после изменений достаточно перезапустить:  python3 scripts/readme.py

Скриншоты сайта (images/readme/screens.webp) сняты отдельно, скрипт их не трогает.
"""
import glob
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'images', 'readme')
SITE = 'https://www.rentui.it.com'
LANG = 'en'


def tr(en, ru=None):
    """Текст на языке, который сейчас собирается: tr('eng', 'рус') или tr(('eng', 'рус')).
    Просто строка — одна на оба языка."""
    if ru is None:
        if isinstance(en, str):
            return en
        en, ru = en
    return ru if LANG == 'ru' else en


FONT = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
GRAD = {
    'blue': ('#64d2ff', '#0a84ff'), 'violet': ('#d48cff', '#7d3bd1'), 'green': ('#4ade80', '#1e9e47'),
    'orange': ('#ffb340', '#d26a00'), 'pink': ('#ff7a9a', '#e0245e'), 'indigo': ('#8e8cff', '#4b44d6'),
    'gray': ('#7c7c80', '#3a3a3c'),
}
AI_STOPS = ('<stop offset="0" stop-color="#ff9f0a"/><stop offset="0.35" stop-color="#ff375f"/>'
            '<stop offset="0.7" stop-color="#bf5af2"/><stop offset="1" stop-color="#0a84ff"/>')
TILE = ('<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#161618"/><stop offset="1" stop-color="#000000"/></linearGradient>')
TITANIUM = ('<linearGradient id="titanium" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0.2" stop-color="#ffffff"/><stop offset="1" stop-color="#8e8e93"/></linearGradient>')

# Логотипы технологий (Simple Icons, сетка 24×24) — те же, что в профиле
with open(os.path.join(ROOT, 'scripts', 'readme_icons.json')) as f:
    TECH_ICONS = json.load(f)

# Свои иконки в сетке 24×24: рисуются белым поверх цветного квадрата
GLYPHS = {
    'house': '<path d="M12 2.6 1.8 10.4l1.4 1.8L4.5 11.2V21h6v-6h3v6h6v-9.8l1.3 1 1.4-1.8z" fill="#fff"/>',
    'photo': ('<rect x="2.5" y="4.5" width="19" height="15" rx="3" fill="none" stroke="#fff" stroke-width="2"/>'
              '<circle cx="8.5" cy="9.5" r="1.8" fill="#fff"/>'
              '<path d="M3.5 17.5l5-5 4 4 3-3 5 5" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'),
    'person': '<circle cx="12" cy="7.5" r="4.2" fill="#fff"/><path d="M3.8 21a8.2 8.2 0 0 1 16.4 0z" fill="#fff"/>',
    'search': ('<circle cx="10.5" cy="10.5" r="6.3" fill="none" stroke="#fff" stroke-width="2.6"/>'
               '<path d="M15.3 15.3 20.5 20.5" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'),
    'lock': ('<rect x="4.5" y="10.5" width="15" height="11" rx="2.5" fill="#fff"/>'
             '<path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="#fff" stroke-width="2.4"/>'),
    'cloud': '<path d="M7 19.5a5 5 0 0 1-.7-9.95A6.5 6.5 0 0 1 18.9 9.6 4.95 4.95 0 0 1 18 19.5z" fill="#fff"/>',
    'key': ('<circle cx="8" cy="12" r="4.3" fill="none" stroke="#fff" stroke-width="2.4"/>'
            '<path d="M12.3 12H21M18 12v3M21 12v2.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'),
    'database': ('<ellipse cx="12" cy="5.8" rx="7" ry="2.8" fill="#fff"/>'
                 '<path d="M5 9v9.2c0 1.55 3.13 2.8 7 2.8s7-1.25 7-2.8V9c0 1.55-3.13 2.8-7 2.8S5 10.55 5 9z" fill="#fff"/>'),
    'mail': ('<rect x="2.5" y="5" width="19" height="14" rx="2.8" fill="#fff"/>'
             '<path d="M3.5 6.5 12 13l8.5-6.5" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="2" stroke-linejoin="round"/>'),
    'terminal': ('<path d="M5 7.5l4.5 4.5L5 16.5M12.5 16.5H19" fill="none" stroke="#fff" stroke-width="2.6" '
                 'stroke-linecap="round" stroke-linejoin="round"/>'),
    'phone': ('<rect x="7" y="2.5" width="10" height="19" rx="2.6" fill="none" stroke="#fff" stroke-width="2"/>'
              '<path d="M10.5 18.5h3" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'),
    'tablet': ('<rect x="4" y="3" width="16" height="18" rx="2.6" fill="none" stroke="#fff" stroke-width="2"/>'
               '<path d="M10.5 18h3" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'),
    'laptop': ('<rect x="4.5" y="5" width="15" height="10.5" rx="1.8" fill="none" stroke="#fff" stroke-width="2"/>'
               '<path d="M2 19h20" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'),
}

FEATURES = [
    # (файл картинки, название, описание, плашка справа, цвет иконки, иконка, куда ведёт строка)
    ('listings', ('Listings', 'Объявления'),
     ('Title, description, price in som, address and phone', 'Заголовок, описание, цена в сомах, адрес и телефон'),
     'CRUD', 'blue', 'house', 'anons/models.py'),
    ('photos', ('Photo gallery', 'Фотогалерея'),
     ('The first photo is the cover, the other photos go to the gallery', 'Первое фото — обложка, остальные идут в галерею'),
     ('≤ 5 MB', '≤ 5 МБ'), 'pink', 'photo', 'anons/forms.py'),
    ('accounts', ('Accounts', 'Аккаунты'),
     ('Sign up, log in, log out and go back to the page you were on', 'Регистрация, вход, выход и возврат на ту же страницу'),
     'auth', 'green', 'person', 'anons/views.py'),
    ('search', ('Search', 'Поиск'),
     ('By title and description, 20 listings per page', 'По заголовку и описанию, 20 объявлений на странице'),
     'Q()', 'violet', 'search', 'anons/views.py'),
    ('owner-only', ('Owner only', 'Только владелец'),
     ('Only the author or an admin can edit or delete a listing', 'Менять и удалять объявление может только автор или админ'),
     'POST', 'gray', 'lock', 'anons/views.py'),
    ('storage', ('Cloud storage', 'Облачное хранилище'),
     ('Photos are kept in DigitalOcean Spaces and are deleted with the listing',
      'Фото лежат в DigitalOcean Spaces и удаляются вместе с объявлением'),
     'S3', 'indigo', 'cloud', 'anons/models.py'),
]

STACK = [
    ('python', 'Python', ('Language', 'Язык')), ('django', 'Django', ('Backend', 'Бэкенд')),
    ('postgresql', 'PostgreSQL', ('Production', 'Продакшен')), ('sqlite', 'SQLite', ('Local & tests', 'Локально и тесты')),
    ('digitalocean', 'DigitalOcean', ('Photo storage', 'Хранение фото')), ('vercel', 'Vercel', ('Hosting', 'Хостинг')),
]

SETTINGS = [
    # (иконка, цвет, переменные, зачем нужны, обязательность)
    ('key', 'orange', 'SECRET_KEY', ('Django secret key', 'Секретный ключ Django'), 'Required'),
    ('database', 'blue', 'DATABASE_URL', ('SQLite locally, PostgreSQL on Vercel', 'Локально SQLite, на Vercel — PostgreSQL'),
     'Required'),
    ('cloud', 'indigo', 'AWS_ACCESS_KEY_ID · AWS_SECRET_ACCESS_KEY',
     ('DigitalOcean Spaces keys for photos', 'Ключи DigitalOcean Spaces для фото'), 'Required'),
    ('mail', 'pink', 'EMAIL_HOST_USER · EMAIL_HOST_PASSWORD',
     ('Gmail address and app password for the contact form', 'Адрес Gmail и пароль приложения для формы обратной связи'),
     'Optional'),
    ('terminal', 'gray', 'DEBUG', ('True on your computer, never on Vercel', 'True на своём компьютере, на Vercel — никогда'),
     'Local only'),
]
PILLS = {
    'Required': ('#0a84ff', '0.2', '#64d2ff'),
    'Optional': ('#ffffff', '0.08', '#c7c7cc'),
    'Local only': ('#ff9f0a', '0.16', '#ffb340'),
}
NEED_RU = {'Required': 'Обязательно', 'Optional': 'Необязательно', 'Local only': 'Только локально'}


# ───────────────────────── данные из проекта ─────────────────────────

def count_tests():
    total = 0
    for path in glob.glob(os.path.join(ROOT, '*', 'tests.py')):
        with open(path) as f:
            total += len(re.findall(r'^\s+def test_', f.read(), flags=re.M))
    return total


def versions():
    with open(os.path.join(ROOT, 'requirements.txt')) as f:
        django = re.search(r'^Django==(\d+\.\d+)', f.read(), flags=re.M | re.I).group(1)
    with open(os.path.join(ROOT, '.python-version')) as f:
        python = f.read().strip()
    return python, django


# ───────────────────────── SVG-помощники ─────────────────────────

def esc(s):
    return html.escape(str(s), quote=False)


def grad_def(gid, name):
    a, b = GRAD[name]
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')


def write_svg(path, w, h, label, defs, body):
    full = os.path.join(ASSETS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
                f'role="img" aria-label="{html.escape(label)}">\n<defs>{defs}</defs>\n'
                f'<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')


def app_icon(x, y, size, gid, inner):
    r = size * 0.26
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{r}" fill="url(#{gid})"/>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{size - 1}" height="{size - 1}" rx="{r}" fill="none" '
            f'stroke="#ffffff" stroke-opacity="0.18"/>' + inner)


def glyph(name, x, y, size, part=0.58):
    """Иконка из GLYPHS по центру квадрата size×size; part — какую долю квадрата она занимает."""
    scale = size * part / 24
    shift = (size - 24 * scale) / 2
    return f'<g transform="translate({x + shift:.2f} {y + shift:.2f}) scale({scale:.4f})">{GLYPHS[name]}</g>'


def tech_logo(name, x, y, size):
    scale = size * 0.0225
    shift = (size - 24 * scale) / 2
    return (f'<path transform="translate({x + shift:.2f} {y + shift:.2f}) scale({scale:.4f})" '
            f'd="{TECH_ICONS[name]["path"]}" fill="#ffffff"/>')


def rich(x, y, line, fs=21):
    """Строка, где `текст в обратных кавычках` выделяется моноширинным голубым."""
    out = f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="500" fill="#d1d1d6">'
    for i, part in enumerate(line.split('`')):
        if not part:
            continue
        if i % 2:
            out += (f'<tspan font-family="{MONO}" font-size="{fs - 2}" font-weight="600" '
                    f'fill="#64d2ff">{esc(part)}</tspan>')
        else:
            out += f'<tspan>{esc(part)}</tspan>'
    return out + '</text>'


def pill(right_x, y, text, bg, opacity, color, mono=False):
    w = 30 + (12 if mono else 11) * len(text)
    font = f' font-family="{MONO}"' if mono else ''
    return (f'<rect x="{right_x - w}" y="{y}" width="{w}" height="36" rx="18" fill="{bg}" fill-opacity="{opacity}"/>'
            f'<text x="{right_x - w / 2}" y="{y + 24}"{font} font-size="18" font-weight="600" fill="{color}" '
            f'text-anchor="middle">{esc(text)}</text>')


CHEVRON = ('<path d="M1160 53l12 13-12 13" fill="none" stroke="#636366" stroke-width="3.5" '
           'stroke-linecap="round" stroke-linejoin="round"/>')


# ───────────────────────── карточки ─────────────────────────

def banner():
    # Dynamic Island раскрывается и показывает, что сайт работает
    island = (
        '<rect x="530" y="30" width="140" height="46" rx="23" fill="#000000" stroke="#ffffff" stroke-opacity="0.16">'
        '<animate attributeName="width" values="140;140;480;480;140" keyTimes="0;0.1;0.2;0.86;1" dur="7s" '
        'repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0.9 0.2 1;0 0 1 1;0.5 0 0.2 1"/>'
        '<animate attributeName="x" values="530;530;360;360;530" keyTimes="0;0.1;0.2;0.86;1" dur="7s" '
        'repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;0.3 0.9 0.2 1;0 0 1 1;0.5 0 0.2 1"/></rect>'
        '<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.18;0.24;0.82;0.86;1" '
        'dur="7s" repeatCount="indefinite"/>'
        '<circle cx="393" cy="53" r="12" fill="#30d158" fill-opacity="0.25"/><circle cx="393" cy="53" r="6" fill="#30d158"/>'
        f'<text x="416" y="59.5" font-size="18" font-weight="600" fill="#ffffff">{tr("Live", "Онлайн")}</text>'
        '<text x="816" y="59.5" font-size="18" font-weight="600" fill="#30d158" text-anchor="end">rentui.it.com</text></g>'
    )
    defs = (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI_STOPS}'
            '<animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" to="360 0.5 0.5" '
            'dur="9s" repeatCount="indefinite"/></linearGradient>'
            f'<linearGradient id="aiText" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}</linearGradient>' + TITANIUM +
            '<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.07"/>'
            '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
            '<filter id="edgeGlow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="20"/></filter>'
            '<clipPath id="card"><rect width="1200" height="600" rx="32"/></clipPath>')
    body = (
        '<g clip-path="url(#card)"><rect width="1200" height="600" fill="#000000"/>'
        '<ellipse cx="600" cy="320" rx="560" ry="260" fill="url(#spot)"/>'
        '<rect width="1200" height="600" rx="32" fill="none" stroke="url(#ai)" stroke-width="40" filter="url(#edgeGlow)" opacity="0.85"/>'
        '<rect x="1.5" y="1.5" width="1197" height="597" rx="30.5" fill="none" stroke="url(#ai)" stroke-width="3"/></g>'
        + island +
        f'<text x="600" y="200" text-anchor="middle" font-size="28" font-weight="600" fill="url(#aiText)">{tr("Homes for rent in Kyrgyzstan", "Аренда жилья в Кыргызстане")}</text>'
        '<text x="600" y="338" text-anchor="middle" font-size="150" font-weight="700" letter-spacing="-4" fill="url(#titanium)">Rent Ui</text>'
        f'<text x="600" y="410" text-anchor="middle" font-size="36" font-weight="600" fill="#86868b">{tr("Direct. Simple. Everywhere.", "Напрямую. Просто. Везде.")}</text>'
        f'<text x="600" y="480" text-anchor="middle" font-size="26" font-weight="500" fill="#2997ff">{tr("Open the site ›", "Открыть сайт ›")}</text>'
    )
    write_svg('banner.svg', 1200, 600, tr('Rent Ui — homes for rent in Kyrgyzstan. Direct. Simple. Everywhere.',
                                          'Rent Ui — аренда жилья в Кыргызстане. Напрямую. Просто. Везде.'), defs, body)


def stats(tests, python, django):
    defs = (f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="1">{AI_STOPS}</linearGradient>'
            + grad_def('blue', 'blue') + TITANIUM + TILE +
            '<filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="60"/></filter>'
            '<clipPath id="t1"><rect width="590" height="540" rx="32"/></clipPath>')
    devices = ''.join(
        f'<rect x="{951 + 72 * i}" y="378" width="60" height="60" rx="16" fill="#1c1c1e" stroke="#ffffff" stroke-opacity="0.12"/>'
        + glyph(name, 951 + 72 * i, 378, 60, part=0.6)
        for i, name in enumerate(('phone', 'tablet', 'laptop')))
    body = (
        '<g font-weight="600">'
        # Комиссия
        '<g clip-path="url(#t1)"><rect width="590" height="540" fill="url(#tile)"/>'
        '<circle cx="470" cy="470" r="150" fill="url(#ai)" opacity="0.35" filter="url(#blur)"/></g>'
        '<rect x="0.5" y="0.5" width="589" height="539" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="48" y="86" font-size="24" fill="#86868b">{tr("Fees", "Комиссия")}</text>'
        '<text x="36" y="410" font-size="300" font-weight="700" letter-spacing="-10" fill="url(#ai)">0%</text>'
        f'<text x="48" y="490" font-size="22" fill="#86868b">{tr("Renters call the owners directly", "Арендаторы звонят хозяевам напрямую")}</text>'
        # Тесты
        '<rect x="610.5" y="0.5" width="589" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="658" y="86" font-size="24" fill="#86868b">{tr("Tests", "Тесты")}</text>'
        f'<text x="650" y="218" font-size="150" font-weight="700" letter-spacing="-4" fill="url(#blue)">{tests}</text>'
        '<text x="1152" y="170" font-size="32" font-weight="700" fill="#f5f5f7" text-anchor="end">Django TestCase</text>'
        f'<text x="1152" y="208" font-size="22" fill="#86868b" text-anchor="end">{tr("photos · access · login · search", "фото · доступ · вход · поиск")}</text>'
        # Стек
        '<rect x="610.5" y="280.5" width="284" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="646" y="344" font-size="24" fill="#86868b">{tr("Stack", "Стек")}</text>'
        '<text x="644" y="440" font-size="58" font-weight="700" letter-spacing="-1" fill="url(#titanium)">Django</text>'
        f'<text x="646" y="490" font-size="24" fill="#86868b">{django} · Python {python}</text>'
        # Устройства
        '<rect x="915.5" y="280.5" width="284" height="259" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
        f'<text x="951" y="344" font-size="24" fill="#ff9f0a">{tr("Works on", "Работает на")}</text>'
        + devices +
        f'<text x="951" y="490" font-size="22" fill="#86868b">{tr("any screen", "любом экране")}</text>'
        '</g>'
    )
    label = tr(f'No fees. {tests} tests. Django {django}, Python {python}. Works on phone, tablet and laptop.',
               f'Без комиссии. Тестов: {tests}. Django {django}, Python {python}. Работает на телефоне, планшете и ноутбуке.')
    write_svg('stats.svg', 1200, 540, label, defs, body)


def title(name, heading, subs):
    defs = f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}</linearGradient>'
    body = f'<text x="2" y="62" font-size="54" font-weight="700" letter-spacing="-1.2" fill="url(#ai)">{esc(heading)}</text>'
    for i, sub in enumerate(subs):
        body += f'<text x="3" y="{104 + 34 * i}" font-size="25" font-weight="500" fill="#8e8e93">{esc(sub)}</text>'
    write_svg(f'titles/{name}.svg', 1200, 92 + 34 * len(subs), heading, defs, body)


def feature_row(slug, name, about, tag, color, icon):
    body = ('<rect x="0.5" y="6.5" width="1199" height="119" rx="26" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            + app_icon(22, 24, 84, 'ic', glyph(icon, 22, 24, 84))
            + f'<text x="128" y="61" font-size="30" font-weight="600" fill="#f5f5f7">{esc(name)}</text>'
            f'<text x="128" y="99" font-size="21" font-weight="500" fill="#86868b">{esc(about)}</text>'
            + pill(1128, 48, tag, '#ffffff', '0.08', '#f5f5f7', mono=True) + CHEVRON)
    write_svg(f'rows/{slug}.svg', 1200, 132, f'{name} — {about}', TILE + grad_def('ic', color), body)


def stack():
    size, top = 112, 108
    defs = TILE + ''.join(
        f'<linearGradient id="t_{key}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TECH_ICONS[key]["colors"][0]}"/>'
        f'<stop offset="1" stop-color="{TECH_ICONS[key]["colors"][1]}"/></linearGradient>' for key, _, _ in STACK)
    body = ('<rect x="0.5" y="0.5" width="1199" height="329" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            f'<text x="60" y="72" font-size="20" font-weight="600" fill="#ff9f0a" letter-spacing="0.5">{tr("BUILT WITH", "СДЕЛАНО НА")}</text>')
    for i, (key, name, role) in enumerate(STACK):
        cx = 120 + 192 * i
        x = cx - size / 2
        body += (app_icon(x, top, size, f't_{key}', tech_logo(key, x, top, size))
                 + f'<text x="{cx}" y="{top + size + 42}" font-size="22" font-weight="700" fill="#f5f5f7" text-anchor="middle">{esc(name)}</text>'
                 f'<text x="{cx}" y="{top + size + 70}" font-size="17" font-weight="500" fill="#86868b" text-anchor="middle">{esc(tr(role))}</text>')
    write_svg('stack.svg', 1200, 330, tr('Built with ', 'Сделано на: ') + ', '.join(name for _, name, _ in STACK), defs, body)


def terminal(tests):
    p, t, op, com, out = '#30d158', '#f5f5f7', '#ff375f', '#636366', '#64d2ff'
    lines = [
        [(tr('# Install', '# Установка'), com)],
        [('$ ', p), ('git clone https://github.com/a1tvv/rentui.kg.git ', t), ('&&', op), (' cd rentui.kg', t)],
        [('$ ', p), ('python3 -m venv .venv ', t), ('&&', op), (' source .venv/bin/activate', t)],
        [('$ ', p), ('pip install -r requirements.txt', t)],
        [('$ ', p), ('cp .env.example .env', t), (tr('   # then fill in SECRET_KEY', '   # потом впиши SECRET_KEY'), com)],
        [],
        [(tr('# Run', '# Запуск'), com)],
        [('$ ', p), ('python manage.py migrate', t)],
        [('$ ', p), ('python manage.py runserver', t)],
        [('Starting development server at http://127.0.0.1:8000/', out)],
        [],
        [(tr('# Test', '# Тесты'), com)],
        [('$ ', p), ('python manage.py test', t)],
        [(f'Ran {tests} tests · OK', out)],
    ]
    lh, top = 36, 122
    h = top + lh * (len(lines) - 1) + 56
    body = (f'<rect x="0.5" y="0.5" width="1199" height="{h - 1}" rx="23.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<rect x="1" y="1" width="1198" height="59" rx="23" fill="#ffffff" fill-opacity="0.04"/>'
            '<line x1="1" y1="60.5" x2="1199" y2="60.5" stroke="#ffffff" stroke-opacity="0.08"/>'
            + ''.join(f'<circle cx="{34 + 24 * k}" cy="30" r="7" fill="{col}"/>' for k, col in enumerate(('#ff5f57', '#febc2e', '#28c840')))
            + f'<text x="600" y="36" font-family="{MONO}" font-size="16" fill="#8e8e93" text-anchor="middle">zsh — rentui.kg</text>')
    for i, segs in enumerate(lines):
        if segs:
            body += (f'<text x="48" y="{top + i * lh}" font-family="{MONO}" font-size="20" xml:space="preserve" style="white-space:pre">'
                     + ''.join(f'<tspan fill="{col}">{esc(txt)}</tspan>' for txt, col in segs) + '</text>')
    write_svg('run.svg', 1200, h, tr('Install, run and test the project in the terminal',
                                     'Установка, запуск и тесты проекта в терминале'), TILE, body)


def settings():
    # Как экран «Настройки» в iOS: иконка, название, пояснение и плашка справа
    row, top = 100, 20
    h = top + row * len(SETTINGS) + 76
    defs = TILE + ''.join(grad_def(f'ic{i}', color) for i, (_, color, _, _, _) in enumerate(SETTINGS))
    body = f'<rect x="0.5" y="0.5" width="1199" height="{h - 1}" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
    for i, (icon, _, names, about, need) in enumerate(SETTINGS):
        y = top + row * i
        bg, opacity, color = PILLS[need]
        body += (app_icon(40, y + 24, 52, f'ic{i}', glyph(icon, 40, y + 24, 52))
                 + f'<text x="116" y="{y + 46}" font-family="{MONO}" font-size="21" font-weight="600" fill="#f5f5f7">{esc(names)}</text>'
                 f'<text x="116" y="{y + 78}" font-size="19" font-weight="500" fill="#86868b">{esc(tr(about))}</text>'
                 + pill(1160, y + 32, tr(need, NEED_RU[need]), bg, opacity, color))
        if i < len(SETTINGS) - 1:
            body += f'<line x1="116" y1="{y + row + .5}" x2="1160" y2="{y + row + .5}" stroke="#ffffff" stroke-opacity="0.08"/>'
    body += rich(40, h - 34, tr('On your computer from `.env`, on Vercel from Environment Variables. Never commit `.env`',
                                'Локально — из `.env`, на Vercel — из Environment Variables. Никогда не коммить `.env`'), fs=20)
    write_svg('settings.svg', 1200, h, tr('Environment variables: ', 'Переменные окружения: ') + ', '.join(s[2] for s in SETTINGS),
              defs, body)


def structure():
    tree = [
        (0, 'rentui.kg/', ''),
        (1, 'anons/', tr('listings, photos, sign up and log in', 'объявления, фото, регистрация и вход')),
        (1, 'main/', tr('home, about, services and contacts', 'главная, «О нас», услуги и контакты')),
        (1, 'config/', tr('settings and URLs', 'настройки и URL')),
        (1, 'templates/', tr('Django templates', 'шаблоны Django')),
        (1, 'static/', tr('site CSS and images', 'CSS и картинки сайта')),
        (1, 'scripts/', tr('builds this README', 'сборка этого README')),
        (1, 'images/readme/', tr('pictures for this README', 'картинки для этого README')),
        (1, 'requirements.txt', tr('package versions', 'версии пакетов')),
        (1, 'vercel.json', tr('Vercel settings', 'настройки Vercel')),
    ]
    row, top, x0, ind = 46, 74, 48, 44
    h = top + row * len(tree) + 130
    defs = TILE + grad_def('folder', 'blue') + grad_def('root', 'violet') + grad_def('file', 'gray')
    lines, items = '', ''
    for i, (d, name, desc) in enumerate(tree):
        y, x = top + i * row, x0 + d * ind
        if d:
            p = max(k for k in range(i) if tree[k][0] == d - 1)
            px, py = x0 + (d - 1) * ind + 15, top + p * row
            lines += f'<path d="M{px} {py + 8}V{y - 8}H{x - 8}" fill="none" stroke="#3a3a3c" stroke-width="2"/>'
        if name.endswith('/'):
            fill = 'root' if d == 0 else 'folder'
            items += (f'<path transform="translate({x} {y - 19})" d="M0 4a3 3 0 0 1 3-3h7.5l3 3.5H27a3 3 0 0 1 3 3V19a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3z" '
                      f'fill="url(#{fill})"/>')
        else:
            items += f'<path transform="translate({x + 5} {y - 22})" d="M0 3a3 3 0 0 1 3-3h10l7 7v15a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3z" fill="url(#file)"/>'
        items += f'<text x="{x + 42}" y="{y}" font-family="{MONO}" font-size="21" font-weight="600" fill="#f5f5f7">{esc(name)}</text>'
        if desc:
            items += f'<text x="660" y="{y}" font-size="21" font-weight="500" fill="#86868b">{esc(desc)}</text>'
    ny = h - 78
    body = (f'<rect x="0.5" y="0.5" width="1199" height="{h - 1}" rx="31.5" fill="url(#tile)" stroke="#ffffff" stroke-opacity="0.1"/>'
            + lines + items +
            f'<line x1="48" y1="{ny - 42}" x2="1152" y2="{ny - 42}" stroke="#ffffff" stroke-opacity="0.08"/>'
            + rich(48, ny, tr('Tests are next to the code: `anons/tests.py` and `main/tests.py`',
                              'Тесты лежат рядом с кодом: `anons/tests.py` и `main/tests.py`'), fs=20)
            + rich(48, ny + 36, tr('Push to `main` and Vercel puts it online. Secrets are kept in Environment Variables',
                                   'Пуш в `main` — и Vercel выкатит сайт. Секреты хранятся в Environment Variables'), fs=20))
    write_svg('structure.svg', 1200, h, tr('Repository structure', 'Структура репозитория'), defs, body)


def footer():
    defs = (TITANIUM + f'<linearGradient id="ai" x1="0" y1="0" x2="1" y2="0">{AI_STOPS}'
            '<animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>'
            '</linearGradient><radialGradient id="spot" cx="0.5" cy="1" r="0.7"><stop offset="0" stop-color="#bf5af2" stop-opacity="0.22"/>'
            '<stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></radialGradient>'
            '<clipPath id="card"><rect width="1200" height="380" rx="32"/></clipPath>')
    body = ('<g clip-path="url(#card)"><rect width="1200" height="380" fill="#000000"/><rect width="1200" height="380" fill="url(#spot)"/></g>'
            '<rect x="0.5" y="0.5" width="1199" height="379" rx="31.5" fill="none" stroke="#ffffff" stroke-opacity="0.1"/>'
            '<g font-weight="700" text-anchor="middle">'
            '<text x="600" y="160" font-size="96" letter-spacing="-3" fill="url(#titanium)">Stay hungry.</text>'
            '<text x="600" y="262" font-size="96" letter-spacing="-3" fill="url(#ai)">Stay foolish.</text>'
            '<text x="600" y="326" font-size="22" font-weight="600" fill="#86868b">Steve Jobs · 1955–2011</text></g>')
    write_svg('footer.svg', 1200, 380, 'Stay hungry. Stay foolish. — Steve Jobs, 1955–2011', defs, body)


# ───────────────────────── README ─────────────────────────

def section_title(anchor, name, alt, img):
    return f'<a name="{anchor}"></a>\n<img src="{img}/titles/{name}.svg" alt="{alt}" width="100%">\n'


def readme(tests):
    img = 'images/readme' if LANG == 'en' else 'images/readme/ru'  # футер и скриншоты — общие
    switch = ('<p align="center"><b>English</b> &nbsp;|&nbsp; <a href="README.ru.md">Русский</a></p>' if LANG == 'en' else
              '<p align="center"><a href="README.md">English</a> &nbsp;|&nbsp; <b>Русский</b></p>')
    nav = '&emsp;\n  '.join(f'<a href="#{anchor}">{tr(name)}&nbsp;›</a>' for anchor, name in (
        ('features', ('Features', 'Возможности')), ('screens', ('Screens', 'Экраны')), ('stack', ('Stack', 'Стек')),
        ('run', ('Run', 'Запуск')), ('settings', ('Settings', 'Настройки')), ('structure', ('Structure', 'Структура'))))
    rows = '\n'.join(f'<a href="{link}"><img src="{img}/rows/{slug}.svg" alt="{tr(name)} — {tr(about)}" width="100%"></a>'
                     for slug, name, about, _, _, _, link in FEATURES)

    text = f'''{tr('<!-- This file is built automatically: python3 scripts/readme.py. Edits by hand will be lost. -->',
             '<!-- Этот файл собирается автоматически: python3 scripts/readme.py. Правки вручную перезапишутся. -->')}
{switch}

<a href="{SITE}"><img src="{img}/banner.svg" alt="{tr('Rent Ui — homes for rent in Kyrgyzstan. Direct. Simple. Everywhere.',
                                                     'Rent Ui — аренда жилья в Кыргызстане. Напрямую. Просто. Везде.')}" width="100%"></a>

<p align="center">
  {nav}
</p>

<br>

<img src="{img}/stats.svg" alt="{tr(f'No fees. {tests} tests. Works on any screen.',
                                    f'Без комиссии. Тестов: {tests}. Работает на любом экране.')}" width="100%">

<br>
<br>

<p align="center">
  <i>“Simplicity is the ultimate sophistication.”</i><br>
  <sub>— {tr('Apple II brochure, 1977', 'брошюра Apple II, 1977')}</sub>
</p>

<br>

{section_title('features', 'features', tr('Features', 'Возможности'), img)}
{rows}

<br>
<br>

{section_title('screens', 'screens', tr('Screens', 'Экраны'), img)}
<a href="{SITE}"><img src="images/readme/screens.webp" alt="{tr('Home, about and sign-up pages on iPhone',
                                                                'Главная, «О нас» и регистрация на iPhone')}" width="100%"></a>

<br>
<br>

{section_title('stack', 'stack', tr('Stack', 'Стек'), img)}
<img src="{img}/stack.svg" alt="{tr('Built with Python, Django, PostgreSQL, SQLite, DigitalOcean and Vercel',
                                    'Сделано на Python, Django, PostgreSQL, SQLite, DigitalOcean и Vercel')}" width="100%">

<br>
<br>

{section_title('run', 'run', tr('Run', 'Запуск'), img)}
<img src="{img}/run.svg" alt="{tr('Install, run and test the project in the terminal',
                                  'Установка, запуск и тесты проекта в терминале')}" width="100%">

<details>
<summary>{tr('Copy the commands', 'Скопировать команды')}</summary>
<br>

```bash
git clone https://github.com/a1tvv/rentui.kg.git && cd rentui.kg
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
{tr('# paste the key into SECRET_KEY in .env', '# вставь ключ в SECRET_KEY в .env')}

python manage.py migrate
python manage.py runserver

{tr('# Tests: use SQLite in DATABASE_URL on your computer', '# Тесты: локально держи DATABASE_URL на SQLite')}
python manage.py test

{tr('# Rebuild this README', '# Пересобрать этот README')}
python3 scripts/readme.py
```

</details>

<br>

{section_title('settings', 'settings', tr('Settings', 'Настройки'), img)}
<img src="{img}/settings.svg" alt="{tr('Environment variables: SECRET_KEY, DATABASE_URL, AWS keys, email, DEBUG',
                                       'Переменные окружения: SECRET_KEY, DATABASE_URL, ключи AWS, почта, DEBUG')}" width="100%">

<br>
<br>

{section_title('structure', 'structure', tr('Structure', 'Структура'), img)}
<img src="{img}/structure.svg" alt="{tr('Repository structure', 'Структура репозитория')}" width="100%">

<br>
<br>

<img src="images/readme/footer.svg" alt="Stay hungry. Stay foolish. — Steve Jobs, 1955–2011" width="100%">

<p align="center">
  <sub>{tr('Made by the Fidea team', 'Сделано командой Fidea')} &nbsp;·&nbsp; <a href="https://github.com/a1tvv">@a1tvv</a> &nbsp;·&nbsp; <a href="LICENSE">{tr('MIT License', 'Лицензия MIT')}</a></sub>
</p>
'''
    with open(os.path.join(ROOT, 'README.md' if LANG == 'en' else 'README.ru.md'), 'w') as f:
        f.write(text)


def build(lang, tests, python, django):
    """Картинки и README на одном языке: 'en' — images/readme и README.md, 'ru' — images/readme/ru и README.ru.md."""
    global LANG, ASSETS
    LANG = lang
    ASSETS = os.path.join(ROOT, 'images', 'readme') if lang == 'en' else os.path.join(ROOT, 'images', 'readme', 'ru')
    for sub in ('rows', 'titles'):  # сгенерированные папки пересоздаём, чтобы не копился мусор
        shutil.rmtree(os.path.join(ASSETS, sub), ignore_errors=True)

    banner()
    stats(tests, python, django)
    for slug, name, about, tag, color, icon, _ in FEATURES:
        feature_row(slug, tr(name), tr(about), tr(tag), color, icon)
    title('features', tr('Features', 'Возможности'),
          [tr('Everything an owner and a renter need.', 'Всё, что нужно хозяину и арендатору.'),
           tr('Click a row to open its code.', 'Нажми на строку — откроется её код.')])
    title('screens', tr('Screens', 'Экраны'), [tr('The real site, on a phone.', 'Настоящий сайт на телефоне.')])
    title('stack', tr('Stack', 'Стек'), [tr('Small, simple, reliable.', 'Маленький, простой, надёжный.')])
    title('run', tr('Run', 'Запуск'), [tr('Copy. Paste. Done.', 'Скопировал. Вставил. Готово.')])
    title('settings', tr('Settings', 'Настройки'),
          [tr('Set a few variables, and the site is yours.', 'Пара переменных — и сайт твой.')])
    title('structure', tr('Structure', 'Структура'), [tr('Everything in its place.', 'Всё на своих местах.')])
    stack()
    terminal(tests)
    settings()
    structure()
    if lang == 'en':  # в футере нет текста на русском — он общий для обеих версий
        footer()
    readme(tests)


def main():
    tests = count_tests()
    python, django = versions()
    build('en', tests, python, django)
    build('ru', tests, python, django)
    print(f'README.md и README.ru.md собраны: тестов {tests}, Django {django}, Python {python}')


if __name__ == '__main__':
    main()

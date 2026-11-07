# My Thoughts

A personal thoughts website built with Django and SQLite.

- **Pages:** Home (latest 3), Thoughts (Newest/Oldest sort, 10 per page), single thought (body only), About
- **Search:** live dropdown plus a full results page, across titles and bodies
- **Writing:** `/admin/` (title + Markdown body, draft or publish, edit, delete)
- **Dates:** 24-hour IST. Publishing or editing a thought sets its time to now and moves it to the top
- **Extras:** dark/light toggle (dark default), share buttons, RSS at `/feed/`, backup commands

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and write at http://127.0.0.1:8000/admin/.

## Customize

- **Background:** copy your 1280x720 mp4 or gif into `static/media/` and set `SITE["background"]` in `config/settings.py` (for example `"media/background.mp4"`). Keep it under about 10 MB. Until you add one, a dark gradient shows.
- **Site name, intro, About text, footer links:** edit `SITE` in `config/settings.py`.
- **Accent color:** change `--accent` in `static/css/style.css`.

## Backup and restore

```bash
python manage.py export_thoughts                 # writes thoughts_backup.json
python manage.py import_thoughts thoughts_backup.json   # restore into an empty database
```

`db.sqlite3` and the backup file are in `.gitignore`, so your thoughts are never pushed to GitHub.

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

## Deploy on PythonAnywhere (free)

Free web apps expire after a month. Log in and press the extend button on the Web tab to keep it live.

1. Create a free account at pythonanywhere.com. Your site will be `YOURUSERNAME.pythonanywhere.com`.
2. Open a **Bash console** and clone your repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git thoughts-site
   cd thoughts-site
   ```
3. Create a virtualenv (pick a Python version PythonAnywhere offers, 3.10 or newer):
   ```bash
   mkvirtualenv --python=python3.12 thoughts-env
   pip install -r requirements.txt
   ```
4. Set up the database and static files, and create your admin login:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
5. **Web** tab, then **Add a new web app**, then **Manual configuration**, with the same Python version.
6. On the Web tab set:
   - **Source code** and **Working directory:** `/home/YOURUSERNAME/thoughts-site`
   - **Virtualenv:** `/home/YOURUSERNAME/.virtualenvs/thoughts-env`
   - **Static files:** URL `/static/` pointing to `/home/YOURUSERNAME/thoughts-site/staticfiles`
7. Open the **WSGI configuration file** link, delete its contents and paste:
   ```python
   import os, sys

   path = "/home/YOURUSERNAME/thoughts-site"
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
   os.environ["DJANGO_DEBUG"] = "0"
   os.environ["DJANGO_SECRET_KEY"] = "PASTE-A-LONG-RANDOM-STRING"
   os.environ["DJANGO_ALLOWED_HOSTS"] = "YOURUSERNAME.pythonanywhere.com"

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
   Generate a secret key with `python -c "import secrets; print(secrets.token_urlsafe(50))"`.
8. Press **Reload**. Visit your site and sign in at `/admin/`.

**Updating later:** `git pull` in the console, run `python manage.py migrate` and `python manage.py collectstatic --noinput` if needed, then press Reload.

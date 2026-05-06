# Kakahoyan — Quick Setup Guide (SQLite / Local)

## Steps to run the site locally

### 1. Extract and enter the project folder
```
cd kakahoyan
```

### 2. Create and activate virtual environment
```
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set your environment variables
Open `.env` and fill in at minimum:
```
SECRET_KEY=any-random-long-string-here
DEBUG=True
ANTHROPIC_API_KEY=your-key-from-console.anthropic.com
```
Leave Cloudinary blank for now — photos will be saved locally.

### 5. ✅ Run migrations (REQUIRED — fixes the OperationalError)
```
python manage.py migrate
```

### 6. Create admin account
```
python manage.py createsuperuser
```
Then in a separate shell:
```
python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.get(username='YOUR_USERNAME')
u.is_staff = True
u.save()
print('Done — you can now log in to /admin-panel/')
"
```

### 7. Run the server
```
python manage.py runserver
```

### 8. Open in browser
- **Client site:** http://127.0.0.1:8000/
- **Custom admin panel:** http://127.0.0.1:8000/admin-panel/login/
- **Django admin:** http://127.0.0.1:8000/django-admin/

---

## Common errors and fixes

| Error | Fix |
|---|---|
| `no such table: core_sitesettings` | You forgot to run `python manage.py migrate` |
| `No module named 'anthropic'` | Run `pip install -r requirements.txt` |
| Chatbot replies "I'm currently unavailable" | Add your `ANTHROPIC_API_KEY` in `.env` |
| Images not showing | Make sure `media/` folder exists in the project root |


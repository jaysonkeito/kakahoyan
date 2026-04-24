# Kakahoyan Event Place — Web System

A full-featured Django web system for Kakahoyan Event Place in Sta. Catalina, Negros Oriental.

## Features

### Client Interface
- **Homepage** — Hero section, event types, featured gallery, Google Maps, recent posts, contact CTA
- **Gallery** — Filterable photo/video gallery with lightbox viewer (Cloudinary-hosted)
- **Appointments** — Booking form with meeting type selection (phone call / at Kakahoyan / client address between Sta. Catalina–Bayawan City)
- **Posts/Updates** — Event highlights and news feed
- **AI Chatbot** — Claude-powered assistant that answers venue inquiries 24/7 (bottom-right bubble on all pages)
- **About Page** — Venue story and capacity info

### Admin Panel (`/admin-panel/`)
- **Dashboard** — Stats overview + recent appointments
- **Gallery Manager** — Upload photos/videos (multi-file), categorize, mark as featured, delete
- **Posts Manager** — Create/edit/delete posts with cover images (mirrors Facebook-style updates)
- **Appointments** — View all requests, filter by status, update status, add notes
- **Chatbot Logs** — Browse all client chat sessions and messages

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+ / Django 5.0 |
| Database | PostgreSQL |
| Media Storage | Cloudinary |
| AI Chatbot | Anthropic Claude API |
| Frontend | Bootstrap 5 + custom CSS |
| Fonts | Cormorant Garamond + DM Sans |
| Email | Gmail SMTP (for appointment notifications) |
| Production Server | Gunicorn + WhiteNoise |

---

## Setup Instructions

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd kakahoyan
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Required values:
```
SECRET_KEY=<generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
DEBUG=True

# PostgreSQL
DB_NAME=kakahoyan_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Cloudinary (https://cloudinary.com — free tier works)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Anthropic (https://console.anthropic.com)
ANTHROPIC_API_KEY=your-anthropic-key

# Email (Gmail — enable App Passwords in Google Account settings)
EMAIL_HOST_USER=youremail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMIN_EMAIL=admin@kakahoyan.com
```

### 3. Database Setup

```bash
# Create the PostgreSQL database first
createdb kakahoyan_db

# Run migrations
python manage.py migrate

# Create a superuser (for admin panel access)
python manage.py createsuperuser
```

> **Note:** After creating the superuser, go to Django admin (`/django-admin/`) and set `is_staff = True` on the user, OR use `python manage.py shell`:
> ```python
> from django.contrib.auth.models import User
> u = User.objects.get(username='your-username')
> u.is_staff = True
> u.save()
> ```

### 4. Seed Initial Data (Optional)

```bash
python manage.py shell
```
```python
from apps.gallery.models import MediaCategory
MediaCategory.objects.bulk_create([
    MediaCategory(name='Glass Pavilion', slug='glass-pavilion', order=1),
    MediaCategory(name='Lawn & Outdoor', slug='lawn-outdoor', order=2),
    MediaCategory(name='Weddings', slug='weddings', order=3),
    MediaCategory(name='Birthdays & Parties', slug='birthdays', order=4),
    MediaCategory(name='Corporate Events', slug='corporate', order=5),
])
print("Categories created!")
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit:
- **Client site:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin-panel/login/
- **Django admin:** http://127.0.0.1:8000/django-admin/

---

## Project Structure

```
kakahoyan/
├── kakahoyan/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/               # Homepage, about page
│   ├── gallery/            # Media gallery (Cloudinary)
│   ├── appointments/       # Booking/consultation form
│   ├── chatbot/            # Claude AI chatbot API
│   ├── posts/              # News/event posts
│   └── admin_panel/        # Custom admin dashboard
├── templates/
│   ├── base.html           # Site-wide layout + chatbot
│   ├── core/
│   ├── gallery/
│   ├── appointments/
│   ├── posts/
│   └── admin_panel/
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Google Maps

To use the real Kakahoyan location on the map, replace the Google Maps embed URL in `templates/core/home.html`:

1. Go to [Google Maps](https://maps.google.com)
2. Search for **Kakahoyan, Sta. Catalina, Negros Oriental**
3. Click **Share → Embed a map → Copy HTML**
4. Replace the `<iframe src="...">` in the template with the one you copied

---

## Deployment (Production)

```bash
# Collect static files
python manage.py collectstatic

# Set in .env:
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Run with Gunicorn
gunicorn kakahoyan.wsgi:application --bind 0.0.0.0:8000
```

Recommended: Deploy on **Railway**, **Render**, or a VPS (Ubuntu + Nginx + Gunicorn).

---

## Contact

- **Venue:** Purok 2, Brgy. Caranoche, Sta. Catalina, Negros Oriental, 6220
- **Phone:** 0920 611 2718
- **Facebook:** [Kakahoyan](https://www.facebook.com/Kakahoyan)

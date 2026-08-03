"""
Django settings for the store project.

Reads SECRET_KEY and DEBUG from environment variables (via python-dotenv)
so the same code works locally and on Render.
"""

import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

# Load variables from a .env file in the project root (local dev only)
load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
print("EMAIL USER LOADED:", EMAIL_HOST_USER, flush=True)
print("EMAIL_HOST_USER is:", repr(EMAIL_HOST_USER), flush=True)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_TIMEOUT = int(os.environ.get("EMAIL_TIMEOUT", "5"))
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "webmaster@localhost"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --- Security ---
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-key-change-this-before-deploying",
)
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# --- Apps ---
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",  # our e-commerce app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "store.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.context_processors.cart_count",  # cart badge in navbar
            ],
        },
    },
]

WSGI_APPLICATION = "store.wsgi.application"

# --- Database ---
# Uses SQLite locally; switches to PostgreSQL when DATABASE_URL is set (Render)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Render provides postgres:// — Django needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    db_url = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db_url.path[1:],
            "USER": db_url.username,
            "PASSWORD": db_url.password,
            "HOST": db_url.hostname,
            "PORT": db_url.port or 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Auth password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static files (CSS, JS, images) ---
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Student Store Admin",
    "site_header": "Student Store Admin",
    "site_brand": "Student Store",
    "welcome_sign": "Welcome to the Student Store admin panel",
    "copyright": "Student Store",
    "icons": {
        "shop.Product": "fas fa-box",
        "shop.Order": "fas fa-receipt",
        "shop.OrderItem": "fas fa-list",
        "auth.User": "fas fa-user",
    },
}

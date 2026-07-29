import os
from pathlib import Path

from dotenv import load_dotenv


# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent


# تحميل المتغيرات السرية من ملف .env
load_dotenv(BASE_DIR / ".env")


# مفتاح مشروع Django
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "المتغير DJANGO_SECRET_KEY غير موجود داخل ملف .env"
    )


# وضع التطوير
DEBUG = os.getenv("DEBUG", "True").lower() == "true"


# النطاقات المسموح لها
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


# التطبيقات المثبتة
INSTALLED_APPS = [
    # تطبيقات Django الأساسية
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # تطبيقات Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # تطبيقات المشروع
    "accounts.apps.AccountsConfig",
    "catalog.apps.CatalogConfig",
    "orders.apps.OrdersConfig",
]


# البرمجيات الوسيطة
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ملف الروابط الرئيسي
ROOT_URLCONF = "hassan1.urls"


# إعدادات القوالب
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# بوابة WSGI
WSGI_APPLICATION = "hassan1.wsgi.application"


# قاعدة البيانات
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# اللغة والتوقيت
LANGUAGE_CODE = "ar"

TIME_ZONE = "Asia/Riyadh"

USE_I18N = True

USE_TZ = True


# ==========================================
# إعدادات ملفات Static
# ==========================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ==========================================
# إعدادات Cloudinary
# ==========================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    "SECURE": True,
}


# التحقق من وجود مفاتيح Cloudinary
if not CLOUDINARY_STORAGE["CLOUD_NAME"]:
    raise ValueError(
        "المتغير CLOUDINARY_CLOUD_NAME غير موجود داخل ملف .env"
    )

if not CLOUDINARY_STORAGE["API_KEY"]:
    raise ValueError(
        "المتغير CLOUDINARY_API_KEY غير موجود داخل ملف .env"
    )

if not CLOUDINARY_STORAGE["API_SECRET"]:
    raise ValueError(
        "المتغير CLOUDINARY_API_SECRET غير موجود داخل ملف .env"
    )


# ==========================================
# أنظمة التخزين
# ==========================================

STORAGES = {
    # تخزين ملفات الميديا داخل Cloudinary
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage."
            "MediaCloudinaryStorage"
        ),
    },

    # تخزين ملفات static بالطريقة العادية
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage."
            "StaticFilesStorage"
        ),
    },
}


# رابط ملفات الميديا
MEDIA_URL = "/media/"


# نوع المفتاح الأساسي الافتراضي
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
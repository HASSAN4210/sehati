import os
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# المسار الأساسي للمشروع
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# تحميل متغيرات البيئة
# =========================================================

load_dotenv(BASE_DIR / ".env")


# =========================================================
# الإعدادات الأساسية
# =========================================================

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError(
        "المتغير DJANGO_SECRET_KEY غير موجود. "
        "أضفه داخل ملف .env محليًا أو داخل Environment في Render."
    )


DEBUG = os.getenv("DEBUG", "True").strip().lower() == "true"


# =========================================================
# النطاقات المسموح بها
# =========================================================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


# يضيف Render اسم رابط الموقع تلقائيًا
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# يسمح بإضافة نطاقات إضافية من متغير البيئة عند الحاجة
# مثال:
# ALLOWED_HOSTS=example.com,www.example.com
EXTRA_ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "")

if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in EXTRA_ALLOWED_HOSTS.split(",")
        if host.strip()
    )


# إزالة النطاقات المكررة
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))


# =========================================================
# النطاقات الموثوقة لحماية CSRF
# =========================================================

CSRF_TRUSTED_ORIGINS = []

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_EXTERNAL_HOSTNAME}"
    )


# يمكن إضافة نطاقات أخرى من Render عند الحاجة
# مثال:
# CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
EXTRA_CSRF_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "")

if EXTRA_CSRF_ORIGINS:
    CSRF_TRUSTED_ORIGINS.extend(
        origin.strip()
        for origin in EXTRA_CSRF_ORIGINS.split(",")
        if origin.strip()
    )


CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))


# =========================================================
# التطبيقات المثبتة
# =========================================================

INSTALLED_APPS = [
    # تطبيقات Django الأساسية
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    "cloudinary",
    "cloudinary_storage",

    # تطبيقات المشروع
    "accounts.apps.AccountsConfig",
    "catalog.apps.CatalogConfig",
    "orders.apps.OrdersConfig",
]


# =========================================================
# البرمجيات الوسيطة
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # يجب أن يأتي بعد SecurityMiddleware مباشرة
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# الروابط والقوالب
# =========================================================

ROOT_URLCONF = "hassan1.urls"


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


WSGI_APPLICATION = "hassan1.wsgi.application"


# =========================================================
# قاعدة البيانات
# =========================================================
# حاليًا يستخدم SQLite محليًا.
# لاحقًا يمكن ربط PostgreSQL في Render.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================================================
# التحقق من كلمات المرور
# =========================================================

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


# =========================================================
# اللغة والتوقيت
# =========================================================

LANGUAGE_CODE = "ar"

TIME_ZONE = "Asia/Riyadh"

USE_I18N = True

USE_TZ = True


# =========================================================
# ملفات Static
# =========================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# إعدادات Cloudinary
# =========================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    "SECURE": True,
}


CLOUDINARY_REQUIRED_VARIABLES = {
    "CLOUDINARY_CLOUD_NAME": CLOUDINARY_STORAGE["CLOUD_NAME"],
    "CLOUDINARY_API_KEY": CLOUDINARY_STORAGE["API_KEY"],
    "CLOUDINARY_API_SECRET": CLOUDINARY_STORAGE["API_SECRET"],
}


missing_cloudinary_variables = [
    variable_name
    for variable_name, variable_value in CLOUDINARY_REQUIRED_VARIABLES.items()
    if not variable_value
]


if missing_cloudinary_variables:
    missing_names = ", ".join(missing_cloudinary_variables)

    raise ValueError(
        f"متغيرات Cloudinary التالية غير موجودة: {missing_names}. "
        "أضفها داخل ملف .env محليًا أو داخل Environment في Render."
    )


# =========================================================
# أنظمة التخزين
# =========================================================

STORAGES = {
    # تخزين ملفات الميديا على Cloudinary
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage."
            "MediaCloudinaryStorage"
        ),
    },

    # ضغط وتقديم ملفات CSS وJavaScript والصور بواسطة WhiteNoise
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


MEDIA_URL = "/media/"


# =========================================================
# إعدادات الأمان للإنتاج
# =========================================================

if not DEBUG:
    # Render يرسل الطلبات من خلال Proxy
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_REFERRER_POLICY = "same-origin"


# =========================================================
# المفتاح الأساسي الافتراضي
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
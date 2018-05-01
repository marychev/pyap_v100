from .settings import os, BASE_DIR


PYAP_INSTALLED_APPS = [
    'filebrowser',
    'admin_menu',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'mptt',
    'ckeditor',
    'ckeditor_uploader',
    'daterange_filter',

    # --modules
    'cart',
    'search',
    'utils',
    # --apps
    'advertising',
    'blog',
    'markdown_deux',
    'gallery',
    'catalog',
    'product',
    'order',
    'users',
    'home',
    'menu',
    'page',
    'site_info',
    'settings_template',
    'include_area',
    'dev_init',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'pyap', 'static'),
    os.path.join(BASE_DIR, '..', 'app', 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'theme', 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)
# COMPRESS_ENABLED = True
# COMPRESS_PRECOMPILERS = (
#     ('text/stylus', 'stylus -u nib < {infile} > {outfile}'),
# )


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'theme', 'media')


FILEBROWSER_DIRECTORY = ''
DIRECTORY = ''
MAX_UPLOAD_SIZE = 60485760
FILEBROWSER_MAX_UPLOAD_SIZE = MAX_UPLOAD_SIZE
FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': 'Small (2 col)', 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (4col )', 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (6 col)', 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (8 col)', 'width': 680, 'height': '', 'opts': ''},
    'max': {'verbose_name': 'Max (12 col)', 'width': 1600, 'height': '', 'opts': ''},
}
FILEBROWSER_ADMIN_VERSIONS = ['thumbnail', 'small', 'medium', 'big', 'large', 'max']
FILEBROWSER_ADMIN_THUMBNAIL = 'admin_thumbnail'


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
}
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_RESTRICT_BY_DATE = True


SITE_ID = 1

LOGIN_URL = '/users/login/'

CART_SESSION_ID = 'cart'

# APPEND_SLASH = False


# django menu style
ADMIN_STYLE = {
    'primary-color': '#1f2735',
    'secondary-color': '#344256',
    'tertiary-color': '#3a4860',
    # 'background': 'white',
    'primary-text': '#fff',
    # 'secondary-text': 'white',
    'tertiary-text': '#fff',
    'breadcrumb-color': '#b6d0ff',
    'breadcrumb-text': '#34d5ff',
    'focus-color': '#e4edff',
    # 'focus-text': '#45ffe8 ',
    'primary-button': '#23d5ff',
    # 'primary-button-text': 'red',
    'secondary-button': '#4d7fda',
    # 'secondary-button-text': 'red',
    'link-color': '#005f77',  # '#447e9b',
    # 'link-color-hover': 'lighten($link-color, 20%)'
}
ADMIN_LOGO = 'img/pyap_logo.png'

# AUTH_USER_MODEL = 'users.models'

TEMPLATE_DEBUG = False

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'marychev@garpix.com'
EMAIL_HOST_PASSWORD = 'garpix_81086'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = EMAIL_HOST_USER
# # --- DURUNG DEVELOPMENT ONLY ---
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# # ------------------------------------------------------------------

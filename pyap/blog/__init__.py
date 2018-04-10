VERSION = (0, 2, 1)
default_app_config = 'blog.apps.BlogAppConfig'


def get_version():
    """Return the Django Simple Blog version as a string."""
    return '.'.join(map(str, VERSION))

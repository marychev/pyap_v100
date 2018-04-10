"""FOR JOB'S with Email """
from django.conf import settings
from django.core.validators import validate_email, ValidationError
from django.core.mail import EmailMultiAlternatives


SITE_URL = settings.SITE_URL
SITE_NAME = 'my-site.ru'


def send_html_email(to_email, from_email=settings.EMAIL_HOST_USER, subject=None, html=None):
    """Отправка 1го письма пол-лю (HTML)"""

    validate_email(from_email)
    validate_email(to_email)

    if not subject:
        subject = 'Вам письмо! от "%s"' % from_email

    if not html:
        html = subject + '\r\n'

    try:
        msg = EmailMultiAlternatives(subject, html, from_email, [to_email])
        msg.attach_alternative(html, "text/html")
        return msg.send()
    except ValidationError:
        raise ('|x_x|: Ошибка при отправке `Email`a|\n\t %s|%s|%s' % (subject, from_email, to_email))


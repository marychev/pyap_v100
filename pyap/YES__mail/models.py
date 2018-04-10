from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from garpix.helpers import CreatedUpdatedModel
from order.models import Order
from users.models import CustomUser
from coupon.models import Coupon


HELP_HTML = """
<h5>Параметры для шаблона: <small>[!] Не действуют для `Индивидуального шаблона`</small></h5>
Заказ <br>
`````````````````````````````<br>
<code>{{ order.id }}</code> - Номер заказа<br>
<code>{{ order.email_sender }}</code> - Email клиента, оформленного заказа<br>
<code>{{ order.get_payment_method }}</code> - Способ оплаты<br>
<code>{{ order.get_type_delivery }}</code> - Доставки или самовывоз<br>
<code>{{ order.shipping_address }}</code> - Адрес доставки<br>
<code>{{ order.get_fast_or_full }}</code> - Какой заказ: быстрый или полный<br>
<code>{{ order.get_status_display }}</code> - Что ожидает/статус заказа: подтвердить (статус подтвержден?), ожидает оплаты<br>
<code>{{ order.phone_sender }}</code> - Телефон клиента.<br>
<code>{{ order.get_link_user }}</code> - Ссылка на заказ<br>
<code>{{ order.get_used_coupons }}</code> - "Купон", если не использовался выдавать "Не использовался"<br>
<code>{{ order.get_table }}</code> - Таблица заказа.<br> 
<code>{{ order.total_price }}</code> - Общая стоимость заказа (Итоговая цена)<br>
<code>{{ order.clean_total_price }}</code> - Общая стоимость заказа (только за товары)<br><br>
Получатель (пользователь)<br>
`````````````````````````````<br>
<code>{{ user.email }}</code> - Емайл пользователя<br>
<code>{{ user.get_full_name }}</code> - Фамилие и Имя пользователя<br>
<code>{{ user.get_link_confirm_email }}</code> - Ссылка для отправки пароля пользователю<br>
<small>https://dev.fl-ag.ru/user/confirm/NKD0XU5B68G044ZR6E65FU807AT951GPKL7DSSM5P813XJ0S30RDN738DRDH2NTE/</small><br>
<code>{{ user.get_default_token_generator }}</code> - default_token_generator
Купон<br>
`````````````````````````````<br>
<code>{{ coupon.code }}</code> - Служебное название выпуска купонов<br>
<code>{{ coupon.content }}</code> - Текст описания сути акции на купоне<br>
<code>{{ coupon.email_friend }}</code> - Емайл друга<br>
<code>{{ coupon.get_method_create_display }}</code> - Метод создания<br>
<code>{{ coupon.discount }}</code> - Размер скидки(руб)<br>
<code>{{ coupon.url }}</code> - Ссылка на подробные условия акции<br>
<code>{{ coupon.time_action }}</code> - Время действия [минут]<br>
<code>{{ coupon.date_end }}</code> - Действие купона до<br>
<code>{{ coupon.date_create }}</code> - Дата создания<br>
<code>{{ coupon.get_data_end }}</code> - Дата окончания действия купона<br>
<code>{{ coupon.mail_description }}</code> - Маркетинговый текст купона (для событий/напоминаний), заполняется в автогенерациях купона.<br>
"""


class HTMLTemplate(models.Model):
    """
    Емайл сообщения. Шаблон/ХТМЛ/ для эл.писем.
        # Пример:
        # Отправить письма: Новый заказ[2]
        HTMLTemplate.sent_mail(event_choice=HTMLTemplate.ORDER_CREATE_CHOICE, order=order, user=order.user)
    """

    DEFAULT_CHOICE = 'Custom'
    ORDER_CREATE_CHOICE = 'OrderCreate'
    ORDER_READY_CHOICE = 'OrderReady'
    ORDER_PAYMENT_CHOICE = 'OrderPayment'
    USER_REGISTER_CHOICE = 'UserRegister'
    USER_CONFIRM_EMAIL_CHOICE = 'UserConfirmEmail'
    USER_PASSWORD_RESET_CHOICE = 'UserPasswordReset'
    COUPON_GIVE_CHOICE = 'CouponGive'
    COUPON_FRIEND_CHOICE = 'CouponFriend'

    EVENT_CHOICES = (
        (DEFAULT_CHOICE, '*Индивидульно'),
        (ORDER_CREATE_CHOICE,   '`Заказ` Сделан'),
        (ORDER_READY_CHOICE,    '`Заказ` Выполнен'),
        (ORDER_PAYMENT_CHOICE,  '`Заказ` Оплачен'),
        (USER_REGISTER_CHOICE,          '`Пользователь`. Регистрация'),
        (USER_CONFIRM_EMAIL_CHOICE,     '`Пользователь`. Подтверждение E-mail'),
        (USER_PASSWORD_RESET_CHOICE,    '`Пользователь`. Сброс пароля'),
        (COUPON_GIVE_CHOICE,    '`Купон`. Создание купона'),
        (COUPON_FRIEND_CHOICE,  '`Купон`. Подарочный купон другу'),
    )

    subject = models.CharField(max_length=255, verbose_name='Заголовок', db_index=True)
    # from_email = models.EmailField(
    #     verbose_name='`Email` отправитьелья', default=settings.EMAIL_HOST_USER,
    #     help_text='*По умолчанию: {0}' .format(settings.EMAIL_HOST_USER))
    to_email = models.EmailField(
        verbose_name='`Email` получателя', blank=True, null=True,
        help_text='Определяется автоматически, если событие не *Индивидуально')
    is_admin = models.BooleanField(default=False, verbose_name='Письмо админу', help_text='*Письмо для Администратора.')
    event = models.CharField(
        max_length=20, choices=EVENT_CHOICES, default=DEFAULT_CHOICE, verbose_name='Событие',
        help_text='*В зависимости от события опрелеяются необходимые модели|Order|User|')
    html = RichTextUploadingField(verbose_name="Шаблон-HTML", help_text=HELP_HTML)

    def __str__(self):
        string = self.get_event_display()
        whom = ': Пол-ль'
        if self.is_admin:
            whom = ': Админ'
        return string + whom

    def make_html(self, order=None, user=None, coupon=None):
        """Вернуть заполненый HTML объектами"""
        from django.template import Template, Context
        template = Template(self.html)
        c = Context({'order': order, 'user': user, 'coupon': coupon})
        return template.render(c)

    def sent(self, order=None, user=None, coupon=None, to_email=None):
        """ Отправить Email's. Создается ХТМЛ Шаблон. С заполненными параметрами (если нужно)"""
        from utils.mail import send_html_email
        from des.models import DynamicEmailConfiguration
        des_config = DynamicEmailConfiguration.get_solo()

        html = self.make_html(order=order, user=user, coupon=coupon)

        from_email = des_config.from_email

        # если передан емалй получателья - используется он
        # иначе выполняется ряд условий
        if not to_email:
            to_email = user.email if user else self.to_email
            if self.is_admin:
                to_email = from_email
            elif not to_email:
                to_email = order.email_sender

        sent = SentLetter(html_template=self, order=order, user=user, coupon=coupon, html=html)
        if send_html_email(to_email=to_email, from_email=from_email, subject=self.subject, html=html):
            sent.is_sent = True
        return sent.save()

    @staticmethod
    def sent_mail(event_choice, order=None, user=None, coupon=None, to_email=None):
        """
        Отправить письма и Админу и Клиенту.
        Определяет какой шаблон выбрать по переданному событию.
        :param event_choice:
        :param order:
        :param user:
        :param coupon:
        :param to_email: - если заполненно - письмо будет отправленно этому адресату
        """
        admin_template = HTMLTemplate.objects.filter(event=event_choice, is_admin=True).first()
        user_template = HTMLTemplate.objects.filter(event=event_choice, is_admin=False).first()
        if admin_template:
            admin_template.sent(order=order, user=user, coupon=coupon, to_email=to_email)
        if user_template:
            user_template.sent(order=order, user=user, coupon=coupon, to_email=to_email)

    class Meta:
        unique_together = ('subject', 'is_admin', 'event')
        verbose_name = 'Письмо'
        verbose_name_plural = ' Письма'


class SentLetter(CreatedUpdatedModel):
    """Отправленные письма"""
    order = models.ForeignKey(Order, blank=True, null=True, verbose_name='Заказ')
    user = models.ForeignKey(CustomUser, blank=True, null=True, verbose_name='Получатель')
    coupon = models.ForeignKey(Coupon, blank=True, null=True, verbose_name='Купоны')
    html_template = models.ForeignKey(HTMLTemplate, verbose_name='Шаблон')
    html = models.TextField(verbose_name='HTML письма', default='...')
    is_sent = models.BooleanField(default=False, verbose_name='Отправлено')

    class Meta:
        verbose_name = 'Отправленное письмо'
        verbose_name_plural = 'Отправленные письма'


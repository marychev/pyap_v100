from __future__ import unicode_literals
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from utils.abstract_model import CreatedUpdatedModel
from users.models import User
from product.models import ProductItem


MSG_PRODUCT_PRICE_CHANGE = '[*]Цена изменена. Товар:`{}` {} x {} = {} p'
MSG_PRODUCT_QTY_CHANGE = '[*]Кол-во изменено. Товар:`{}` {} x {} = {} p'
MSG_PRODUCT_ADD = '[+]Добавлен товар `{}` {} x {} = {} p'
MSG_PRODUCT_DELETE = '[-]Удален товар `{}` {} x {} = {} p'


class Status(models.Model):
    """Модель Статусы заказов"""

    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Order(CreatedUpdatedModel):
    """Модель заказа."""

    user = models.ForeignKey(User, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Адрес', max_length=250)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', null=True, blank=True)
    total_cost = models.DecimalField(
        verbose_name='Общая стоимость', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))],
        help_text=' Автоматический расчет при сохранении.')
    status = models.ForeignKey(Status, verbose_name='Статус заказа', null=True)
    ttn = models.CharField('Товарно-транспортная накладная', blank=True, null=True, max_length=128)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_user_full_name(self):
        """Полное ФИО грузополучателя. Может отличаться от того, кто делает заказ"""
        full_name = '%s %s' % (self.last_name, self.first_name)
        if (self.first_name in self.user.first_name) and (self.last_name in self.user.last_name):
            full_name = self.user.get_full_name()
        return full_name

    def get_total_qty(self):
        """Общее кол-во заказанных товаров"""
        return sum(item.quantity for item in self.orderitem_set.all())

    def get_total_cost(self):
        """Получить общую стоимость(все варианты позиций в заказе)"""
        return sum(item.get_cost() for item in self.orderitem_set.all())

    def save(self, *args, **kwargs):
        # # Обрабатывается при втором и последующих обновлений заказа
        if not self.total_cost:
            self.total_cost = self.get_total_cost()
        if self.id:
            Story.create_or_update(order=self)

        super(Order, self).save(*args, *kwargs)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created', )


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'пункт заказа'
        verbose_name_plural = 'пункты заказа'

    order = models.ForeignKey(Order, verbose_name='Заказ')  # related_name='items',
    product_item = models.ForeignKey(ProductItem, verbose_name='Вариант товара')  # related_name='order_items'
    price = models.DecimalField(
        verbose_name='Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    quantity = models.PositiveSmallIntegerField(verbose_name='Кол-во', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        """Получить стоимость заказанной позиции"""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        """
        При изменении данных пункта в может измениться общая сумма заказа
        1. При добавление/ удалении товара
        2. При изменении кол-ва / цены товара
        """
        try:
            old_obj = OrderItem.objects.get(id=self.id)
        except OrderItem.DoesNotExist:
            old_obj = self

        old_qty = old_obj.quantity
        old_count_items = self.order.orderitem_set.count()

        super(OrderItem, self).save(*args, **kwargs)

        current_count_items = self.order.orderitem_set.count()
        current_qty = self.quantity

        # изменении цены товара
        if old_obj.price != self.price:
            message = MSG_PRODUCT_PRICE_CHANGE.format(
                self.product_item, self.price, self.quantity, self.get_cost())
            Story.create_or_update(self.order, message)

        # изменение кол-ва у варианта товара
        if current_qty != old_qty:
            message = MSG_PRODUCT_QTY_CHANGE.format(
                self.product_item, self.price, self.quantity, self.get_cost())
            Story.create_or_update(self.order, message)

        # добавление нового варианта товара
        if old_count_items < current_count_items:
            message = MSG_PRODUCT_ADD.format(
                self.product_item, self.price, self.quantity, self.get_cost())
            Story.create_or_update(self.order, message)

        # заново сохранить заказ, т.к. данные изменены
        self.order.save()

    def delete(self, *args, **kwargs):
        old_count_items = self.order.orderitem_set.count()
        super(OrderItem, self).delete(*args, **kwargs)
        current_count_items = self.order.orderitem_set.count()

        # удаление варианта товара
        if old_count_items > current_count_items:
            message = MSG_PRODUCT_DELETE.format(
                self.product_item, self.price, self.quantity, self.get_cost())
            Story.create_or_update(self.order, message)

        # заново сохранить заказ, т.к. данные изменены
        self.order.save()


class Story(CreatedUpdatedModel):
    """
    Модель содержит Историю жизни заказа.
    *Сохраняет историю заказа о выполненых действиях.
    *Отслеживает изменение стоимости заказа на каждом этапе.
    """
    order = models.ForeignKey(Order, verbose_name='Заказ')
    status = models.ForeignKey(Status, null=True, verbose_name='Статус заказа')
    total_cost = models.DecimalField(
        verbose_name='Общая стоимость', max_digits=10, decimal_places=2,
        default=0, validators=[MinValueValidator(Decimal('0'))])
    comment = models.TextField(verbose_name='Комментарий', null=True)

    def __str__(self):
        return str(self.order)

    @staticmethod
    def create_or_update(order, message=''):
        """
        Создание / Обновлние Истории жизни заказа.
        Создать новый, если `заказ, статус и общая цена` уникальны, иначе обновить данные
        """
        order.total_cost = order.get_total_cost()
        story, is_created = Story.objects.get_or_create(
            order_id=order.id, status=order.status, total_cost=order.total_cost,
            defaults={
                'comment': message,
                'status': order.status,
                'total_cost': order.total_cost
            })

        # обновление существующего пункта истории
        br = '\r' if message else ''
        if not is_created:
            story.comment += br + message
            story.status = order.status
            story.total_cost = order.total_cost
            story.save(update_fields=('comment', 'status', 'total_cost'))

    class Meta:
        unique_together = ('order', 'status', 'total_cost')
        verbose_name = 'Историю'
        verbose_name_plural = 'История'

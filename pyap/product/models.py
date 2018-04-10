from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from catalog.models import Catalog
from utils.abstract_model import ABSContentModel, CreatedUpdatedModel, ABSImageModel, ABSCommentModel
from utils.translit_field import translaton_field
# from django.db.models.signals import post_save
# from .signals import save_product_comment


class Product(ABSContentModel):
    """
    Модель главного товара
    """
    articul = models.CharField(max_length=256, verbose_name='Артикул (уник)', unique=True, blank=True, null=True)
    catalog = models.ManyToManyField(Catalog, blank=True, verbose_name='Категории')
    is_bestseller = models.BooleanField(default=False, verbose_name='Хит продаж')
    is_new = models.BooleanField(default=True, verbose_name='Новинка')
    recommend_products = models.ManyToManyField(
        'self', verbose_name='Рекомендованные/Похожие', blank=True, limit_choices_to={'is_show': True},
        help_text='Отображаются внизу карточки товара, как рекомендованные или похожие товары')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # не отображать, если клонированный объект
        if 'CLONE' in self.title or 'CLONE' in self.slug:
            self.is_show = False
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаление объекта и связаных с ним изображений"""
        if ProductImage.objects.filter(product=self).first():
            [image.delete() for image in ProductImage.objects.filter(product=self)]
        if self.image:
            self.image.delete()
        super(Product, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        catalog_slug = '#'
        if self.catalog.first():
            catalog_slug = self.catalog.first().slug
            return reverse('product:product-detail', args=[catalog_slug, self.slug])
        else:
            return catalog_slug

    def get_main_item(self):
        """
        Получить главный вариант товара. 
        Если среди вариантов нет главного, выберет первый из всех вариантов
        """
        return ProductItem.objects.filter(product_id=self.id, is_main=True).first() or self.productitem_set.first()

    def get_price(self):
        price = 0
        if self.get_main_item():
            price = Decimal(self.get_main_item().price)
        return price

    def get_price_discount(self):
        price = 0
        if self.get_main_item():
            price = Decimal(self.get_main_item().price_discount)
        return price

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = ProductImage.objects.filter(product_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return ProductImage.objects.filter(product_id=self.id)
    # -----------------------------------------------------------------------------------

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        unique_together = ('title', 'slug')


class ProductImage(ABSImageModel):
    """Дополнительное изображние к товару"""
    product = models.ForeignKey(Product, verbose_name='Товар')

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.set_image_title(obj=self.product)
        super(ProductImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'


class ProductItem(CreatedUpdatedModel):
    """Варианты товара"""
    product = models.ForeignKey(Product, verbose_name='Главный товар')
    name = models.CharField(max_length=256, verbose_name='Наименование', help_text='Прим:размерный ряд')
    articul = models.CharField(max_length=256, verbose_name='Артикул (уникальный)', blank=True, null=True, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена', default=0,
        validators=[MinValueValidator(Decimal('0'))])
    price_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Акционная цена', help_text='Если указана - станет ценой продажи товара.')
    price_purchase = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена закупки', default=0,
        validators=[MinValueValidator(Decimal('0'))])
    quantity = models.IntegerField(verbose_name='Кол-во', default=0)
    is_main = models.BooleanField(default=False, verbose_name='Главный')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_main()
        if self.price_discount and not self.price:
            self.price = self.price_discount
        if not self.articul and self.name:
            self.articul = translaton_field(self.name)
        super(ProductItem, self).save(*args, **kwargs)

    def get_absolute_url(self):
        catalog_slug = '#'
        if self.product.catalog.first():
            catalog_slug = self.product.catalog.first().slug
            return reverse('product:product-detail', args=[catalog_slug, self.product.slug])
        else:
            return catalog_slug

    # ------------ SETTER HELPER -------------
    def set_main(self):
        """
        Установить вариант товара Главым
        главных товаров не может быть много. Он один!
        """
        if self.product.productitem_set.filter(is_main=True).count() >= 1:
            self.is_main = False
        elif self.product.productitem_set.filter(is_main=True).count() == 0:
            self.is_main = True

    def get_price(self):
        return self.price

    class Meta:
        unique_together = ('product', 'name')
        ordering = ('product', '-is_main', 'name')
        verbose_name = 'Вариант продукта'
        verbose_name_plural = 'Варианты продукта'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProductComment(ABSCommentModel):
    """
    Коментарии к продукту, товару
    """
    product = models.ForeignKey(Product, verbose_name='Товар', null=True, on_delete=models.SET_NULL)

#
# post_save.connect(save_product_comment, sender=ProductComment)
#

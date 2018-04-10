# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from product.models import ProductItem


class Cart(object):
    """Управление корзиной"""
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})

    def __iter__(self):
        """Итерация по товарам"""
        product_ids = self.cart.keys()
        products = ProductItem.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Кол-во товаров"""
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, is_update_qty=False):
        """Добавить товар в корзину"""
        product_id = str(product.id)
        price = product.price_discount if product.price_discount and (product.price_discount > 0) else product.price

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(price)}
        self.cart[product_id]['quantity'] = quantity if is_update_qty else self.cart[product_id]['quantity'] + quantity
        self.save()

    def edit(self, product, quantity=0):
        """обновить кол-во товара в корзине"""
        product_id = str(product.id)
        self.cart[product_id]['quantity'] = quantity
        if quantity < 1:
            self.remove(product)
        self.save()

    def save(self):
        """Сохранить данные в сессию"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """Удалить продукт из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """Получить полную стоимость товаров"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистить сессию"""
        try:
            del self.session[settings.CART_SESSION_ID]
        except KeyError:
            pass
        self.session.modified = True

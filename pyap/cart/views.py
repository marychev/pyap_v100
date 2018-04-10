from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from product.models import ProductItem, Product
from . cart import Cart
from . forms import CartAddProductForm
from generic.mixins import MainPageMixin
import json


class CartDetail(MainPageMixin, TemplateView):
    """
    Страница корзины
    """
    template_name = 'cart/templates/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        for item in context['cart']:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'is_update': True})
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Обновить товары в корзине - Ajax"""
        product = ProductItem.objects.get(id=request.POST.get('product_id', 0))
        price = product.price_discount if product.price_discount > 0 else product.price
        response_data = {
            'product_id': product.id,
            'price': float(price),
            'total_price_product': int(request.POST.get('quantity', 0)) * float(price)
        }

        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.edit(product=product, quantity=cd['quantity'])
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def cart_remove(request, product_id):
    """Удаление товар"""
    cart = Cart(request)
    product = get_object_or_404(ProductItem, id=product_id)
    cart.remove(product)
    return redirect('cart:cart-detail')


def cart_clear(request):
    """Очистить корзину полностью"""
    Cart(request).clear()
    return redirect('cart:cart-detail')


# ------------------------------------
#           дополнительные методы
# ====================================
def basket_add(request):
    """
    Добавить товар/ы в корзину. -  для методов Ajax -
    :return {json}: объект для JS - json.dump
    """
    # одиночный товар или у товара есть позиции для выбора
    obj = ProductItem.objects.get(id=int(request.POST['product_id']))

    # Сформировать данные для ответа клиенту
    response_data = {
        'product_id': obj.id,
        'name': obj.name,
        'articul': obj.articul,
        'quantity': int(request.POST.get('quantity', 1)),
    }
    json_response = json.dumps(response_data)

    # Добавить товары в корзину
    form = CartAddProductForm(request.POST)
    cart = Cart(request)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=obj, quantity=cd['quantity'], is_update_qty=cd['is_update'])
        return json_response


@csrf_exempt
def add_to_cart(request):
    """Ajax метод, для добавления в корзину"""
    return HttpResponse(basket_add(request), content_type="application/json")

# ====================================================================================


from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from generic.mixins import MainPageMixin
from cart.cart import Cart
from catalog.models import Catalog
from cart.forms import CartAddProductForm
from utils.next_prev_obj import get_next_prev
from utils.leftbar import get_leftbar
from django.shortcuts import redirect
from django.contrib import messages
from .models import Product, ProductItem, ProductComment
from .forms import CommentForm

import json


class ProductDetail(MainPageMixin, TemplateView):
    template_name = 'product/templates/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, slug=kwargs['product'])

        initial = {
            'obj': context['product'],
            'request': self.request,
        }
        comment_form = CommentForm(initial=initial)

        context['comment_form'] = comment_form
        context['review_products'] = ProductComment.objects.filter(
            is_show=True, product_id=context['product'].id)
        context['catalog'] = get_object_or_404(Catalog, slug=kwargs['catalog'])
        context['cart_product_form'] = CartAddProductForm()
        context['next_prev'] = get_next_prev(Product, context['product'])
        context['leftbar'] = get_leftbar(Catalog, context['catalog'])

        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Добавить товар в корзину на странице - карточка товара - Ajax"""
        obj = ProductItem.objects.get(id=request.POST['product_id'])

        response_data = {
            'product_id': obj.id,
            'name': obj.name,
            'articul': obj.articul,
            'quantity': int(request.POST.get('quantity', 0)),
            'price': float(obj.price)
        }

        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=obj, quantity=cd['quantity'], is_update_qty=cd['is_update'])

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    @staticmethod
    def get_context_for_catalog(context):
        """
        Попадая на страницу какатога, если ее нет - перейти на страницу товара
        Todo: заглушка
        """
        context['template_name'] = 'product_detail.html'
        context['product'] = get_object_or_404(Product, slug=context['slug'])

        initial = {
            'obj': context['product'],
            'request': context['request'],
        }
        comment_form = CommentForm(initial=initial)

        context['comment_form'] = comment_form
        context['review_products'] = ProductComment.objects.filter(is_show=True, product_id=context['product'].id)
        context['catalog'] = context['product'].catalog.first()
        context['cart_product_form'] = CartAddProductForm()
        context['next_prev'] = get_next_prev(Product, context['product'])
        context['leftbar'] = get_leftbar(Catalog, context['catalog'])
        return context


class ProductCommentView(MainPageMixin, TemplateView):
    """
    Отзыв к товару
    """
    form_class = CommentForm
    model = ProductComment
    template_name = 'product/templates/product_detail.html'

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Product, id=request.POST.get('product'))
        review_form = CommentForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, ':) Спасибо! Отзыв принят.')
        else:
            messages.error(request, '(: Произошла ошибка при отправке отзыва.')
        return redirect(obj.get_absolute_url())
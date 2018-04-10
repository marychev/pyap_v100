from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from generic.mixins import MainPageMixin
from utils.pagination import get_pagination
from utils.leftbar import get_leftbar
from catalog.models import Catalog
from product.models import Product, ProductItem
from product.views import ProductDetail
import json


def sort_by_params(request, object_list):
    """
    Сортировка по GET параметрам запрса
    """
    # новинки
    is_new = request.GET.get('is_new', '')
    if is_new:
        object_list = object_list.order_by(is_new)

    # по цене
    price = request.GET.get('price', '')
    if price:
        reverse = True if request.GET.get('price')[:1] == '-' else False
        object_list = list(object_list)
        object_list.sort(key=lambda o: o.get_price(), reverse=reverse)

    return object_list


class CatalogView(MainPageMixin, TemplateView):
    """Каталог"""
    template_name = 'catalog/templates/catalog.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)
        try:
            context['object'] = Catalog.objects.get(slug=context['slug'], is_show=True)
            context['leftbar'] = get_leftbar(Catalog, context['object'])
            catalog_id = context['leftbar']['root_obj'].id
            context['current_mainmenu'] = context['mainmenu'].filter(
                catalog_id=catalog_id
            ).first()

            context['objects'] = Product.objects.filter(catalog=context['object'], is_show=True).order_by('-id')
            context['objects'] = sort_by_params(self.request, context['objects'])
            context['objects'] = get_pagination(self.request, context['objects'])
        except Catalog.DoesNotExist:
            # --- redirect in product  ---
            self.template_name = 'product/templates/product_detail.html'
            context = ProductDetail.get_context_for_catalog(context)
        return context

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Добавить товар в корзину на странице - карточка товара - Ajax"""
        # TODO: |[!]|: перенести в метод товара
        # одиночный товар или у товара есть позиции для выбора
        obj = ProductItem.objects.get(id=request.POST['product_id'])

        product_detail = ProductDetail()
        product_detail.post(request)

        response_data = {
            'product_id': obj.id,
            'name': obj.name,
            'articul': obj.articul,
            'quantity': int(request.POST.get('quantity', 0)),
            'price': float(obj.price)
        }

        return HttpResponse(json.dumps(response_data), content_type="application/json")




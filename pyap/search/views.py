from django.views.generic.base import TemplateView
from generic.mixins import MainPageMixin
from product.models import Product
from simple_search import search_form_factory
from utils.pagination import get_pagination


class Search(MainPageMixin, TemplateView):
    """Поиск по сайту. """
    template_name = 'search/search_result.html'

    def get_context_data(self, **kwargs):
        # todo: add to forms.py
        SearchForm = search_form_factory(
            Product.objects.filter(is_show=True), 
            ['title', 'articul',])

        context = super(Search, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', None)
        context['title'] = 'Поиск по запросу: `{}`'.format(context['q'])
        context['form'] = SearchForm(self.request.GET or {})
        context['objects'] = Product.objects.none()

        if context['form'].is_valid() and context['q']:
            context['objects'] = get_pagination(self.request, context['form'].get_queryset())
        return context

# ------------
# HELP search
# `````````````
# from simple_search import search_filter
# search_query = self.request.GET.get('q', '')
# if search_query:
#     search_fields = ['^title', 'description', '=id']
#     search_product = search_filter(search_fields, search_query)
#     context['products'] = Product.objects.filter(search_product)
#     return render(self.request, 'default/search_result.html',
#     context=context['products'])

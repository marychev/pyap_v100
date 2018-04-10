from django.conf.urls import url
from .views import CatalogView

# max 5 tree
urlpatterns = [
    url(r'^(?P<slug>[-_\w]+)/$', CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug>[_\-\w\d]+)/$', CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug_1>[_\-\w\d]+)/(?P<slug>[_\-\w\d]+)/$', CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug_2>[_\-\w\d]+)/(?P<slug_1>[_\-\w\d]+)/(?P<slug>[_\-\w\d]+)/$', CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug_3>[_\-\w\d]+)/(?P<slug_2>[_\-\w\d]+)/(?P<slug_1>[_\-\w\d]+)/(?P<slug>[_\-\w\d]+)/$',
    #     CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug_4>[_\-\w\d]+)/(?P<slug_3>[_\-\w\d]+)/(?P<slug_2>[_\-\w\d]+)/(?P<slug_1>[_\-\w\d]+)/'
    #     r'(?P<slug>[_\-\w\d]+)/$', CatalogView.as_view(), name='catalog'),
    # url(r'^(?P<slug_5>[_\-\w\d]+)/(?P<slug_4>[_\-\w\d]+)/(?P<slug_3>[_\-\w\d]+)/(?P<slug_2>[_\-\w\d]+)/'
    #     r'(?P<slug_1>[_\-\w\d]+)/(?P<slug>[_\-\w\d]+)/$', CatalogView.as_view(), name='catalog'),
]


# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import ProductDetail, ProductCommentView


urlpatterns = [
    url(r'^(?P<catalog>[_\-\w\d]+)/(?P<product>[_\-\w\d]+)/$', ProductDetail.as_view(), name='product-detail'),
    url(r'^comment/product/(?P<product_id>\d+)/$', ProductCommentView.as_view(), name='product_comment'),
]


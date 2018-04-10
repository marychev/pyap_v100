# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.CartDetail.as_view(), name='cart-detail'),
    url(r'^add/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart-remove'),
    url(r'^clear/$', views.cart_clear, name='cart_clear'),
]



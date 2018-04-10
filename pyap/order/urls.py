from django.conf.urls import url
from order.views import OrderCreate, OrderCreated


urlpatterns = [
    url(r'^create/$', OrderCreate.as_view(), name='order-create'),
    url(r'^(?P<pk>\d+)/created/$', OrderCreated.as_view(), name='order-created')
]

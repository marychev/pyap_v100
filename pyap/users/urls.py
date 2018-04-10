from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from users.views import Register, Login, logout_view, Profile, Orders, OrderDetail, ReviewProducts
# NewUserProfileView, EditUserProfileView,

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^profile/$', login_required(Profile.as_view()), name='profile'),
    url(r'^orders/$', login_required(Orders.as_view()), name='orders'),
    url(r'^review/products/$', login_required(ReviewProducts.as_view()), name='review_products'),
    url(r'^(?P<pk>\d+)/order/$', login_required(OrderDetail.as_view()), name='order_detail'),

    # url(r'^profile/new/$', NewUserProfileView.as_view(), name='profile_new'),
    # url(r'^profile/(?P<pk>\d+)/$', EditUserProfileView.as_view(), name='profile_edit'),
]

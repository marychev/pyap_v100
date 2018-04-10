from django.conf.urls import url
from home.views import HomePageView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
]

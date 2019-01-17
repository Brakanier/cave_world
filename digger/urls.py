from django.conf.urls import url

from . import views

app_name = 'digger'

urlpatterns = [
    url('', views.index, name='index'),
]
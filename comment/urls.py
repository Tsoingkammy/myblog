from django.conf.urls import url
from .views import *


app_name = 'comment'
urlpatterns = [
    url(r'^comment/article/(?P<article_pk>[0-9]+)/$', article_comment, name='article_comment'),
]
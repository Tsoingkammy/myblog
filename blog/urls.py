from django.conf.urls import url
from .views import *
from .feeds import AllArticlesRssFeed


app_name = 'blog'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', ArticleDetailView.as_view(), name='detail'),
    url(r'^articles/$', article_list, name='article_list'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagView.as_view(), name='tag'),
    url(r'^all/rss/$', AllArticlesRssFeed(), name='rss'),
]
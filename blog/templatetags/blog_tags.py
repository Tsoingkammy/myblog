from ..models import *
from django import template
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_articles_list(num=5):
    return Article.objects.all().order_by('-create_date')[:num]


@register.simple_tag
def archives():
    return Article.objects.dates('create_date', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)


@register.simple_tag
def get_tag_list():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)



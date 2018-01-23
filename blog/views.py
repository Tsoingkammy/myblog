from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
import markdown
from comment.forms import CommentForm
from django.views.generic import *
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number -3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last}
        return data


def about(request):
    return render(request, 'blog/about.html')


def article_list(request):
    return render(request, 'blog/full-width.html')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/single.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.has_views()
        return response

    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions={
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        })
        article.article_text = md.convert(article.article_text)
        article.toc = md.toc
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


def contact(request):
    return render(request, 'blog/contact.html')


class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(create_date__year=self.kwargs.get('year'),
                                                               create_date__month=self.kwargs.get('month')
                                                               ).order_by('-create_date')


class CategoryView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate).order_by('-create_date')


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag).order_by('-create_date')


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    article_list = Article.objects.filter(Q(title__icontains=q) | Q(article_text__icontains=q))
    return render(request, 'blog/index.html', {'article_list': article_list,
                                               'error_msg': error_msg})
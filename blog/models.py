from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    article_text = models.TextField()
    create_date = models.DateTimeField('create_date')
    modified_date = models.DateTimeField(auto_now=True)
    excerpt = models.CharField(max_length=54, blank=True)
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def has_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                               'markdown.extensions.codehilite'])
            self.excerpt = strip_tags(md.convert(self.article_text))[:50]

        super(Article, self).save(*args, **kwargs)

    class Meta:
            ordering = ['-create_date']

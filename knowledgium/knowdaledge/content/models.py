from django.db import models
from django.core.urlresolvers import reverse


class Content(models.Model):

    author = models.ForeignKey('coder.Coder', related_name='content')
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=300)
    title = models.CharField(max_length=80)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', related_name='content', null=True)

    def __unicode__(self):
        return '{0]-{1}-{2}'.format(self.created, self.author, self.title)

    def get_absolute_url(self):
        return reverse('content_detail', args=[self.pk])


class Category(models.Model):

    title = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.title

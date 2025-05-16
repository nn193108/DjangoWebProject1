"""
Definition of models.
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    pub_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"
        ordering = ['-pub_date']

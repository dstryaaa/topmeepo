from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField('title', max_length=50)
    content = models.TextField('content', null=True, blank=True)
    published = models.DateTimeField('published', auto_now_add=True, db_index=True)
    username = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']

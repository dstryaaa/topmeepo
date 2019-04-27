from django.db import models
from django.contrib.auth.models import User
import secretballot


class Post(models.Model):
    title = models.CharField('title', max_length=50)
    content = models.TextField('content', null=True, blank=True)
    published = models.DateTimeField('published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']


class Likes(models.Model):
    post_id = models.CharField('vote_id', max_length=200)
    like_count = models.PositiveIntegerField('like_id', default=0)
    author = models.CharField('author_id', max_length=200)


class Bio(models.Model):
    biogr = models.TextField('biogr', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

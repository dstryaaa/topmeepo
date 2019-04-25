from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    title = models.CharField('title', max_length=50)
    content = models.TextField('content', null=True, blank=True)
    published = models.DateTimeField('published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.content

    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']


class Bio(models.Model):
    biogr = models.TextField('biogr', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

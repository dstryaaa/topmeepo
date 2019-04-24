from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    # Лайки и дислайки плюсуются и минусуются на один
    like = 1
    dislike = -1
    # Какие мнения есть
    votes = ((dislike, 'Не нравится'), (like, 'Нравится'))
    vote = models.SmallIntegerField(verbose_name=("Мнение"), choices=votes)
    # Какой юзер делает
    user = models.ForeignKey(User, verbose_name=("Юзер"), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # Поле для связи
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()


class Post(models.Model):
    title = models.CharField('title', max_length=50)
    content = models.TextField('content', null=True, blank=True)
    published = models.DateTimeField('published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = GenericRelation(LikeDislike, related_query_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published']


class Bio(models.Model):
    biogr = models.TextField('biogr', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

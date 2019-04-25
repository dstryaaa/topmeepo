from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like


User = get_user_model()


def add_like(obj, user):
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE), берет тип контента, можно
    # узнать через контрл
    obj_type = ContentType.objects.get_for_model(obj)
    # берет или создает лайк, делает запись в бд модель Like, или возвращает его
    # обрати внимание на is_created, это bool
    like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user):
    # опять же, берет тип контента
    obj_type = ContentType.objects.get_for_model(obj)
    # через фильтр удаляет, идет проверка на тип объекта(фигурируют app_label, class name), дальше айдишник и юзер
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user).delete()


def is_fan(obj, user):
    # посылает, если неаутентифицирован
    if not user.is_authenticated:
        return False
    # опять берем тип
    obj_type = ContentType.objects.get_for_model(obj)
    # опять выборку делаем
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
    # возвращаем лайки, которые есть
    return likes.exists()


def get_fans(obj):
    # см. выше
    obj_type = ContentType.objects.get_for_model(obj)
    # возвращает уже юзером по фильтру
    return User.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)

#from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
import json
#from django.template import loader
from django.shortcuts import render
from .forms import PostForm, BioForm
from .models import Post, Bio, LikeDislike
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.contrib import admin
from django.views import View
from django.contrib.contenttypes.models import ContentType


# Аккаунт пользователя
# Интересный факт: если сюда не поставить user_id, то выдаст ошибку


def index(request, user_id):
    if request.user.id != user_id:
        posts = Post.objects.filter(author=user_id)
        bios = Bio.objexts.filter(author=user_id)
        return render(request, 'first/feed.html', {'posts': posts, 'bios': bios})
    if request.method == 'POST':
        postform = PostForm(request.POST)
        post = postform.save(commit=False)
        post.author = request.user
        post.save()
        postform.save()
        bioform = BioForm(request.POST)
        bio = bioform.save(commit=False)
        bio.author = request.user
        bio.save()
        bioform.save()
    bioform = BioForm()
    postform = PostForm()
    bios = Bio.objects.filter(author=request.user)
    posts = Post.objects.filter(author=request.user)
    return render(request, 'first/index.html', {'posts': posts, 'postform': postform, 'bios': bios, 'bioform': bioform}, )


class Vote(View):
    model = None  # Модель данных - Статьи или Комментарии, в будущем
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        # Берем объект
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            # Берем инфу об объекте
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                                  object_id=obj.id,
                                                  user=request.user)
            # .воут получает тип лайка, сохраняет его, смотри урлы
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                # лайк уже доставлен
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            # ставим в первый раз
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )
# ЗАВТРА ДОПИШУ АЯКС ЗАПРОСЫ

def kek(request):
    return HttpResponse('НЕПРАВИЛЬНО')


# Общий фид
def feed(request):
    posts = Post.objects.order_by('-published')
    return render(request, 'first/feed.html', {'posts': posts,})


# Регистрация
class Signup(FormView):
    form_class = UserCreationForm
    success_url = "../feed/"
    template_name = "first/signup.html"

    def form_valid(self, form):
        form.save()
        return super(Signup, self).form_valid(form)


# Логинка, надо обработать index
class Login(FormView):
    form_class = AuthenticationForm
    template_name = "first/login.html"
    success_url = "../feed/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(Login, self).form_valid(form)


# Логаут
class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("../feed/")

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from .forms import PostForm, BioForm
from .models import Post, Bio, Likes
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View


def index(request, user_id):
    if request.user.id != user_id:
        posts = Post.objects.filter(author=user_id)
        bios = Bio.objects.filter(author=user_id)
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


def like(request, post_id):
    author = User(id=request.user.id)
    post = Post(id=post_id)

    like_create = Likes.objects.create(post=post, author=author)
    like_create.save()

    return HttpResponse('meh')


def kek(request):
    return HttpResponse('НЕПРАВИЛЬНО')


def add_vote(request, object_id):
    id = object_id
    author = request.user.id
    try:
        like = Likes.objects.get(pk=object_id)
        if request.user.id != like.author:
            like.post_id = id
            like.like_count += 1
            like.author = author
            like.save()
            return HttpResponseRedirect('../../feed/')
        else:
            return HttpResponse('Вы голосовали')
    except Likes.DoesNotExist:
        Likes.objects.create(pk=object_id)
        like = Likes.objects.get(pk=object_id)
        like.post_id = id
        like.like_count += 1
        like.author = author
        like.save()
        return HttpResponse('Успешно!')


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

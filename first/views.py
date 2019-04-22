#from django.shortcuts import render
from django.http import HttpResponseRedirect
#from django.template import loader
from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('../login/')
    if request.method == 'POST':
        postform = PostForm(request.POST)
        postform.save()
    postform = PostForm()
    posts = Post.objects.order_by('-published')
    return render(request, 'first/index.html', {'posts': posts, 'postform': postform})


def feed(request):
    posts = Post.objects.order_by('-published')
    return render(request, 'first/feed.html', {'posts': posts,})


class Signup(FormView):
    form_class = UserCreationForm
    success_url = "../first"
    template_name = "first/signup.html"

    def form_valid(self, form):
        form.save()
        return super(Signup, self).form_valid(form)


class Login(FormView):
    form_class = AuthenticationForm
    template_name = "first/login.html"
    success_url = "first/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(Login, self).form_valid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("../feed/")

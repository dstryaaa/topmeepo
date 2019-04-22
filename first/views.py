#from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
from .forms import PostForm
from .models import Post
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


def index(request):
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
    success_url = "../first.html"
    template_name = "first/signup.html"

    def form_valid(self, form):
        form.save()
        return super(Signup, self).form_valid(form)

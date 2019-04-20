#from django.shortcuts import render
#from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
from .forms import PostForm
from .models import Post


def index(request):

    if request.method == 'POST':
        postform = PostForm(request.POST)
        postform.save()


    postform = PostForm()

    posts = Post.objects.order_by('-published')

    return render(request, 'first/index.html', {'posts': posts, 'postform': postform})

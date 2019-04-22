from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {'title': TextInput(attrs={'class': 'validate', 'id': 'title'}),
                    'content': Textarea(attrs={'class': 'materialize-textarea', 'id': 'content'})
                   }

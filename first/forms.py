from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import Post, Bio


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {'content': Textarea(attrs={'class': 'materialize-textarea', 'id': 'content'})
                   }


class BioForm(ModelForm):
    class Meta:
        model = Bio
        fields = ['biogr']
        widgets = {'biogr': Textarea(attrs={'class': 'materialize-textarea', 'id': 'bio'})}

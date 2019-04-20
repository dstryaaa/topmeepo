from django.forms import ModelForm, TextInput
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
                   'content': TextInput(attrs={'class': 'input', 'placeholder': 'Content'})}
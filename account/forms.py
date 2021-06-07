from django import forms
from django.contrib.auth import authenticate
from account.models import Home,Post

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']



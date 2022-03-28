from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from .models import Post,Tags,Comment,CustomUser

User = get_user_model()

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','age',)

class find_userForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('name', 'email',)

class TagForm(forms.ModelForm):

    class Meta:
        model = Tags
        fields = ('tag',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class CustomUserCreationForm(UserCreationForm):
 
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','name', 'email', 'gender', 'job','active','auto_increment_id')
  
class CustomUserChangeForm(UserChangeForm):
 
    class Meta:
        model = CustomUser
        fields = ('username','name', 'email', 'gender', 'job','active','auto_increment_id')



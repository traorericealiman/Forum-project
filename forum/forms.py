from django import forms
from .models import Comment, CustomUser, Reply, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the post title', 'required': 'required'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your content here', 'rows': 5, 'required': 'required'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': 'required'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Vous pouvez rendre le champ requis

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture']

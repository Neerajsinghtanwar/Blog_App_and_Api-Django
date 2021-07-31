from django.contrib.auth import models
from django.forms import widgets
from app.models import Contact, Blog
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, UserModel, UsernameField
from django.contrib.auth.models import Group, User

class Signupform(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User     
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {'first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs=
        {'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class Loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title', 'desc']
        labels = {'title':'Title', 'desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
        'desc':forms.Textarea(attrs={'class':'form-control'})
        }

class UserDetail(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs=
        {'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        'date_joined':forms.TextInput(attrs={'class':'form-control'}),
        }
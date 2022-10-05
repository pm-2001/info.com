
import email
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Category, Post,Comment,Profile
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password1': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password2': forms.TextInput(attrs={'class': 'form-control'}),
        # }
class EditProfileForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    # username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    # # last_login = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    # # is_superuser = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    # # is_staff = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    # # is_active = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    # # date_joined = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User    
        fields = ('username','first_name','last_name','email')

        widgets={
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
        }
        # 'is_superuser','is_staff','is_active','last_login','date_joined'

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields = ('pic','bio','website_url','fb_url','twitter_url','instagram_url','linkedin_url')
        template_name='edit_profile.html'
        widgets={
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'website_url': forms.TextInput(attrs={'class':'form-control'}),
            'fb_url': forms.TextInput(attrs={'class':'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class':'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class':'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class':'form-control'}),
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))

    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2',]

choices = Category.objects.all().values_list('name','name')
choice_list =[]

for item in choices:
    choice_list.append(item)

class ImageForm(forms.ModelForm):
    class Meta:
        model=Post
        fields =['title','username','body','image','snippet','category']
        template_name='post.html'   
        # fields = ('title',)  
        widgets = {
            'category':forms.Select(attrs={'class':'form-control'},choices=choice_list),
            # 'body': CKEditorUploadingWidget(attrs={
            #     'class': 'my-ckeditor-class'
            #     'id': 'my-ckeditor-id'
            # })
        } 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','body')

        widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
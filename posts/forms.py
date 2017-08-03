from django import forms
from .models import Post
from django.contrib.auth.models import User 

class PostForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields =['title','content' , 'image','draft']
		
		widgets = {
		'publish':forms.DateInput(attrs={"type":"date"}),
		}



class UserSignUp(forms.ModelForm):

	class Meta :
		model= User 

		fields = ['username','password']

		widgets ={

		'password':forms.PasswordInput()
		}

class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True , widget=forms.PasswordInput())
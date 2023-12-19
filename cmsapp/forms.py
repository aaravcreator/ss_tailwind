from dataclasses import fields
from django import forms 
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        



class CustomUserChangeForm(UserChangeForm):
    '''This form is for user update in django admin'''

    class Meta:
        model = User

        exclude = ('password',)







class CourseForm(ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))   

    class Meta:

        model = Course
        exclude = ['slug','author']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}
class LessonForm(ModelForm):
    class Meta:

        model = lessons
        exclude = ['slug','author','Course']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}
class signupForm(UserCreationForm):
    password1 = forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model  = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.TextInput(attrs={'class':'form-control'})}
        
class signinForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label= 'Password',strip  =False,widget=forms.PasswordInput(attrs = {'class':'form-control','autocomplete':'current-password'}))

class QuestionForm(ModelForm):
    class Meta:

        model = Question
        exclude = ['quiz','created']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}

class AnswerForm(ModelForm):
    class Meta:

        model = Answer
        exclude = ['question']
        widgets = {'text':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}



class QuizForm(ModelForm):
    class Meta:

        model = Quiz
        exclude = ['course','lessons']
        widgets = {'text':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}




class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
        

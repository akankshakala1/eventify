from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category', 'organizer']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    


class LoginForm(forms.Form):  
    
    username = forms.CharField(max_length = 200 , widget=forms.TextInput(attrs={'class': 'form-control'}))  
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))

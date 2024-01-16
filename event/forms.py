from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event,Invitation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category', 'organizer']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['organizer'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control'

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    


class LoginForm(forms.Form):  
    
    username = forms.CharField(max_length = 200 , widget=forms.TextInput(attrs={'class': 'form-control'}))  
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}))



class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['receiver', 'event']


    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields['receiver'].widget.attrs['class'] = 'form-control'    
        self.fields['event'].widget.attrs['class'] = 'form-control'    
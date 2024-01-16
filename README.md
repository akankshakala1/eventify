# eventify

# Project Documentation

## Table of Contents

---

1. [Introduction](#1-introduction)
2. [Project Overview](#2-project-overview)
   1. [Project Goals](#21-project-goals)
   2. [Technologies Used](#22-technologies-used)
3. [System Architecture](#3-system-architecture)
   1. [Frontend (React + TypeScript)](#31-frontend-react--typescript)
   2. [Backend (Django)](#32-backend-django)
4. [Features](#4-features)
   1. [User Registration and Authentication](#41-user-registration-and-authentication)
   2. [Event Creation](#42-event-creation)
   3. [Event Management](#43-event-management)
   4. [Invitations](#44-invitations)
5. [API Root](#5-api-root)
6. [Settings and Configurations](#6-settings-and-configurations)
7. [Project Structure](#7-project-structure)

---

## 1. Introduction

---

Here is a rough walk through the journey of conceptualizing, designing, and implementing an application that simplifies event planning and management

---

## 2. Project Overview

---

### 2.1 Project Goals

The aim was to develop a user-friendly and efficient Event Planning App that enables users to create, manage, and schedule events seamlessly. The key project goals include:

Streamlining event creation and management.
Ensuring user data security.
Sending invitations to other users.
Leveraging modern web technologies for a robust and responsive user interface.

### 2.2 Technologies Used

The Event Planning built using a combination of modern technologies:

- **Frontend (django templates):** The user interface is developed using Django templates, which provide a seamless integration with the backend logic. The frontend templates are organized into a structured layout to ensure a consistent and user-friendly design

- **Backend (Django):** The backend is powered by Django, a Python web framework. We use Django Rest Framework for building RESTful APIs and generic views are employed for efficient data handling.

---

## 3. System Architecture

---

### 3.1 Frontend (django forms + HTML5 templates)

The frontend is built django forms and are then hooked up with the views and templates

### 3.2 Backend (Django)

The backend is powered by Django, a high-level Python web framework. We employed Django Rest Framework (DRF) to create RESTful APIs, enabling seamless communication between the frontend and backend.

---

## 4. Features

---

### 4.1 User Registration and Authentication

The project uses a basic mechanism for authentication username and password

Authentication routes used are:

- **http:127.0.0.1:8000/register/:** This url end point is responsible for creating a new user.

- **http:127.0.0.1:8000/login/:** This url end point is responsible for logging in and using a username and password

### 4.2 Event Creation

A ModelViewSet is implemented that handles different CRUDE requests, for creating events

- **EventListView:**

```python
class EventListView(ListView):
    model = Event
    template_name = 'event_details.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Event.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

```

- **forms:**

A form is used to implement the behavour and attributes of the different html

```python


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

```

### 4.3 Event Management

Users can manage their events within the app and or send invites

### 4.4 Invitations

Based on created events, a logged in user can send event invitations to other users. An email smtp server is also implemented that can send email based event invitations to other users. The email uses google oauth2

InvitationCreateView

```python


class InvitationCreateView(LoginRequiredMixin, FormView):
    template_name = 'invitation_create.html'
    form_class = InvitationForm
    success_url = reverse_lazy('invitation_create_success')

    def form_valid(self, form):
        mail_host_user = getattr(settings, "EMAIL_HOST_USER", None)

        event = form.cleaned_data['event']
        receiver = form.cleaned_data['receiver']
        recipient_email = receiver.email

        email_subject = 'Event Invitation'
        email_text_content = 'Event Invitation'
        email_html_content = render_to_string('emails/event_email.html', {'event': event})

        if recipient_email:
            msg = EmailMultiAlternatives(email_subject, email_text_content, mail_host_user, [recipient_email])
            msg.attach_alternative(email_html_content, "text/html")
            msg.send()

            invitation = form.save(commit=False)
            invitation.sender = self.request.user
            invitation.save()

            return super().form_valid(form)
        else:
            return JsonResponse({'error': 'Recipient email not provided'}, status=400)

    def form_invalid(self, form):
        return JsonResponse({'error': 'Form is invalid'}, status=400)


```

Admin Dashboard

```python

from django.contrib import admin
from .models import Event,Invitation,Category,Location




# Register your models here.
@admin.register(Location)
class LoacationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    list_per_page = 25
    search_fields = ('name', 'address')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_per_page = 25
    search_fields = ('name', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'location', 'date')
    list_per_page = 25
    ordering = ('-date',)
    search_fields = ('title', 'location', 'date')


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'event_name', 'status')
    list_per_page = 25
    ordering = ('accepted',)
    search_fields = ('title', 'location', 'date')


    @admin.display(ordering='accepted')
    def status(self, invitation):
        if invitation.accepted == False:
            return 'Not Accepted'
        return 'Accepted'

    def event_name(self , invitation):
        return invitation.event.title

```

- Loook for the above code in `eventify/event/admin.py`

## 5. Api Root

Here is the api documentation for the different endpoints:

```python

urlpatterns = [
 path('admin/', admin.site.urls),
     path('', IndexView.as_view(), name='index'),
     path('login/', UserLoginView.as_view(), name='login'),
     path('logout/', UserLogoutView.as_view(), name='logout'),
     path('create/', CreateEventView.as_view(), name='create_event'),
     path('profile/', ProfileView.as_view(), name='profile'),
     path('search/', SearchView.as_view(), name='search'),
     path('event_details/<int:event_id>/', EventDetailView.as_view(), name='event_details'),
     path('register/', UserRegistrationView.as_view(), name='register'),
     path('home/', HomeView.as_view(), name='home'),
     path('invite/create', InvitationCreateView.as_view(), name='invitation_create'),
     path('invite/success/', TemplateView.as_view(template_name='invitation_create_success.html'), name='invitation_create_success'),
     path('logout/', UserLogoutView.as_view(), name='logout'),

]

```

## 6. Settings and Configurations

Different app configurations are set in `eventify/eventify/settings`

To configure the email backend, username and password, edit

```python

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_DEBUG = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get('MAIL_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('MAIL_PASSWORD')


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

GOOGLE_CLIENT_ID = os.environ.get('CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)
client.prepare_request_body(include_client_id=True)

```

To configure allowed hosts and ip's change the following:

```python

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

```

One can also use a different database other than sqlite3 db
here is the current configuration;

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


```

To use MySQL database , change it to :

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db name',
        'HOST': 'localhost',
        'USER': 'db username',
        'PASSWORD': 'db password'
    }
}

```

Then run,

```sh
python3 manage.py migrate

```

<p style="color: orange;"> NB: Each time you change your database and run the above command you'll loose all your data eg events,invitations,users etc. To recover the data , search for a backup tool eg mysqldump to backup the data then repopulate the data into the new database</p>

Other necessary commands are:

- python3 manage.py createsuperuser (to create an admin)
- python3 manage.py changepassword (to reset the admin password)

The above commands must be against the root project folder (eventify)

---

## 7. Project Structure

---

```
.
└── eventify                   # The project root folder
    └── event                   # Contains most of the the backend code
        ├── migrations          # Contains database migrations
        └── templates           # Django templates (html)


```

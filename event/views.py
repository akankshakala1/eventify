from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EventForm,SignUpForm,LoginForm,InvitationForm
from django.contrib.auth.models import User
from .models import Event


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'



# class UserLoginView(LoginView):
#     template_name = 'login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('home')

class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        return render(request, self.template_name, {'form': form})

class UserRegistrationView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object) 
        return response

class HomeView(LoginRequiredMixin,ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    login_url = '/login/'



class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'create_event.html'
    login_url = '/login/'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    


class ProfileView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'profile.html'
    context_object_name = 'user_events'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)           


class SearchView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Event.objects.filter(title__icontains=query) | Event.objects.filter(description__icontains=query)


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


class EventDetailView(View):
    template_name = 'event_details.html'

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        return render(request, self.template_name, {'event': event})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

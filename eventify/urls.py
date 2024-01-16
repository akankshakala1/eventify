"""
URL configuration for eventify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from event.views import ( UserLoginView, UserLogoutView ,
                        IndexView,CreateEventView,
                     ProfileView,SearchView,EventListView,
                     UserRegistrationView ,HomeView,InvitationCreateView,EventDetailView
)

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



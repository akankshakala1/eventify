from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User,AbstractUser, Group, Permission



class RegularUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='regularuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='regularuser_set', blank=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        permissions = (("can_do_view_events", "view events"),)

    def __str__(self):
        return self.username

class OrganizerUser(AbstractUser):
    organization = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    groups = models.ManyToManyField(Group, related_name='organizeruser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='organizeruser_set', blank=True)
    
    class Meta:
        permissions = (("can_manage_events", "Can manage events"),)  


    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.address}'

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE , related_name='location_events')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)

    def __str__(self):
        return f'{self.title} - {self.description}'

class Invitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)


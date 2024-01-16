from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



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


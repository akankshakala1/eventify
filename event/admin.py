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




from django.contrib import admin
from .models import Event, Review, Category, Bookmark, Organizer, Media, Ticket, IpModel

# Register your models here.
admin.site.register(Event)
admin.site.register(Media)
admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(Organizer)
admin.site.register(IpModel)
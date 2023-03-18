from django.forms import ModelForm
from .models import Event, Organizer

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['creator', 'slug']

class OrgForm(ModelForm):
    class Meta:
        model = Organizer
        fields = '__all__'
        exclude = ['user',  'account_name', 'account_number', 'bank', 'slug']
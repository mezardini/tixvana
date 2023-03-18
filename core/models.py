from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify  
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Organizer(models.Model):
    Access_Bank    = '044'
    Citibank    = '023'
    Ecobank    = '050'
    FCMB    = '214'
    Fidelity    = '070'
    First_Bank    = '011'
    GTB    = '058'
    Heritage    = '030'
    Jaiz_Bank    = '301'
    Keystone    = '082'
    Parallex    = '526'
    Providus    = '101'
    Stanbic     = '221'
    Skye_Bank    = '076'
    Standard_Bank    = '068'
    Sterling_Bank    = '232'
    Suntrust_Bank    = '100'
    Titan_Trust    = '102'
    Union_Bank    = '032'
    United_Bank    = '033'
    Unity_Bank    = '215'
    Wema_Bank    = '035'
    Zenith_Bank   = '057'
    Code = [
            ('044'  ,    ('Access Bank')),     
            ('023'  ,    ("Citibank")) , 
            ('050'   ,    ('Ecobank')),   
            ('214'     ,    ('FCMB'))  ,   
            ('070'  ,    ('Fidelity')),  
            ('011',    ('First Bank')), 
            ('058'  ,    ("GTB")), 
            ('030'  ,    ('Heritage')) , 
            ('301'  ,  ('Jaiz Bank')), 
            ('082' ,    ('Keystone')), 
            ('526' ,    ('Parallex')), 
            ('101' ,    ('Providus')), 
            ('221' ,    ('Stanbic')), 
            ('076' ,  ('Skye Bank')), 
            ('068',    ('Standard Bank')), 
            ('232',    ('Sterling Bank')), 
            ('100',    ('Suntrust Bank')), 
            ('102'  ,    ('Titan Trust')), 
            ('032',    ('Union Bank')),
            ('033'  ,    ('United Bank')), 
            ('215',    ('Unity Bank')),
            ('035' ,   ('Wema Bank')),
            ('057'  ,    ('Zenith Bank')), 
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    biz_name = models.CharField(max_length=1000,null=True)
    slug = models.SlugField(max_length=500, null=False, unique=True)
    account_number = models.IntegerField(null=True)
    bank_code = models.CharField(choices=Code, null=True, max_length=4)
    account_name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Event(models.Model):
    entertainment = 'Entertainment'
    tech = 'Tech'
    professional = 'Professional'
    religious = 'Religious'
    STATUS = [
       (entertainment, ('ENtertainment')),
       (tech, ('TEch')),
       (professional, ('PRofessional')),
       (religious, ('REligious')),
   ]
    title = models.CharField(max_length=500)
    venue = models.CharField(max_length=1000, null=True)
    description = models.TextField()
    creator = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=STATUS, null=True)
    poster = models.ImageField(null=True, blank=False, upload_to='media')
    ticket_price = models.FloatField(null=True)
    tickets_ava  = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(default=0)

    slug = models.SlugField(max_length=500, null=False, unique=True)
    # earnings = models.FloatField(null=True)

    
    class Meta:
        ordering = [ '-created']

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tix_code = models.CharField(max_length=500, null=True, unique=True)
    tix_mail = models.CharField(max_length=500, null=True)
    tix_name = models.CharField(max_length=500, null=True)
    tix_phone = models.CharField(max_length=500, null=True)
    ticket_price = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    # def total_tix(self):
    #     return self.count() * self.ticket_price

    def __str__(self):
        return self.event.title +  "; " + self.tix_code

class Media(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    photos = models.ImageField(null=True, blank=False, upload_to='media')

    def __str__(self):
        return self.event.title 

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.event.title +  "; " + self.comment

class Bookmark(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title

class CustomerInfo(models.Model):
    full_name= models.CharField(max_length  = 150)
    email= models.EmailField()
    phone_number = models.CharField(max_length= 20)
    address = models.CharField(max_length = 150)
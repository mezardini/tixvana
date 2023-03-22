from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, get_object_or_404
import requests
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages
from .models import Event, Review, Category, Bookmark, Organizer, Media, Ticket
import random
from django.db.models import Sum
from django.template.defaultfilters import slugify  
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template import loader, Template
from django.template.loader import render_to_string
from django.core import mail
from datetime import datetime
from django.conf import settings

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import environ
from .forms import EventForm, OrgForm

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# Create your views here.
def index(request):
    events = Event.objects.all()
    users_in_group = Group.objects.get(name="Organizers").user_set.all()
    organizer = Organizer.objects.all()

    context = {'events':events, 'users_in_group':users_in_group, 'organizer':organizer}
    return render(request, 'home.html', context)

def browse(request):
    events = Event.objects.all()

    context = {'events':events}
    return render(request, 'browse.html', context)

def search_event(request):
    room = Event.objects.all()
    if request.method == 'GET':
        searched = request.GET['search_term']
        topics = Event.objects.filter(title__contains = searched)
        return render(request, 'search_event.html', {'searched':searched, 'room':room, 'topics':topics})

    context = {'room':room,  'topics':topics}
    return render(request, 'search_event.html', context)

def terms(request):

    return render(request, 'terms.html')

def contact(request):

    if request.method == 'POST':

        sender = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            'Message from '+ email + " " + sender,
            message,
            'settings.EMAIL_HOST_USER',
            ['mezardini@gmail.com'],
            fail_silently=False,
        )

    return redirect('index')

def details(request, slug):
    event = Event.objects.get(slug=slug)
    event.views=event.views+1
    event.save()
    organizer = Organizer.objects.all()
    media = event.media_set.all()
    review = event.review_set.all()
    ticket = Ticket.objects.filter(event=event)
    if request.method == 'POST':
        comment = Review.objects.create(
            name = request.POST.get('name'),
            comment = request.POST.get('comment'),
            event = event
        )
        comment.save()
        return redirect('details', slug=event.slug)

    context = {'event':event, 'media':media, 'review':review, 'ticket':ticket, 'organizer':organizer}
    return render(request, 'eventx.html', context)

def admin_details(request, slug):
    event = Event.objects.get(slug=slug)
    tickets = event.ticket_set.all()
    x = tickets.count()
    y = event.ticket_price
    sold = event.tickets_ava
    left = "{:0.2f}".format(x/sold * 100)
    res =  x*y
    ava = sold-x
    sum_total = '{:,}'.format(res)
    event_date = event.date.date()
    present = datetime.now().date()
    # d1 = datetime.datetime.strptime(event_date, "%m/%d/%Y").date()
    # date_check = datetime(event_date) < present

    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
         

    context = {'event':event, 'tickets':tickets, 'form':form, 'left':left, 'sum_total':sum_total, 
               'ava':ava, 'date': event_date, 'present':present}
    return render(request, 'eventadmin.html', context)

def delete_event(request, slug):
    event = Event.objects.get(slug=slug)

    if request.method == 'POST':
        event.delete()
        return redirect('index')
    
    context = {'event':event}
    return render(request, 'delete.html', context)
    

def profile(request, slug):
    profilex = Organizer.objects.get(slug=slug)
    events = Event.objects.filter(creator=profilex)
    eventsz = Event.objects.all()
    tickets = Ticket.objects.filter(event__creator=profilex)
    sum_totalx  = tickets.count()
    sum_total =  sum(tickets.values_list('ticket_price', flat=True))
    ticket_sold = events.count()
    # avg_price = sum_total/ticket_sold
    # earnings of organizer, get the price of tickets sold for an event and then add all events for an organizer


    form = OrgForm(request.POST or None, instance=profilex)

    if request.method == 'POST':

        
        
        org = Organizer.objects.create(
            user = request.user,
            phone = request.POST.get('phone'),
            account_number = request.POST.get('aza_num'),
            account_name = request.POST.get('aza_name').lower(),
            bank = request.POST.get('bank'),
            poster = request.FILES.get('image'),
            slug = slugify(request.POST['user']),
        )
        
        org.save()
       
    if form.is_valid():
        form.save()

    context = {'profilex':profilex, 'events':events, 'tickets':tickets, 'sum_total':sum_total, 'sum_totalx':sum_totalx, 'form':form, 'ticket_sold':ticket_sold}
    return render(request, 'admin.html', context)

@login_required(login_url='signin')
def create_event(request, pk):
    profilex = Organizer.objects.get(id=pk)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        eventcreate = Event.objects.create(
            title = request.POST.get('title'),
            venue = request.POST.get('venue'),
            description = request.POST.get('description'),
            tickets_ava = request.POST.get('limit'),
            ticket_price = request.POST.get('price'),
            creator = profilex,
            category = request.POST.get('category'),
            date = request.POST.get('date'),
            slug = slugify(request.POST['title']),  
            poster = request.FILES.get('images')
        )
        
        eventcreate.save()

        for image in images:
            photo = Media.objects.create(
            event = eventcreate,
            photos = image,
            video = request.FILES.get('video'),
            )
            photo.save()

        

        # photo = Media.objects.create(
        #     event = eventcreate,
        #     photos = request.FILES.get('image'),
        #     video = request.FILES.get('floor_plan'),
        # )
        # photo.save()
            
        return redirect('details', slug=eventcreate.slug)

    context = {'profile':profilex}
    return render(request, 'create_event.html', context)




def makepayment(request, slug):
    global eventx
    eventx = Event.objects.get(slug=slug)
    pricex = "{:.0f}".format(eventx.ticket_price)
    qprice = int(eventx.ticket_price*100)
    price = "{:.0f}".format(qprice) 
    byte = random.randint(1000,1239)
    ticket = Ticket.objects.filter(event=eventx)
    tix_count = ticket.count
    
    # commission = 5
    # if tix_count() >  10:
    #     commission = 0
    # elif tix_count() > 10 and tix_count() < 101:
    #     commission = 0.05*int(eventx.ticket_price)
    # elif tix_count() > 100 and tix_count() < 501:
    #     commission = 0.035*int(eventx.ticket_price)
    # elif tix_count() > 500 :
    #     commission = 0.02*int(eventx.ticket_price)
    
   
    #determine the commission of tixvana

    # global tix_code
    # tix_code = "#" + str(eventx.id) + "-" + str(random.randint(1000,123999999))
    global tix_mail
    tix_mail = request.POST.get('customer[email]')
    ref = ''+str((1000 + random.random()*900))
    # tix_name = request.POST.get('customer[name]')
    # tix_phone = request.POST.get('phone')
    if request.method == 'POST':
        global tix_code
        tix_code = "#" + str(eventx.id) + "-" + str(random.randint(1000,123999999))
        tix_mail = request.POST.get('customer[email]')
        global tix_name
        tix_name = request.POST.get('customer[name]')
        tix_phone = request.POST.get('phone')
        ticket_price = request.POST.get('price'),
        tix = Ticket.objects.create(
            event = eventx,
            tix_code = tix_code,
            tix_mail = request.POST.get('customer[email]'),
            tix_name = request.POST.get('customer[name]'),
            tix_phone = request.POST.get('phone'),
            ticket_price = request.POST.get('price'),
        )
        tix.save()
        
        # return redirect(str(process_payment(tix_name,tix_mail,ticket_price,tix_phone)))

    context = {'event':eventx, 'byte':byte, 'ref':ref, 'price':price, 'pricex':pricex, 'tix_count':tix_count}
    return render(request,'payx.html', context)

def bookmark(request, pk):
    eventx = Event.objects.get(slug=pk)
    
    
    tix = Bookmark.objects.create(
            event= eventx,
            user = request.user,  
        )
    tix.save()
    tix.event.add(eventx)
        
    return redirect('details', slug=eventx.slug)

def bookmarklist(request, pk):
    event = User.objects.get(id=pk)
    events = Event.objects.all
    bookmarks = Bookmark.objects.filter(user=event)
    

    context = {'bookmarks':bookmarks}
    return render(request, 'bookmarks.html', context)

@login_required(login_url='signin')   
def organizer(request):
    
    if request.method == 'POST':
        headers = {
            'Authorization': env('Bearer'),
        }
        account_number = request.POST.get('aza_num')
        bank_code = request.POST.get('bank')

        response = requests.get('https://api.paystack.co/bank/resolve?account_number='+account_number+'&bank_code='+bank_code, headers=headers)
        print(response.text)

        data = json.loads(response.text)
        print(data)
        x = data.get("data").get("account_name")
        aza_name = x.lower()
        account_namex = aza_name.lower()
        

        if aza_name != account_namex:
            messages.error(request, "Account credentials invalid!.")
            return render(request, 'org_create.html')
        else:
            
            org = Organizer.objects.create(
                user = request.user,
                phone = request.POST.get('phone'),
                account_number = request.POST.get('aza_num'),
                account_name = account_namex,
                bank_code = request.POST.get('bank'),
                biz_name = request.POST.get('biz_name'),
                slug = slugify(request.POST['biz_name']),
            )
            org.save()
            user_group = Group.objects.get(name="Organizers")
            request.user.groups.add(user_group)
            return redirect('profile', slug=org.slug)
    
    return render(request, 'org_create.html')

def signup(request):
    if request.method == 'POST':
        global first_name
        username = request.POST.get('email')
        first_name = request.POST.get('name')
        global email
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        global token
        token =  str(random.randint(100001,999999))

        
        if User.objects.filter(email=email).exists():
                messages.error(request, "User already exists.")
                return redirect('signup')

        if not request.POST.get('password1'):
            messages.error(request, "Password cannot be blank.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "User already exists.")
                return redirect('signup')
            else:
                global user
                html_message = loader.render_to_string(
                'email.html',
                {
                    'user_name': first_name,
                    'token':   token,
                  
                }

                )
                # context = {'user_name': first_name,'token':   token}
                # template = template_env.get_template('templates/email.html')
                # output_text = template.render(context)
                # send_mail(
                #     'Ticket booked!!!',
                #      html_message,
                #     'tixvana@gmail.com',
                #     [email],
                #     fail_silently=False,
                # )
                mail = EmailMessage(
                    "Registered",
                    html_message,
                    'settings.EMAIL_HOST_USER',
                    [email],
                )
                mail.fail_silently = False
                mail.content_subtype = 'html'
                mail.send()
                user = User.objects.create_user(username=username,first_name=first_name, password=password1, email=email)
                
                user.is_active = False
                user.save()
                return redirect('verifymail')


    return render(request, 'register.html')

def verifymail(request):
    
    
    

    
    if request.method == 'POST':
        
        entetoken = request.POST.get('token')
        entered_token = str(entetoken)

        if entered_token == token:
            messages.error(request, "Email validated, you can now signin.")
            user.is_active = True
            user.save()
            return redirect('signin')

        else:
            messages.error(request, "Token incorrect.")
            user.is_active = False
            user.save()
            return redirect('signup')


    return render(request, 'verify.html')

def signin(request):
    users_in_group = Group.objects.get(name="Organizers").user_set.all()
    organizer = Organizer.objects.all()
    if request.method == 'POST':
        
        organizer = Organizer.objects.all()
        email = request.POST.get('email')
        password = request.POST['password']

        if not request.POST.get('email'):
            messages.error(request, "Email cannot be blank.")
            return redirect('signin')

        if not request.POST.get('password'):
            messages.error(request, "Password cannot be blank.")
            return redirect('signin')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None and user is organizer:
            auth.login(request, user)
            return redirect('index')
        elif user is not None and user is not organizer:
            auth.login(request, user)
            return redirect('organizer')
        else:
            messages.error(request, "Incorrect username or password.")
            return render(request, 'signin.html')
    
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('signin') 

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')

# def process_payment(tix_name,tix_mail,ticket_price,tix_phone):
#      auth_token= env('SECRET_KEY')
#      hed = {'Authorization': 'Bearer ' + auth_token}
#      data = {
#                 "tx_ref":''+str((1000 + random.random()*900)),
#                 "amount":ticket_price,
#                 "currency":"NGN",
#                 "redirect_url":"http://localhost:8000/callback",
#                 "payment_options":"card",
#                 "meta":{
#                     "consumer_id":23,
#                     "consumer_mac":"92a3-912ba-1192a"
#                 },
#                 "customer":{
#                     "email":tix_mail,
#                     "phonenumber":tix_phone,
#                     "name":tix_name
#                 },
#                 "customizations":{
#                     "title":"Tixvana",
#                     "description":"Best store in town",
#                     "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
#                 }
#                 }
#      url = ' https://api.flutterwave.com/v3/payments'
#      response = requests.post(url, json=data, headers=hed)
#      response=response.json()
#      link=response['data']['link']
#     #  message = 'Dear' + tix_name + 'your ticket for event has been booked. Your ticket code is ' + tix_code,
#     #  receiver = tix_mail
#      return link
    

@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    event = str(eventx)
    tix_namez = tix_name
    tix_codex = 'Hello ' + tix_namez + ' your ticket for the show ' + event + ' has been booked, your ticket code is '+ tix_code
    tix_mailx = tix_mail
    send_mail(
            'Ticket booked!!!',
            tix_codex,
            'settings.EMAIL_HOST_USER',
            [tix_mailx],
            fail_silently=False,
        )
    return HttpResponse('Finished')



# import os
# from rave_python import Rave

# def verifyaza(account_name,account_number,bank):
#     rave = Rave(os.getenv("FLW_PUBLIC_KEY"), os.getenv("FLW_SECRET_KEY"))
#     details = {
#       "account_number": account_number,
#       "account_bank": bank
#     }
#     response = rave.Transfer.accountResolve(details)
#     context = {'response':response}
#     return redirect('profile', context)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('browse', views.browse, name="browse"),
    path('terms', views.terms, name="terms"),
    path('search', views.search_event, name="search"),
    path('contact', views.contact, name="contact"),
    path('event/<str:slug>', views.details, name="details"),
    path('create_event', views.create_event, name="create_event"),
    path('ticket/<str:pk>', views.bookmark, name="bookmark"),
    path('bookmark/<str:pk>', views.bookmarklist, name="bookmarklist"),
    path('organizer', views.organizer, name="organizer"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('verifymail', views.verifymail, name='verifymail'),
    path('signout', views.signout, name='signout'),
    path('makepayment/<str:slug>', views.makepayment, name='makepayment'),
    path('adminview/<str:slug>', views.admin_details, name='adminview'),
    path('organizer/<str:slug>', views.profile, name='profile'),
    path('deleteevent/<str:slug>', views.delete_event, name='deleteevent'),
    path('callback', views.payment_response, name='payment_response'),
    
]




if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
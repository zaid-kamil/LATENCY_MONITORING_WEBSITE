from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/', views.feedback, name='feedback'), 
    path('issue/', views.Issue, name='issue'),
    path('notification/', views.notification, name='notification'),
    path('website/', views.website, name='website'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    ]
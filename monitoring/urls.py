from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/', views.feedback, name='feedback'), 
    path('issue/', views.Issue, name='Issue'),
    path('notification/', views.notification, name='notification'),
    path('website/', views.website, name='website'),
    ]
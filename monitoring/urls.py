from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/', views.create_new_feedback, name='feedback'), 
    path('feedback/', views.view_feedback, name='view_feedback'),
    path('issue/', views.create_new_issue, name='issue'),
    path('notification/', views.notification, name='notification'),
    path('website/new/', views.website, name='website'),
    path('website/<int:pk>/view', views.view_website, name='website_view'),
    path('website/<int:pk>/edit/', views.edit_website, name='website_edit'),
    path('website/<int:pk>/delete/', views.delete_website, name='website_delete'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact_view, name='contact'),
    
    ]
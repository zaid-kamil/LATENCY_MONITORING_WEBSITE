from django.urls import path
from . import views 
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path('reset-password/<str:otp>/', views.reset_password, name='reset_password'),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("profile/create", views.create_profile, name="create_profile"),
    

]
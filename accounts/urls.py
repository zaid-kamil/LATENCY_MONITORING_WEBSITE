from django.urls import path
from . import views 
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("profile/create", views.create_profile, name="create_profile"),
    path("profile/view", views.view_profile, name="view_profile"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
]
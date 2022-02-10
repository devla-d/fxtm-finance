from django.urls import path

from . import views



urlpatterns = [
    path('register/',views.registration_view, name="register"), 
    path('login/',views.login_view, name="login"), 
    path('logout/',views.logout_view, name="logout"), 
    path('activate-account/<uidb64>/<token>/',views.account_activate_view, name="account_activate"), 
]

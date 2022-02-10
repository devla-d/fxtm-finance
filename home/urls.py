from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('pricing/', views.pricing_page, name="pricing"),
    path('about-us/', views.about_page, name="about"),
    path('contact-us/', views.contact_page, name="contact"),
]

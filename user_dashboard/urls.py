from django.urls import path

from . import views 

urlpatterns = [
     path('dashboard/', views.dashbaord_view, name="dashboard"),
     path('my-account/', views.account_view, name="account"),
     path('fund-account/', views.deposite_view, name="deposite"),
     path('withdraw-funds/', views.withdrawal_view, name="withdrawal"),
     path('notifications/', views.notification_view, name="notification"),
     path('account-log/', views.history_view, name="history"),
     path('settings/', views.settings_view, name="settings"),
     path('password-settings/', views.settings_password_view, name="password-settings"),
     path('create-investment/', views.create_investment_view, name="create_investment"),
     path('checkout/', views.checkout_view, name="checkout"),
     path('credit-user-investment/', views.end_user_investment_view, name="end_user_investment_view"),
]

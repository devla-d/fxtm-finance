from django.urls import path

from . import views


urlpatterns = [
    path('staff/dashboard/',views.dashboard_view, name="dashboard"), 
    path('staff/users/',views.users_view, name="users"), 
    path('staff/user/<int:pk>/',views.user_detail_view, name="user"), 
    path('staff/user/<int:pk>/message/',views.user_message_view, name="message-user"),

    path('staff/payments/',views.deposit_view, name="deposit"),  

    path('staff/payment/<int:pk>/',views.deposit_detail_view, name="deposit_detail"), 



    path('staff/withdrawals/',views.withdrawal_view, name="withdrawal"),  
    path('staff/withdrawal/<int:pk>/',views.withdrawal_detail_view, name="withdrawal_detail"),  
]
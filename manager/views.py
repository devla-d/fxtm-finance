from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage, send_mail
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string



from account.models import Account

from user_dashboard.models import Transactions,Notification,Investments,Packages



from .decorators import  manager_required

from .forms import UserChangeForm





EMAIL_ADMIN = "worldcryptocurrencies01@gmail.com"
D =  'deposite'
W = "withdraw"





@manager_required
def dashboard_view(request):
    return render(request, 'superuser/dashboard.html')



@manager_required
def users_view(request):
    users = Account.objects.all()
    return render(request, 'superuser/users.html',{"users":users})






@manager_required
def user_message_view(request,pk):
    account = get_object_or_404(Account, pk=pk)
    if request.POST:
        subject = request.POST.get('subject')
        message = request.POST.get('message') 
        to_email = [account.email]
        send_mail(subject,message,EMAIL_ADMIN,to_email)
        messages.info(request,("Email sent"))
        return redirect(f"/staff/user/{account.id}/")
    else:
        messages.info(request,("UNKNOW ERROR OCCURED"))
        return redirect(f"/staff/user/{account.id}/")








@manager_required
def user_detail_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    investment =  get_object_or_404(Investments, user=account)
    if request.POST:
        submit = request.POST.get('submit')
        if submit == 'Update':
            form = UserChangeForm(request.POST,instance=account)
            if form.is_valid():
                form.save()
                messages.success(request, ('Account Updated'))
                return redirect(f'/staff/user/{account.id}/')
        elif submit == 'Delete':
            account.delete()
            messages.success(request, ('Account Deleted'))
            return redirect('users')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/staff/user/{account.id}/')
    else:
        form = UserChangeForm(instance=account)
    return render(request, 'superuser/user_detail.html',{"account":account,"investment":investment,"form":form})










@manager_required
def deposit_view(request):
    deposits = Transactions.objects.filter(trans_type=D).order_by('-date')
    return render(request, 'superuser/deposits.html',{"deposits":deposits})



@manager_required
def deposit_detail_view(request, pk):
    deposit = Transactions.objects.get(pk=pk) 
    if request.POST:
        submit = request.POST.get('submit')
        if submit == "Approve":
            deposit.status = 'approved'
            deposit.user.deposite_balance += deposit.amount
            subject = "Transaction Approved"
            message = render_to_string('superuser/deposite-email.html', {
                'user': deposit.user,
                'date': timezone.now(),
                'amount': deposit.amount,
                'status': "Approved",
            })
            deposit.user.save()
            deposit.save()
            Notification.objects.create(user=deposit.user,title="Transaction Approved", body=f" YOUR DEPOSIT OF ${deposit.amount} HAS BEEN APPROVED YOU CAN NOW BUY A PLAN")
            deposit.user.email_user(subject, message)
            messages.success(request, ('Transaction Approved'))
            return redirect(f'/staff/payment/{deposit.id}/')
        elif submit == "Decline":
            deposit.status = 'declined'
            subject = "Transaction Declined"
            message = render_to_string('superuser/deposite-email.html', {
                'user': deposit.user,
                'date': timezone.now(),
                'amount': deposit.amount,
                'status': "Declined",
            })
            Notification.objects.create(user=deposit.user,title="Transaction Declined", body=f" YOUR DEPOSIT OF ${deposit.amount} HAS BEEN Declined YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
            deposit.save()
            deposit.user.email_user(subject, message)
            messages.success(request, ('Transaction Declined'))
            return redirect(f'/staff/payment/{deposit.id}/')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/staff/payment/{deposit.id}/')
    return render(request, 'superuser/deposit_detail.html',{"deposit":deposit})








@manager_required
def withdrawal_view(request):
    withdrawals = Transactions.objects.filter(trans_type=W).order_by('-date')
    return render(request, 'superuser/withdrawals.html',{"withdrawals":withdrawals})




@manager_required
def withdrawal_detail_view(request, pk):
    withdrawal = Transactions.objects.get(pk=pk) 
    if request.POST:
        submit = request.POST.get('submit')
        if submit == "Approve":
            withdrawal.status = 'approved'
            withdrawal.user.withdraw_total += withdrawal.amount
            subject = "Transaction Approved"
            message = render_to_string('superuser/with-email.html', {
                'user': withdrawal.user,
                'date': timezone.now(),
                'amount': withdrawal.amount,
                'status': "Approved",
            })
            withdrawal.user.save()
            withdrawal.save()
            Notification.objects.create(user=withdrawal.user,title="Transaction Approved", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS BEEN APPROVED ")
            withdrawal.user.email_user(subject, message)
            messages.success(request, ('Transaction Approved'))
            return redirect(f'/staff/withdrawal/{withdrawal.id}/')
        elif submit == "Decline":
            withdrawal.status = 'declined'
            subject = "Transaction Declined"
            message = render_to_string('superuser/deposite-email.html', {
                'user': withdrawal.user,
                'date': timezone.now(),
                'amount': withdrawal.amount,
                'status': "Declined",
            })
            Notification.objects.create(user=withdrawal.user,title="Transaction Declined", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS BEEN Declined YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
            withdrawal.save()
            withdrawal.user.email_user(subject, message)
            messages.success(request, ('Transaction Declined'))
            return redirect(f'/staff/withdrawal/{withdrawal.id}/')
        else:
            messages.success(request, ('Unknown Error Occured'))
            return redirect(f'/staff/withdrawal/{withdrawal.id}/')
    return render(request, 'superuser/withdrawal_detail.html',{"withdrawal":withdrawal})









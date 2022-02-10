from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta



from .models import Transactions,Notification,Investments,Packages
from .forms import UserUpdateForm,PasswordChangeForm

D =  'deposite'
W = "withdraw"

def get_deadline(h):
	return timezone.now() + timedelta(hours=h)

def earnings(amount , perc):
    return (7/100) * amount

@login_required
def dashbaord_view(request):
    investment = get_object_or_404(Investments, user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:3]
    return render(request, 'user/dashboard.html',{"investment":investment,"notifications":notifications})


@login_required
def account_view(request):
    return render(request, 'user/account.html')

@login_required
def deposite_view(request):
    if request.POST:
        user = request.user
        amount = request.POST.get('amount')
        coin_tpye = request.POST.get('coin')
        Transactions.objects.create(user= user, amount=amount,coin_tpye=coin_tpye,trans_type=D)
        messages.success(request, ('Your Deposit Has Been Made, You Will Be Alerted Onc It Is Approved'))
        return redirect("deposite")
    else:
        return render(request, 'user/deposite.html')


@login_required
def withdrawal_view(request):
    if request.POST:
        user = request.user
        amount = int(request.POST.get('amount'))
        coin_tpye = request.POST.get('coin')
        wallet_address = request.POST.get('wallet_address')
        if amount > user.balance:
            messages.success(request, ('Inssuficient Funds'))
            return redirect("withdrawal")
        else:
            Transactions.objects.create(user= user, amount=amount,coin_tpye=coin_tpye,trans_type=W,wallet_address=wallet_address)
            messages.success(request, ('Your Withdrawal Has Been Made, You Will Be Alerted Once It Is Approved'))
            return redirect("withdrawal")
    else:
        return render(request, 'user/withdrawal.html')




@login_required
def notification_view(request):
    return render(request, 'user/notification.html')

@login_required
def history_view(request):
    transactions = Transactions.objects.filter(user=request.user).order_by('-date')
    return render(request, 'user/history.html',{"transactions":transactions})

@login_required
def settings_view(request):
    user = request.user
    if request.POST:
        submit = request.POST.get('submit')
        if submit == 'Update Profile':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, ('YOUR ACCOUNT HAS BEEN UPDATED'))
                return redirect("settings")
        elif submit == 'Change Password':
            p_form = PasswordChangeForm(request.POST,instance=user)
            if p_form.is_valid():
                password1 = p_form.cleaned_data['password1']
                user.set_password(password1)
                user.save()
                messages.info(request, f'Password Change')
                return redirect('settings')
        else:
            messages.info(request, f'Unknown error Occured')
            return redirect('settings')
    else:
        p_form =  PasswordChangeForm(initial={'user_id': request.user.id})
    return render(request, 'user/settings.html',{'p_form':p_form})

@login_required
def settings_password_view(request):
    user = request.user
    if request.POST:
        form = PasswordChangeForm(request.POST,instance=user)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            messages.info(request, f'Password Change')
            return redirect('settings')
    else:
        messages.info(request, f'Unknown error Occured')
        return redirect('settings')



@login_required
def create_investment_view(request):
    if  request.session.get('pack_id'):
        del request.session['pack_id']
    if request.POST:
        pack_id = int(request.POST.get('package'))
        package = get_object_or_404(Packages, pk=pack_id)
        request.session['pack_id'] = package.id
        messages.success(request, ('Provide The Amount'))
        return redirect("checkout")
    else:
        packages = Packages.objects.all()
        return render(request, 'user/create_investment.html',{"packages":packages})








@login_required
def checkout_view(request):
    if request.POST:
        user = request.user
        amount = int(request.POST.get('amount'))
        pack_id = int(request.POST.get('pack_id'))
        package = get_object_or_404(Packages, pk=pack_id)
        if amount not in range(package.min_amount ,package.max_amount):
            messages.success(request, (f'Input Amount Between ${package.min_amount} and ${package.max_amount}'))
            return redirect("checkout")
        else:
            if user.deposite_balance >= amount:
                investment = get_object_or_404(Investments,user=user)
                investment.end_date = get_deadline(package.hours)
                investment.start_date = timezone.now()
                investment.status = 'active'
                investment.amount_invested = amount
                user.deposite_balance -= amount
                user.total_amount_invested += amount
                user.total_investement_count += 1
                user.save()
                investment.save()
                del request.session['pack_id']
                messages.success(request, ('YOUR INVESTMENT HAS BEEN ACTIVATED'))
                return redirect("dashboard")
            else:
                del request.session['pack_id']
                messages.success(request, ('INSUFFICIENT FUNDS, DEPOSIT'))
                return redirect("create_investment")
    else:
        if request.session.get('pack_id'):
            pack_id = int(request.session.get('pack_id'))
            package = get_object_or_404(Packages, pk=pack_id)
            return render(request, 'user/checkout.html',{"package":package})
        else:
            messages.success(request, ('Something Went Wrong'))
            return redirect("create_investment")        







def end_user_investment_view(request):
    if request.POST:
        user_id = int(request.POST.get('user_pk'))
        user = request.user
        investment = get_object_or_404(Investments, user=user)
        investment.status = "completed"
        investment.amount_earn += earnings(investment.amount_invested,investment.package.percent)
        investment.is_complete = True 
        user.balance += earnings(investment.amount_invested,investment.package.percent)
        user.save()
        investment.save()
        Notification.objects.create(user=user,title="Investment Has Been Completed", body=f" YOUR INVESTMENT OF ${investment.amount_invested} HAS BEEN COMPLETED YOU CAN NOW RENEW OR UPGRADE YOUR PLAN")
        return JsonResponse({"msg":"Account Credited"})
    else:
        return JsonResponse({"msg":"Get Request Not Accepted"})









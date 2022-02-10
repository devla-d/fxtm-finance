from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import  messages
from django.http import JsonResponse
from django.contrib.auth  import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template






from .models import Account
from .forms import UserCreationForm,UserActivateForm,LoginForm



EMAIL_ADMIN = "worldcryptocurrencies01@gmail.com"






def registration_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            fullname = request.POST.get('fullname')
            username = fullname.replace(" ","_")
            instance = form.save(commit=False)
            instance.username = username
            instance.is_active = False
            instance.save()
            current_site = get_current_site(request)
            subject = 'Confirm Your TradeFx Account'
            '''message = render_to_string('account_activation_email.html', {
                'user': instance,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': default_token_generator.make_token(instance),
            })'''
            context = {
                'user': instance,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': default_token_generator.make_token(instance),
                }
            message = get_template("account_activation_email.html").render(context)
            #instance.email_user(subject, message)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=EMAIL_ADMIN,
                to=[instance.email],
                reply_to=[EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)



            messages.success(request, ('Please check your mail box for confirmation email'))
            return redirect("register")
    else:
        form = UserCreationForm()
    return render(request, 'register.html',{"form":form})





def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    destination = get_redirect_if_exists(request) 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            destination = request.POST.get('destination')
            user = authenticate(email=email, password=password)
            if user:
                login(request,user)
                if destination:
                    return redirect(destination)
                else:
                    return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, 'login.html',{"form":form,"destination":destination})



def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def logout_view(request):
    logout(request)
    return redirect('login')




 




def account_activate_view(request, uidb64, token, *args, **kwargs):
    if request.POST:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)

        '''country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        gender = request.POST.get('gender')
        profile_image = request.FILES['profile_image']

        user.country = country
        user.city = city
        user.state = state
        user.address = address
        user.zipcode = zipcode
        user.gender = gender
        user.profile_image = profile_image'''
        form = UserActivateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user.is_active = True
            user.is_email_verifield = True
            user.save()
            login(request, user)
            messages.success(request, ('Your Account Has Been Activated'))
            return redirect('dashboard')
    else:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            messages.success(request, ('Please Fill in the Form to activate your Account'))
            #return redirect('dashboard')
            return render(request, 'activate-account.html')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')

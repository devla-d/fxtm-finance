from django import forms
from account.models import Account








class UserUpdateForm(forms.ModelForm):

    country = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Country'
            }
        ),
        label = '',
        required=True
    )
    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'City'
            }
        ),
        label = '',
        required=True
    )
    state = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ZIPCODE'
            }
        ),
        label = '',
        required=True
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'ADDRESS'
            }
        ),
        label = '',
        required=True
    )
 
    zipcode = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'zipcode'
            }
        ),
        label = '',
        required=True
    )
    gender = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder":'Gender'
            }
        ),
        label = '',
        required=True
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'tel',
                'class': 'form-control',
                "placeholder":'Phone Number'
            }
        ),
        label = '',
        required=True
    )

 


    class Meta:
        model = Account
        fields = ['country','city','state','address','zipcode','gender','phone']







class PasswordChangeForm(forms.ModelForm):
    user_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'type': 'hidden',
                'class': 'form-control',

            }
        ),
        label = "",
         required=True
    )
    oldpassword = forms.CharField( max_length=30, label='Old password', widget=forms.PasswordInput(attrs={'placeholder': "OLD PASSWORD", 'class': 'form-control',}))
    password1 = forms.CharField( max_length=30, label='New Password', widget=forms.PasswordInput(attrs={'placeholder': "NEW PASSWORD", 'class': 'form-control',}))
    password2 = forms.CharField( max_length=30, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': "CONFIRN NEW PASSWORD", 'class': 'form-control',}))

    class Meta:
        model = Account
        fields = ['user_id','oldpassword','password1','password2']

    def clean(self):
        if self.is_valid():
            user_id = int(self.cleaned_data['user_id'])
            oldpassword = self.cleaned_data['oldpassword']
            password1 =  self.cleaned_data['password1']
            password2 =  self.cleaned_data['password2']
            user = Account.objects.get(id=user_id)
            if password1 != password2:
                raise forms.ValidationError("Passwords don\'t match")
            if not user.check_password(oldpassword):
                raise forms.ValidationError("Old password don\'t match")






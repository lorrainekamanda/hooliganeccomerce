from django import forms
from allauth.account.forms import SignupForm,LoginForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db import models
from django.conf import settings
from .models import Item,Artist,Order
from django.forms import widgets
from django.forms import ModelChoiceField


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
        self.fields['email'].label = False
    first_name = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Last Name'}))
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = False
        self.fields['password'].label = False

   
PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P','Paypal')
)

CATEGORY_CHOICES = (
    ('Pa','Painting'),
    ('Ph','photograph'),
    ('sc','sculpture'),
    ('pr','prints')
)

LABEL_CHOICES = (   
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')

)

class CheckoutForm(forms.Form):
    street_adress = forms.CharField(widget = forms.TextInput(attrs = {'placeholder':'1234 Main st'}))
    apartment_adress = forms.CharField(required = False,widget = forms.TextInput(attrs = {'placeholder':'Apartment or Suite'}))
    country = CountryField(blank_label = '(select country...)').formfield(widget = CountrySelectWidget(attrs = {'class':'custom-select d-block w-100'}))
    zip = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
    same_shipping_adress = forms.BooleanField(required = False)
    save_info = forms.BooleanField(required = False) 
    payment_option = forms.ChoiceField(widget = forms.RadioSelect(),choices = PAYMENT_CHOICES)


class  UserUpdateForm(forms.ModelForm):
    fields = ['username','email']

class updateProfileForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['first_name','last_name',]
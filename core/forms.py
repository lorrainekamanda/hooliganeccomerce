from django import forms
from allauth.account.forms import SignupForm
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


class ItemForm(forms.Form):
    title = forms.CharField(required = True,widget = forms.TextInput())
    price = forms.FloatField(required = True,widget = forms.TextInput())
    discount_price = forms.FloatField(required = False,widget = forms.TextInput())
    description= forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}))
    image = forms.ImageField(label = "Item Image")
    # country = CountryField(blank_label = '(select country...)').formfield(widget = CountrySelectWidget(attrs = {'class':'custom-select d-block w-100'}))
    slug= forms.CharField(label='Image Tag',widget = forms.TextInput(attrs = {'class':'form-control'}))
    lable= forms.ChoiceField(choices = LABEL_CHOICES)
    category= forms.ChoiceField(choices = CATEGORY_CHOICES)
    first_name = forms.CharField(required = True,widget = forms.TextInput())
    last_name = forms.CharField(required = True,widget = forms.TextInput())
    phone = forms.CharField(required = True,widget = forms.TextInput())
    email = forms.EmailField(required = True,widget = forms.TextInput())
    bio = forms.CharField(widget = forms.Textarea(attrs = {'class':'form-control'}))
    tweeter = forms.URLField(label = "twitter",required = True,widget = forms.TextInput())
    instagram = forms.URLField(required = True,widget = forms.TextInput())
    facebook= forms.URLField(required = True,widget = forms.TextInput())
    image_artist = forms.ImageField(label = "Your Image")

    tag= forms.CharField(label='Your Tag',widget = forms.TextInput(attrs = {'class':'form-control'}))
    # bio = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
    # country = CountryField(blank_label = '(select country...)').formfield(widget = CountrySelectWidget(attrs = {'class':'custom-select d-block w-100'}))

 
#        
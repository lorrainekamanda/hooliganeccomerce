from django import forms
from allauth.account.forms import SignupForm,LoginForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db import models
from django.conf import settings
from .models import Item,Artist,Order,BillingAdress,PaymentDetails,Chat,Show,Seller,Account,Gallery,Blog,Comments
from django.forms import widgets
from django.forms import ModelChoiceField
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput
from django_countries.fields import CountryField


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
        super().__init__(*args, **kwargs)

        self.fields["login"].label = False
        self.fields["password"].label = False

   
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
   
    class Meta:
        
        User = get_user_model()
        model = User
        fields = ['first_name','last_name','username']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = False
        self.fields['last_name'].label = False
        self.fields['username'].label = False
    first_name = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Last Name'}))
    username = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Username'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['instagram','facebook','twitter'] 

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['instagram'].label = False
        self.fields['facebook'].label = False
        self.fields['twitter'].label = False
    instagram = forms.URLField(label='',widget = forms.TextInput(attrs = {'placeholder':'instagram'}))
    facebook = forms.URLField(label='',widget = forms.TextInput(attrs = {'placeholder':'facebook'}))
    twitter = forms.URLField(label='',widget = forms.TextInput(attrs = {'placeholder':'twitter'}))
        

class UserImageForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['image_artist'] 

class UploadForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title','price','discount_price','category','label','slug','description','image']

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['host_name','gallery_email','gallery_number','gallery_number','city_state_zip_code','gallery_website']

        
class AdressForm(forms.ModelForm):
    class Meta:
        model = BillingAdress
        fields = ['street_adress','apartment_adress','zip','country']


class DateInput(forms.DateInput):
    input_type = 'date'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ['name','cardno','expiry_date','billing_adress','CITY']
        widgets = {
            'expiry_date':  DateInput(attrs={'type': 'date'}),
           
           
        }

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )
class ChatForm(forms.ModelForm):
   class Meta:
        model = Chat
        fields = ['reciever','message']




class ShowForm(forms.ModelForm):
   class Meta:
        model = Show
        fields = ['title','date','time','location','RSVP','poster']
        widgets = {
            'date':  DateInput(attrs={'type': 'date'}),
            'time':  forms.TimeInput(attrs={'type': 'time'})
           
        }


class AccountForm(forms.ModelForm):
   class Meta:
        model = Account
        fields = ['buyer','seller']


class  SellerForm(forms.ModelForm):
   
    class Meta:
        
       
        model = Seller
        fields = ['name','address','country','phone','description']

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = False
        self.fields['address'].label = False
        self.fields['phone'].label = False
        self.fields['country'].label = False
    name = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Name'}))
    address = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Address'}))
    phone = forms.CharField(max_length=30, label='',widget = forms.TextInput(attrs = {'placeholder':'Phone'}))
    description = forms.CharField(max_length=200, label='',widget = forms.Textarea(attrs = {'placeholder':'Description'}))
    country = CountryField(blank_label = '(select country...)').formfield(widget = CountrySelectWidget(attrs = {'class':'custom-select d-block w-100'}))

class BlogForm(forms.ModelForm):
    class Meta:
        
       
        model = Blog
        fields = ['subject','message','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comments']

from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from datetime import datetime
from django.utils import timezone
from django.db import models

from django.conf import settings


from django.utils.timezone import localtime
from django.db import models


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


ACCOUNT_CHOICES = (
    ('By','Buyer'),
    ('Sl','Seller')
   
)


class Artist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,blank = True)
    mailing_address = models.CharField(max_length = 100, verbose_name = "Mailing_Address",blank = True,null = True)
    instagram = models.URLField(max_length = 200,blank = True,null = True)
    facebook = models.URLField(max_length = 200,blank = True,null = True)
    twitter = models.URLField(max_length = 200,blank = True,null = True)
    image_artist = CloudinaryField("Profile",default = 'https://res.cloudinary.com/dqj36cjxw/image/upload/v1607600679/Rectangle_52_jiszkm.png')
    
    
    
    def __str__(self):
        return str(self.user.username)

    
    def get_absolute_url(self):
        return reverse ('core:profile', kwargs = {'pk':self.pk})




class Item(models.Model):
   title = models.CharField(max_length = 100,unique = True)
   price = models.FloatField()
   discount_price = models.FloatField(default = 0,blank = True,null = True)
   category = models.CharField(choices = CATEGORY_CHOICES,max_length = 2)
   label= models.CharField(choices = LABEL_CHOICES,max_length = 2)
   slug = models.SlugField(verbose_name = "Tag",unique = True)
   description = models.TextField()
   image = CloudinaryField("image") 
   artist = models.ForeignKey(Artist,on_delete = models.CASCADE,null = True)
   user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,null = True)
   date = models.DateTimeField(default=timezone.now)
   likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes' , blank =True)
   
   def __str__(self):
       return self.title


   def all_likes(self):
        return self.likes.count()

   def get_absolute_url(self):
       return reverse("core:product",kwargs = {'slug':self.slug})

   def get_add_to_cart_url(self):
       return reverse("core:add-to-cart",kwargs = {'slug':self.slug})

   def get_remove_from_cart_url(self):
       return reverse("core:remove-from-cart",kwargs = {'slug':self.slug})
   def get_with(self):
        return self.price - self.discount_price
   
   @classmethod
   def search_by_title(cls,search_term):
        item = cls.objects.filter(title__icontains=search_term)
        return item

   
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    ordered = models.BooleanField(default = False)
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    status = models.BooleanField(default = False)
    quantity = models.IntegerField(default =1)

  

    def __str__(self):
       return f"{self.quantity}  {self.item.title}" 

  

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount_price


    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_another(self):
        return self.get_amount_saved() * self.quantity

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_amount_saved()

        return self.get_total_item_price()


       
    

    
class Order(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True) 
    date_ordered = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    billing_adress = models.ForeignKey('BillingAdress',on_delete = models.SET_NULL,blank=True,null= True)
    payment= models.ForeignKey('Payment',on_delete = models.SET_NULL,blank=True,null= True)


    def __str__(self):
        return str(self.id)
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total+=order_item.get_final_price()
        return total

class BillingAdress(models.Model):

   user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
   street_adress = models.CharField(max_length = 200)
   apartment_adress = models.CharField(max_length = 200)
   zip = models.CharField(max_length = 200)
   country = CountryField(multiple = False)

   def __str__(self):
       return self.user.username

class PaymentDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.SET_NULL,blank = True,null = True)
    name = models.CharField(max_length = 100,blank = True,null = True)
    cardno = models.CharField(max_length = 100,blank = True,null = True,verbose_name = "Card Number")
    expiry_date = models.DateField(blank = True,null = True)
    billing_adress = models.CharField(max_length = 100,blank = True,null = True)
    CITY= models.CharField(max_length = 100,blank = True,null = True,verbose_name = "City")

    

    def __str__(self):
        return str(self.name)

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.SET_NULL,blank = True,null = True)
    stripe_charge_id = models.CharField(max_length = 100)
    amount = models.FloatField()
    
    billing_adress = models.ForeignKey('BillingAdress',on_delete = models.SET_NULL,blank=True,null= True)

    def __str__(self):
        return str(self.amount)


class Chat(models.Model):
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "To",related_name='send_to',  on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', on_delete=models.CASCADE,null=True)
    message = models.TextField( null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.message

    @property
    def number_of_chats(self):
        return Chat.objects.all().count()

class Show(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length = 100)
    date = models.DateField()
    time = models.TimeField()
    location =  models.CharField(max_length = 100)
    RSVP = models.CharField(max_length = 100)
    poster = CloudinaryField("Poster",default = "https://res.cloudinary.com/dqj36cjxw/image/upload/v1609854605/uis0nvmmwdkfkhydtenu.jpg")

    def __str__(self):
       return self.title 


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    buyer = models.BooleanField(default = False)
    seller = models.BooleanField(default = False)
    

    def __str__(self):
       return self.user.username


class Gallery(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    host_name = models.CharField(max_length = 100,blank = True,null = True)
    gallery_email = models.CharField(max_length = 100,blank = True,null = True)
    gallery_number = models.CharField(max_length = 100,blank = True,null = True)
    gallery_address = models.CharField(max_length = 100,blank = True,null = True)
    city_state_zip_code = models.CharField(max_length = 100,blank = True,null = True)
    gallery_website = models.CharField(max_length = 100,blank = True,null = True)
    
    

    def __str__(self):
       return self.host_name



class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length = 100,blank = True,null = True)
    phone = models.CharField(max_length = 100,blank = True,null = True)
    address = models.CharField(max_length = 100,blank = True,null = True)
    description = models.TextField(max_length = 100,blank = True,null = True)
    country = CountryField(multiple = False,blank = True,null = True)

    def __str__(self):
       return self.name

   
    


    

    




from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

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
class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 100,blank = True,null = True)
    last_name = models.CharField(max_length = 100,blank = True,null = True)
    email = models.CharField(max_length = 200,blank = True,null = True)
    bio = models.CharField(max_length = 200,blank = True,null = True)
    Adress = models.CharField(max_length = 200,blank = True,null = True)
    phone = models.CharField(max_length = 200,blank = True,null = True)
    instagram = models.URLField(max_length = 200,blank = True,null = True)
    facebook = models.URLField(max_length = 200,blank = True,null = True)
    tweeter = models.URLField(max_length = 200,blank = True,null = True)
    slug = models.SlugField()
    image_artist = models.ImageField(upload_to = "images/",default = "https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/12.jpg")
    
    def __str__(self):
       return self.first_name

    def get_absolute_url(self):
       return reverse("core:profile",kwargs = {'slug':self.slug})


class Item(models.Model):
   title = models.CharField(max_length = 100)
   price = models.FloatField()
   discount_price = models.FloatField(blank = True,null = True)
   category = models.CharField(choices = CATEGORY_CHOICES,max_length = 2)
   label= models.CharField(choices = LABEL_CHOICES,max_length = 2)
   artist = models.ForeignKey(Artist,on_delete = models.CASCADE,null= True)
   slug = models.SlugField(default = 'please enter a tag...')
   description = models.TextField()
   image = models.ImageField(upload_to = "images/",default = "https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/12.jpg")
   

   def __str__(self):
       return self.title
    
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


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.SET_NULL,blank = True,null = True)
    stripe_charge_id = models.CharField(max_length = 100)
    amount = models.FloatField()
    time_stamp = models.DateTimeField(auto_now_add = True)
    billing_adress = models.ForeignKey('BillingAdress',on_delete = models.SET_NULL,blank=True,null= True)

    def __str__(self):
        return str(self.amount)
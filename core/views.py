from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.utils import timezone
from .models import Order,OrderItem,Item,BillingAdress,Payment,CATEGORY_CHOICES,Artist
from django.views.generic import ListView,DetailView,View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .forms import CheckoutForm,UserProfileForm,UserUpdateForm,UploadForm
from allauth.account.views import PasswordResetView
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest
from django.middleware.csrf import get_token
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer,ArtistSerializer,ItemSerializer

import stripe

stripe.api_key =  settings.STRIPE_SECRET_KEY
def is_users(item_user, logged_user):
    return item_user == logged_user



class CheckoutView(View):
    def get(self,*args,**kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user = self.request.user,ordered = False)
        context = {
            'form':form,
            'object':order
        }
     
        return render(self.request,'checkout-page.html',context)
        
        
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:

           order = Order.objects.get(user = self.request.user,ordered = False)
           if form.is_valid():
            
              street_adress = form.cleaned_data.get('street_adress')
              apartment_adress = form.cleaned_data.get('apartment_adress')
              country = form.cleaned_data.get('country')
              zip = form.cleaned_data.get('zip')
              same_shipping_adress = form.cleaned_data.get('same_shipping_adress')
              save_info = form.cleaned_data.get('save_info')
              payment_option = form.cleaned_data.get('payment_option')
              billing_adress = BillingAdress(
                user = self.request.user,
                street_adress = street_adress,
                apartment_adress = apartment_adress,
                country = country,
              )
              billing_adress.save()
              order.billing_adress = billing_adress
              order.save()
              if payment_option == "S":

                  return redirect('core:payment',payment_option = "stripe")

              elif payment_option == "P":
                  return redirect('core:payment',payment_option = "paypal")

              else:

                return redirect('core:checkout')
        
        except ObjectDoesNotExist:
            
            return redirect("core:order-summary")

       

        return redirect('core:checkout')




class CreateDetail(LoginRequiredMixin,CreateView):
    model = Item
    template_name = "item.html"
    fields = ['title','price','discount_price','category','label','slug','description','image']

    def load_profile(user):
        try:
         return user.artist
        except:  
         artist = Artist.objects.create(user=user)


    def form_valid(self,form):
        artist= load_profile(self.request.user)
        
        form.instance.user = self.request.user
        
        
        return super().form_valid(form)
  


      



class homeview(ListView):
    model = Item
    paginate_by = 6
    template_name = "home-page.html"

    def get_context_data(self, **kwargs):
        context = super(homeview, self).get_context_data(**kwargs)
        context['products'] = Item.objects.distinct('user')
        return context



    

class artists(ListView):
    model = Item
    template_name = "artist.html"
    def get_context_data(self, **kwargs):
        context = super(artists, self).get_context_data(**kwargs)
        context['products'] = Item.objects.distinct('user')
        return context


def load_profile(user):
  try:
    return user.artist
  except:  
    artist = Artist.objects.create(user=user)
    return artist

@login_required
def myprofile(request):
    artist= load_profile(request.user)
    if request.method == 'POST':

        u_form =  UserUpdateForm(request.POST,instance = request.user)
        p_form = UserProfileForm(request.POST,request.FILES,instance = request.user.artist)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('core:myprofile')
    else:
        u_form =  UserUpdateForm(instance = request.user)
        p_form = UserProfileForm(instance = request.user.artist)
    

    context ={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'myprofile.html',context)



def paintingsview(request):

    context = {
        'items':Item.objects.filter(category ='Pa')
    }
    return render(request,'paintings.html',context)

def photographsview(request):

    context = {
        'items':Item.objects.filter(category ='Ph')
    }
    return render(request,'photographs.html',context)

def prints(request):

    context = {
        'items':Item.objects.filter(category ='pr')
    }
    return render(request,'prints.html',context)

def sculptures(request):

    context = {
        'items':Item.objects.filter(category ='sc')
    }
    return render(request,'sculptures.html',context)
   
class profile(DetailView):

    model = Artist
    template_name = "profile.html"
    def get_context_data(self, **kwargs):
        context = super(profile, self).get_context_data(**kwargs)
        context['products'] = Item.objects.all()
        return context
    
    

def productview(request):
   context = {
       'items':Item.objects.all()
   }
   return render(request,'product-page.html',context)


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:

           order = Order.objects.get(user = self.request.user,ordered = False)
           context = {
               'object':order
           }
        except ObjectDoesNotExist:
            return redirect("/")
        return render(self.request,'order_summary.html',context)
    

class itemdetailview(DetailView):
    model = Item
    template_name = "product-page.html"
    def get_context_data(self, **kwargs):
        context = super(itemdetailview, self).get_context_data(**kwargs)
        context['products'] = Item.objects.all()
        return context


@login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)
    order_item,created= OrderItem.objects.get_or_create(item=item,user = request.user,ordered = False)
    order_qs = Order.objects.filter(user = request.user,ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            
            return redirect('core:order-summary')
            
        else:
            
            order.items.add(order_item)
            return redirect('core:order-summary')
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(user = request.user,date_ordered =date_ordered )
        order.items.add(order_item)
        return redirect('core:order-summary')

    return redirect('core:product',slug = slug)

@login_required   
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)

    order_qs = Order.objects.filter(user = request.user,ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user = request.user,ordered = False)[0]
            order.items.remove(order_item)
            
            return redirect('core:order-summary')
        else:
            
            
            return redirect('core:product',slug = slug)

    else:
       
        return redirect('core:product',slug = slug)
      
    return redirect('core:product',slug = slug)

@login_required   
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug = slug)

    order_qs = Order.objects.filter(user = request.user,ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,user = request.user,ordered = False)[0]
            if order_item.quantity > 1:
               order_item.quantity -=1
               order_item.save()
            else:
                order.items.remove(order_item)
            order_item.save()
            
            return redirect('core:order-summary')
        else:
            
            
            return redirect('core:product',slug = slug)

    else:
        
        return redirect('core:product',slug = slug)
      
    return redirect('core:product',slug = slug)


class PaymentView(View):
    def get(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered = False)

        context = {

            'order':order
        }

        return render(self.request ,'payment.html',context)

    def post(self,*args,**kwargs):
        order = Order.objects.get(user = self.request.user,ordered = False)
        token = self.request.POST.get('stripeToken')
        amount= int(order.get_total()*100)

        try:
         charge = stripe.Charge.create(
            amount= amount,
            currency="usd",
            source=token
           
            )
           # first create the payment
         payment = Payment()
         payment.stripe_charge_id = charge['id'] 
         payment_user = self.request.user
         payment.amount = order.get_total()
         payment.save()

         # assign the payment to the order
         order_items = order.items.all()
         order_items.update(ordered = True)
         for item in order_items:
             item.save()
             
         order.ordered = True
         order.payment = payment
         order.save()
         messages.success(self.request,'Your order was succesful')
         return redirect('/')
           
        except stripe.error.CardError as e:
       

            body = e.json_body
            err = body.get('error',{})
            messages.error(self.request,f"{err.get('message')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
          messages.error(self.request,'Rate Limit Error')
          return redirect('/')
         
        except stripe.error.InvalidRequestError as e:
          messages.error(self.request,'Invalid Parameters')
          return redirect('/')
        # Invalid parameters were supplied to Stripe's API
          
        except stripe.error.AuthenticationError as e:
          messages.error(self.request,'Not Authenticated')
          return redirect('/')
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        
        except stripe.error.APIConnectionError as e:
          messages.error(self.request,'Network Error')
          return redirect('/')
        # Network communication with Stripe failed
     
        except stripe.error.StripeError as e:
          messages.error(self.request,'Something went wrong,you were not charged,Please try again')
          return redirect('/')
        # Display a very generic error to the user, and maybe send
        # yourself an email
    
        except Exception as e:
        # Something else happened, completely unrelated to Stripe
           messages.error(self.request,'A  serious error occured,we have been notified')
           return redirect('/')
   


       
        
def search_results(request):

    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_items = Item.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"items": searched_items})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})



class ItemList(APIView):
    def get(self, request, format=None):
        all_items= Item.objects.all()
        serializers = ItemSerializer(all_items, many=True)
        return Response(serializers.data)

class ArtistList(APIView):
    def get(self, request, format=None):
        all_items= Item.objects.all()
        serializers = ArtistSerializer(all_items, many=True)
        return Response(serializers.data)
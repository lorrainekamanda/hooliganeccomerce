from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from django.utils import timezone
from .models import Order,OrderItem,Item,BillingAdress,Payment,Artist,PaymentDetails,Chat,Show
from django.views.generic import ListView,DetailView,View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .forms import CheckoutForm,UserProfileForm,UserUpdateForm,UploadForm,AdressForm,PaymentForm,ComposeForm,ChatForm,ShowForm,UserImageForm
from allauth.account.views import PasswordResetView
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpRequest,Http404,HttpResponseRedirect,JsonResponse,HttpResponseForbidden
from django.middleware.csrf import get_token
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer,ArtistSerializer,ItemSerializer
from rest_framework import generics
from django.contrib.auth import get_user_model
import stripe
from django.views.generic import TemplateView,DetailView, ListView
from django.views import View
from django.shortcuts import render_to_response
import json
from django.views import generic

from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.safestring import mark_safe
import json
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput
from django import forms
from django.forms.widgets import SelectDateWidget



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




      
def like(request):


    data = json.loads(request.body)

    itemId = data['itemId']
    action = data['action'] 
    item = Item.objects.get(id =itemId)
    data = {}

    if item.likes.filter(id = request.user.id).exists():
        item.likes.remove(request.user)
        data = {'is_liked':False}
          
        
    else:
        item.likes.add(request.user)
        data = {'is_liked':True}


    print(itemId)
    print(action)


    return JsonResponse(data)



class homeview(ListView):
    model = Item
    paginate_by = 6
    template_name = "home-page.html"

    def get_context_data(self, **kwargs):
        context = super(homeview, self).get_context_data(**kwargs)
        context['products'] = Item.objects.distinct('user')
        context['shows'] = Show.objects.all()
        return context

    def latest_artwork (self):
        
        return Item.objects.latest('date')

    



    

class artists(ListView):
    model = Item
    template_name = "artist.html"
    def get_context_data(self, **kwargs):
        context = super(artists, self).get_context_data(**kwargs)
        context['products'] = Item.objects.distinct('user')
        return context

    def latest_artwork (self):
        
        return Item.objects.latest('date')


    


def load_profile(user):
  try:
    return user.artist
  except:  
    artist = Artist.objects.create(user=user)
    return artist

def load_payment(user):
  try:
    return user.paymentdetails
  except:  
   paymentdetails = PaymentDetails.objects.create(user=user)
   return paymentdetails
class myprofile(View):

    
    template_name = 'myprofile.html'
   

    def get(self, request): 
        artist= load_profile(request.user)
        paymentdetails = load_payment(request.user)
        u_form =  UserUpdateForm(instance = request.user)
        
        p_form = UserProfileForm(instance = request.user.artist)
        d_form = PaymentForm(instance = request.user.paymentdetails)
        a_form = UploadForm(instance = request.user)
       
        products = Item.objects.filter(likes = self.request.user)
        order_items = OrderItem.objects.filter(user = self.request.user,ordered = True)
         
        return render(request, self.template_name, {'u_form': u_form,'p_form': p_form,'d_form': d_form,'object':order_items,'products':products,'a_form':a_form}) 



    def post(self, request): 
        artist= load_profile(request.user)
        paymentdetails = load_payment(request.user)
        u_form = UserUpdateForm(request.POST,instance = request.user)
       
        d_form = PaymentForm(request.POST,instance = request.user.paymentdetails)
        p_form = UserProfileForm(request.POST,request.FILES,instance = request.user.artist)
        if u_form.is_valid() and p_form.is_valid(): 
            # Success! We can use form.cleaned_data now 
            u_form.save()
            p_form.save()
            return redirect('core:myprofile') 

        elif d_form.is_valid(): 
            
            d_form.save()
            return redirect('core:myprofile')

        

        else:
            d_form = PaymentForm(request.POST,instance = request.user.paymentdetails)
            
       

       
            return render_to_response(request, 'myprofile.html', {'d_form':d_form})
            

    def get_context_data(self, **kwargs):
        context = super(myprofile, self).get_context_data(**kwargs)
        context['products'] = Item.objects.all()
        return context
   

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
        context['shows'] = Show.objects.all()
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






class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class   ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ArtistList(APIView):
    def get(self, request, format=None):
        all_items= Item.objects.all()
        serializers = ArtistSerializer(all_items, many=True)
        return Response(serializers.data)


class UserList(generics.ListCreateAPIView):
    User =  get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    User =  get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer




class InboxView(LoginRequiredMixin, ListView):
    template_name = 'inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)



class MessageView(View):
    def get(self,request):
        form = ChatForm()
        form.instance.user = self.request.user
        chats = Chat.objects.all()
        context = {
            'form':form,
            'chats':chats
        }
     
        return render(self.request,'message.html',context)
        
        
    def post(self,request):
        form = ChatForm(self.request.POST or None)
        form.instance.user = self.request.user
        chats = Chat.objects.all()
        if form.is_valid():
            
            form.save()
            return redirect('core:message')


class CreateShow(View):
    def get(self,request):
        form = ShowForm()
        form.instance.user = self.request.user
       
        context = {
            'form':form,
           
        }
     
        return render(self.request,'show.html',context)
        
        
    def post(self,request):
        form = ShowForm(self.request.POST or None)
        form.instance.user = self.request.user
        
        if form.is_valid():
            
            form.save()
            return redirect('/')

        else:
            return render(request, 'show.html', {'form':form})


class UpdateDetail(LoginRequiredMixin,UpdateView):
    model = Item
    template_name = 'uitem.html'
    fields = ['title','price','discount_price','category','label','slug','description','image']
    def test_func(self):
        item = self.get_object()
        


    def form_valid(self,form):
        form.instance.username = self.request.user
        return super().form_valid(form)


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'ditem.html'
    context_object_name = 'image'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().username, self.request.user)






class UpdateShow(LoginRequiredMixin,UpdateView):
    model = Show
    template_name = 'ushow.html'
    
    form_class = ShowForm
    success_url = '/'
   
    def test_func(self):
        item = self.get_object()
        


    def form_valid(self,form):
        form.instance.username = self.request.user
        return super().form_valid(form)

class ShowDelete(LoginRequiredMixin, DeleteView):
    model = Show
    template_name = 'dshow.html'
    context_object_name = 'image'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().username, self.request.user)
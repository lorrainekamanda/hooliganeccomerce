from .models import Order,OrderItem,Item,BillingAdress,Payment,CATEGORY_CHOICES,Artist
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('first_name','last_name','username','email','password','artist')

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('user','profession','bio','focus','about_your_work','phone','instagram','facebook','tweeter')



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title','price','discount_price','description','user','artist','category','slug','label','date','image')
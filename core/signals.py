from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Artist
from django.conf import settings
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up

# User = get_user_model()
# @receiver(post_save,sender = User)
# def create_artist(sender,instance,created,**kwargs):
#     if created:
#         Artist.objects.create(user = instance)
         
# @receiver(post_save,sender = User)
# def save_artist(sender,instance,**kwargs):
#     instance.artist.save()

@receiver(user_signed_up)
def after_user_signed_up(request, user):

    artist = Artist.objects.create(user=user.username,bio = 'My mystrey') 
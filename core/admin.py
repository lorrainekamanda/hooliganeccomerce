from django.contrib import admin

from .models import Order,OrderItem,Item,BillingAdress,Payment,Artist,Profile

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

admin.site.register(Order,OrderAdmin)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(BillingAdress)
admin.site.register(Payment)
admin.site.register(Artist)
admin.site.register(Profile)
from django.contrib import admin

from .models import Order,OrderItem,Item,BillingAdress,Payment,Artist,PaymentDetails,Chat,Show,Account,Seller,Blog,Comments

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

class ItemAdmin(admin.ModelAdmin):
    filter_horizontal =('likes',)





admin.site.register(Order,OrderAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(BillingAdress)
admin.site.register(Payment)
admin.site.register(Artist)
admin.site.register(PaymentDetails)
admin.site.register(Chat)
admin.site.register(Show)
admin.site.register(Account)
admin.site.register(Seller)
admin.site.register(Blog)
admin.site.register(Comments)
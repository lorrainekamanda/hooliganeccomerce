from django.urls import path,re_path
from .views import homeview,itemdetailview,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_item_from_cart,CheckoutView,PaymentView,search_results,productview,paintingsview,photographsview,prints,profile,artists,CreateDetail,sculptures,myprofile,ItemList,ArtistList,ItemDetail,UserList,UserDetail,MessageView,CreateShow,UpdateDetail,ItemDelete,UpdateShow,ShowDelete,Account,SummaryView,blog,BlogDetail,UpdateBlog,DeleteBlog
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'core'


urlpatterns = [
    path('',homeview.as_view(),name = 'home'),
    path('artists/',artists.as_view(),name = 'artists'),
    path('items',productview,name = 'items'),
    path('checkout/',CheckoutView.as_view(),name = 'checkout'),
    path('paintings/',paintingsview,name = 'paintings'),
    path('prints/',prints,name = 'prints'),
    path('profile/<int:pk>/',profile.as_view(),name = 'profile'),
    path('photographs/',photographsview,name = 'phtotographs'),
    path('myprofile/',myprofile.as_view(),name = 'myprofile'),
    path('sculptures/',sculptures,name = 'sculptures'),
    path('order-summary/',OrderSummaryView.as_view(),name = 'order-summary'),
    path('product/<slug>/',itemdetailview.as_view(),name = 'product'),
    path('add-to-cart/<slug>/',add_to_cart,name = 'add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name = 'remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/',remove_single_item_from_cart,name = 'remove-single-item-from-cart'),
    path('payment/<payment_option>/',PaymentView.as_view(),name = 'payment'),
    path('search/',views.search_results, name='search_results'),
    path('upload/', CreateDetail.as_view(), name = 'upload'),
    path('show/', CreateShow.as_view(), name = 'show'),
    path('api-item/', ItemList.as_view(), name = 'api-item'),
    path('api-item/<int:pk>/', views.ItemDetail.as_view()),
    path('api-user/', UserList.as_view(), name = 'api-user'),
    path('api-user/<int:pk>/', views.UserDetail.as_view()),
    path('api-artist/', ArtistList.as_view(), name = 'api-artist'),
    path('like/', views.like , name= 'like'),
    path('message/', MessageView.as_view() , name= 'message'),
    path('product/<slug>/update', UpdateDetail.as_view(), name = 'product-update'),
    path('product/<slug>/delete',ItemDelete.as_view(), name = 'product-delete'),
    path('<int:pk>/update', UpdateShow.as_view(), name = 'show-update'),
    path('<int:pk>/delete', ShowDelete.as_view(), name = 'show-delete'),
    path('seller-account/',Account.as_view() , name= 'seller-account'),
    path('summary-view/',SummaryView.as_view() , name= 'summary-view'),
    path('blog/',blog.as_view() , name= 'blog'),
    path('blog/<int:pk>/', BlogDetail.as_view(), name = 'blog-detail'),
    path('blog/<int:pk>/update', UpdateBlog.as_view(), name = 'update-blog'),
    path('blog/<int:pk>/delete', DeleteBlog.as_view(), name = 'delete-blog'),
    path('searches/',views.search_result, name='search_result'),
    

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
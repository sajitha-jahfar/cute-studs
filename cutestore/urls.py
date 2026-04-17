from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('orders/', views.order_history, name='orders'),
    path('', auth_views.LoginView.as_view(), name='login'),  
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    # path('payment/<int:order_id>/', views.online_payment, name='online_payment'),
    path('order_success/',views.order_success,name='order_success'),
]
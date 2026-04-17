
from django.shortcuts import render, redirect, get_object_or_404


import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY


from .models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required(login_url='/')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})



# def add_to_cart(request, product_id):
#     return redirect('home')



def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })

def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


def remove_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')




def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')




stripe.api_key = settings.STRIPE_SECRET_KEY

# def checkout(request):

#     cart = Cart.objects.get(user=request.user)
#     items = CartItem.objects.filter(cart=cart)

#     total = sum(item.product.price * item.quantity for item in items)

    
#     order = Order.objects.create(
#         user=request.user,
#         total_amount=total,
#         status='PENDING'
#     )

#     line_items = []

#     for item in items:
#         line_items.append({
#             'price_data': {
#                 'currency': 'inr',
#                 'product_data': {
#                     'name': item.product.name,
#                 },
#                 'unit_amount': item.product.price * 100,
#             },
#             'quantity': item.quantity,
#         })

#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url=f'http://127.0.0.1:8000/success/?order_id={order.id}',
#         cancel_url='http://127.0.0.1:8000/cancel/',
#     )

#     return redirect(session.url)

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
def order_success(request):
    return render(request,'ordersuccess.html')


def success(request):
    order_id = request.GET.get('order_id')

  
    order = Order.objects.get(id=order_id)

  
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(user=request.user)

   
    if not items:
        print("Cart is empty!")

   
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

  
    order.status = 'PAID'
    order.save()

   
    items.delete()

    return render(request, 'success.html')
   

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'signup.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from .models import CartItem, Order, OrderItem

def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            name=name,
            address=address,
            phone=phone,
            payment_method=payment_method,
            status='Pending'
        )

        # COD flow
        if payment_method == 'cod':
            order.status = 'Placed'
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()
            return redirect('order_success')

        # ONLINE PAYMENT (Stripe)
        else:
            line_items = []

            for item in cart_items:
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': item.product.price * 100,
                    },
                    'quantity': item.quantity,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f'http://127.0.0.1:8000/success/?order_id={order.id}',
                cancel_url='http://127.0.0.1:8000/cancel/',
            )

            return redirect(session.url)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })

# def online_payment(request, order_id):
#     order = Order.objects.get(id=order_id)

#     if request.method == 'POST':
#         order.status = 'Paid'
#         order.save()

#         CartItem.objects.filter(user=request.user).delete()

#         return redirect('checkout')

#     return render(request, 'success.html', {'order': order})
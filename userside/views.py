from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItems
from admins.models import books

# Create your views here.
def cart(request):
    
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItems.objects.filter(cart=cart)
 
    return render(request,'usertemplate/cart.html',{'cart_items':cart_item})

def add_cart(request,book_id):
    user=request.user
    cart, created = Cart.objects.get_or_create(user=user)
    book = get_object_or_404(books,id=book_id)
    cart_items,item_created = CartItems.objects.get_or_create(
        cart = cart,
        book = book,
        defaults={'quantity':1}
        
    )
    cart_items.save()
    return redirect('hanldesingleproduct',product_id=book_id)
    



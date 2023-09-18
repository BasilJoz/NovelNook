from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import Cart, CartItems
from admins.models import books
from logins.models import user_details
from logins.models import Address
from .models import Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='login')
def cart(request):
    
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItems.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.book.price for item in cart_item)
    
    return render(request,'usertemplate/cart.html',{'cart_items':cart_item,'total_price':total_price})

from django.http import JsonResponse

# ...

def update_cart_item_quantity(request, item_id):
    # Get the cart item
    cart_item = get_object_or_404(CartItems, id=item_id)

    # Check if the request is a POST request
    if request.method == 'POST':
        new_quantity = int(request.POST['new_quantity'])

        # Update the quantity of the cart item
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()

            # Calculate the updated total price (if needed)
            cart = cart_item.cart
            cart_item_list = CartItems.objects.filter(cart=cart)
            total_price = sum(item.quantity * item.book.price for item in cart_item_list)

            # Return a JSON response with the updated data
            return JsonResponse({'success': True, 'total_price': total_price})

    # Return a JSON response for errors (if needed)
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required(login_url='login')
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


def delete_cart_item(request, item_id):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_item = get_object_or_404(CartItems, id=item_id, cart=cart)
    
    # Remove the item from the cart
    cart_item.delete()
    
    return redirect('cart')  

#profile handleing section


@login_required(login_url='login')
def userprofile(request):
    user = request.user
    print(user,"ukyfyuuu")

    if "first_name" in request.POST:
        edited_fist_name = request.POST["first_name"]
        user.first_name = edited_fist_name
        user.save()
    if "last_name" in request.POST:
        edited_last_name = request.POST["last_name"]
        user.last_name = edited_last_name
        user.save()
    if "gender" in request.POST:
        edited_gender = request.POST["gender"]
        user.gender = edited_gender
        user.save()
    if "age" in request.POST:
        edited_age = request.POST["age"]
        user.age = edited_age
        user.save()
    if "email" in request.POST:
        edited_email = request.POST["email"]
        user.email = edited_email
        user.save()

    return render(
        request,
        "usertemplate/userprofile.html",
        {
            "username": user.username,
            "email": user.email,
            "phone": user.phone_number,
            "age": user.age,
            "gender": user.gender,
            "first_name": user.first_name,
            "last_name": user.last_name,})
    
def useraddress(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    address = Address.objects.filter(user=user)
    
    return render(request,'usertemplate/useraddress.html',{'addresses':address})

def add_address(request):
    
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        print("dskjhfsdaklhaslkhfaslkhklasfh")
        housename_companyname = request.POST.get("Housename_companyname")
        post_office = request.POST.get("Post_office")
        street = request.POST.get("Street")
        city = request.POST.get("City")
        state = request.POST.get("State")
        country = request.POST.get("Country")
        pin_code = request.POST.get("Pin_code")

        address = Address(
            user=request.user,
            name=housename_companyname,
            postoffice=post_office,
            street=street,
            city=city,
            state=state,
            country=country,
            pin_code=pin_code,
        )
        address.save()
        print("Saved Address Details:")
        print("Name:", address.name)
        print("Post Office:", address.postoffice)
        print("Street:", address.street)
        print("City:", address.city)
        print("State:", address.state)
        print("Country:", address.country)
        print("Pin Code:", address.pin_code)
        
        next_url = request.GET.get('next', None)
        
        
        if next_url:
            return redirect(next_url)
        else:
            return redirect('useraddress')

    
    return render(request,'usertemplate/add_address.html')


def edit_address(request, edit_id):
    if not request.user.is_authenticated:
        return redirect("login")
    

    address = get_object_or_404(Address, id=edit_id, user=request.user)

    if request.method == "POST":
        housename_companyname = request.POST.get("Edited_Housename_companyname")
        post_office = request.POST.get("Edited_Post_office")
        street = request.POST.get("Edited_Street")
        city = request.POST.get("Edited_City")
        state = request.POST.get("Edited_State")
        country = request.POST.get("Edited_Country")
        pin_code = request.POST.get("Edited_Pin_code")

        address.name = housename_companyname
        address.postoffice = post_office
        address.street = street
        address.city = city
        address.state = state
        address.country = country
        address.pin_code = pin_code
        address.save()

        next_url = request.GET.get('next', None)
       
        if next_url:
            print(next_url)
            return redirect(next_url)
        else:
            return redirect('useraddress')
    

    return render(request, "usertemplate/edit_address.html", {"address": address})


def delete_address(request, del_id):
    address = get_object_or_404(Address, id=del_id)
    address.delete()
    return redirect("useraddress")

def checkout(request):
    
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user
    addresses = Address.objects.filter(user=user)
    cart_items_param = request.GET.get("cart_items")

    selected_address_id = None
    order = None

    if request.method == "POST":
        cart = Cart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)
        selected_address_id = request.POST.get("selected_address")

        if selected_address_id:
            address = Address.objects.get(id=selected_address_id)
            payment_method = "Cash On Delivery"

            total_price = 0

            for item in cart_items:
                print('jhjkghjkgjkgjkgjkg')
                item.offer_price = item.book.offer_price
                item.total_price_each = item.offer_price * item.quantity

                total_price += item.total_price_each
                print(total_price,'jgjggkjghkjgkjgkjgjk')

            total_price_shipping = total_price + 50

            order = Order.objects.create(
                user=user,
                address=address,
                payment_method=payment_method,
                total_price=total_price,
                total_price_shipping=total_price_shipping,
            )

            for item in cart_items:
                product = item.book
                quantity = item.quantity
                book = product

                if book.quantity >= quantity:
                    book.quantity -= quantity
                    book.save()
                    
                    OrderItem.objects.create(
                        order=order,
                        product=book,
                        quantity=quantity,
                    )
                else:
                    pass

            cart_items.delete()

            return redirect(
                "order_summary", address_id=selected_address_id, order_id=order.id
            )

    if cart_items_param == "true":
        cart = Cart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)

        total_price = 0
        for item in cart_items:
            item.offer_price = item.book.offer_price
            item.total_price_each = item.offer_price * item.quantity
            total_price += item.total_price_each

        final_total = total_price + 50

        return render(
            request,
            "usertemplate/checkout.html",
            {
                "addresses": addresses,
                "cart_items": cart_items,
                "total_price": total_price,
                "final_total": final_total,
                "address_id": selected_address_id,
            },
        )

    return render(
        request,
        'usertemplate/checkout.html',
        {"addresses": addresses, "address_id": selected_address_id},
    )
    
   
   
def order_summary(request, address_id, order_id):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    address = Address.objects.get(id=address_id)
    username = user.username

    orders = Order.objects.get(id=order_id, address=address)
    order_items = OrderItem.objects.filter(order=orders)

    context = {
        "address": address,
        "username": username,
        "orders": orders,
        "order_items": order_items,
        
    }

    return render(request, "usertemplate/order_summary.html", context) 

def my_orders(request):
    
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    orders = Order.objects.filter(user=user)

    order_items = OrderItem.objects.filter(order__in=orders).order_by("-id")

    return render(request, "usertemplate/my_orders.html", {"order_items": order_items})

def cancel_order(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

    if order_item:
        order_item.order_status = "Cancelled"
        order_item.save()

    return redirect("my_orders")








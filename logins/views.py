from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import user_details
from django.contrib import auth
from . import verify
from admins.models import books
from django.contrib.auth.hashers import make_password



# Create your views here.
def home(request):
    print(request.user,'newone')
    book =  books.objects.filter(deleted = False)[:4]
    
    
    return render(request, "usertemplate/home.html",{'best_seller':book})


def handlelogin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password =request.POST['password']
        # print('email','password')
        try:
            user = user_details.objects.get(email=email)
            password_matched = user.check_password(password)
            print(user)
            print(password_matched)
        except:
            messages.error(request,'Invalid email or password')
            return redirect('login')
        if user and password_matched:
            print(1)
            auth.login(request,user)
            return redirect('home')
        else:
           messages.error(request,'Invalid email or password')
           return redirect('login')
    else:
        return render(request,'usertemplate/login.html')

    


def handlesignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("number")
        password = request.POST.get("pass1")
        conformpassword = request.POST.get("pass2")
        if password != conformpassword:
            messages.warning(request, "Password is incorrect")
        try:
            if user_details.objects.get(username=username):
                messages.info(request, "username is already taken")
                return redirect("signup")
        except:
            pass

        try:
            if user_details.objects.get(email=email):
                messages.info(request, "email is already taken")
                return redirect("signup")
        except:
            pass

        user = user_details.objects.create(
            username=username, email=email, phone_number=phone
        )
        user.set_password(password)
        user.save()
        auth.login(request, user)
        verify.send(user.phone_number)
        messages.success(request, "Signup sucessfully completed")
        return redirect("Otp", phone, user.id)
    return render(request, "usertemplate/signup.html")


def Otp(request, phone, id):
    user = get_object_or_404(user_details, id=id)

    if request.method == "POST":
        code = request.POST.get("otp")

        if verify.check(phone, code):
            user.is_verified = True
            user.save()
            return redirect("login")
        else:
            user.delete()
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("signup")
    else:
        return render(request, "usertemplate/otp.html", {"phone": phone, "id": id})

def handleshop(request):
    book =  books.objects.filter(deleted = False)
    
    
    return render(request, "usertemplate/shop.html",{'best_seller':book})

    # return render(request,"usertemplate/shop.html")

def Logout(request):
    if user_details.is_authenticated:
        auth.logout(request)
        return redirect("login")
    
def hanldesingleproduct(request,product_id):
    product = books.objects.get(id=product_id)
    
    return render(request,"usertemplate/singlepage.html",{'products':product})

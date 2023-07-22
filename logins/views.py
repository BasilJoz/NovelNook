from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import user_details
from django.contrib import auth


# Create your views here.
def home(request):
    return render(request,'usertemplate/home.html')

def handlelogin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password =request.POST['password']
        # print('email','password')
        try:
            user = user_details.objects.get(email=email)
            password_matched = user.check_password(password)
            print('database password',user.password,'password',password)
        except:
            print('database password',user.password,'password',password)
            return redirect('login')
        if user and password_matched:
            auth.login(request,user)
            return redirect('home')
    else:
        return render(request,'usertemplate/login.html')
                
                
        
    # return render(request,'usertemplate/login.html')
def handlsignup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('number')
        password=request.POST.get('pass1')
        conformpassword=request.POST.get('pass2')
        if password!=conformpassword:
            messages.warning(request,'Password is incorrect')
        try:
            if user_details.objects.get(username=username):
                messages.info(request,'username is already taken')
                return redirect('signup')
        except:
            pass
        
        try:
            if user_details.objects.get(email=email):
                messages.info(request,'email is already taken')
                return redirect('signup')
        except:
            pass
  
        user = user_details.objects.create(username=username,email=email,phone_number=phone)
        user.set_password(password)
        user.save()
        
        
        messages.success(request,'signup succesfull')
        return redirect('login')
        
            
    return render(request,'usertemplate/signup.html')
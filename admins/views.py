from django.shortcuts import render,redirect,HttpResponse
from logins.models import user_details
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Category


# Create your views here.
# def handleadmin(request):
#     return render(request ,'baseadmin.html')

def hanglesignin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password =request.POST['password']
        try:
            user = User.objects.get(email=email)
            password_matched = user.check_password(password)
        except:
            return redirect('signin')
        if user and password_matched and user.is_superuser:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.warning(request,'Not a superuser')
    else:
        return render(request,'admintemplate/signin.html')

def hangleindex(request):
    return render(request,"admintemplate/index.html")

def handleuser(request):
    obj=user_details.objects.all()
    return render(request,'admintemplate/users.html',{'adm_user':obj})

def handleblock(request,id):
    adm_user = user_details.objects.get(id=id)
    adm_user.is_active =False
    adm_user.save()
    return redirect('users')

def handleunblock(request,id):
    adm_user = user_details.objects.get(id=id)
    adm_user.is_active = True
    adm_user.save()
    return redirect('users')

def handlecategory(request):
    adm_category = Category.objects.all().order_by('id')
    return render(request,'admintemplate/category.html',{'categories':adm_category})

def add_category(request):
    if request.method == 'POST':
        cat_name = request.POST['category_name']
        if cat_name:
            existing_category = Category.objects.filter(name=cat_name).exists()
            if existing_category:
                messages.error(request, "Name is Already Exists.")
            else:
                category = Category(name=cat_name)
                category.save()
                return redirect('category')
    return render(request,'admintemplate/addcategory.html')

def edit_category(request,id):

    cat_obj = Category.objects.get(id=id) 
    if request.method == 'POST':
        edit_name = request.POST.get('edited_name')
        if edit_name is not None:
            try:
                existing_category = Category.objects.get(name=edit_name)
                if existing_category.id != id:
                    messages.info(request, "Category with this name already exists.")
                    return redirect('edit_category/' + str(id))

                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('category')
            except Category.DoesNotExist:
                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('category')
    return render(request, 'admintemplate/editcategory.html', {'cat': cat_obj})

def delete_category(request,id):
    cat_obj = Category.objects.get( id=id)
    cat_obj.delete()
    return redirect('category')


    
    
    


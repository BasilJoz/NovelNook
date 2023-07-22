from django.urls import path
from logins import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.handlelogin,name='login'),
    path('signup/',views.handlesignup,name='signup')
]

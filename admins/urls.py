from django.urls import path
from admins import views

urlpatterns = [
    # path('admin',views.handleadmin,name='admin'),
    path('signin',views.hanglesignin,name='signin'),
    path('index',views.hangleindex,name='index'),
    path('users',views.handleuser,name='users'),
    path('block_user/<int:id>',views.handleblock,name='block_user'),
    path('unblock_user/<int:id>',views.handleunblock,name='unblock_user'),
    path('category',views.handlecategory,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category')
    
   
]

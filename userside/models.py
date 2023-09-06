from django.db import models
from logins.models import user_details
from admins.models import books
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"cart for {self.user.username}"

class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    book = models.ForeignKey(books,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.book.title} in cart for {self.cart.user.username}" 
    
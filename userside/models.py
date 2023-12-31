from django.db import models
from logins.models import user_details
from admins.models import books
from  logins.models import Address
from django.utils import timezone
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
    
    
class Order(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def _str_(self):
        return f"Order #{self.id} by {self.user.username} on {self.order_date}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(books, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20,
        choices=[
            ("Order Placed", "Order Placed"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ],
        default="Order Placed",
    )

    def _str_(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
    
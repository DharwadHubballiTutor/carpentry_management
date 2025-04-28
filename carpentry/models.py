from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_order_status_email

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

# carpentry/models.py
class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField()

    def __str__(self):
        return self.name

    def update_stock(self, quantity_ordered):
        """Decreases the stock when an order is placed."""
        if self.quantity_in_stock >= quantity_ordered:
            self.quantity_in_stock -= quantity_ordered
            self.save()
        else:
            raise ValueError(f"Not enough stock for {self.name}. Only {self.quantity_in_stock} items available.")



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    
    def __str__(self):
        return f"Order #{self.id} for {self.customer.name}"

    # @receiver(post_save, sender='carpentry.Order')
    # def send_status_update_email(sender, instance, **kwargs):
    #     send_order_status_email(instance)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.material.name}"

# carpentry/models.py

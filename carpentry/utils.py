# carpentry/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_order_status_email(order):
    subject = f"Your Order #{order.id} Status Update"
    message = f"Dear {order.customer.name},\n\nYour order status is now: {order.status}.\n\nThank you for choosing us!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email]
    
    send_mail(subject, message, from_email, recipient_list)

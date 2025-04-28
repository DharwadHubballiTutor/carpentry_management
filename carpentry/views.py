from django.shortcuts import render, get_object_or_404,redirect
from .models import Order, Customer, Material, OrderItem
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# carpentry/views.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Order
from .forms import *

def home(request):
    return render(request, 'home.html')

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'carpentry/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = Order.objects.prefetch_related('customer').get(id=order_id)
    orderItem=OrderItem.objects.prefetch_related('material').get(order_id=order_id)
    print(orderItem)
    return render(request, 'carpentry/order_detail.html', {'order': order,'orderItem':orderItem})

# carpentry/views.py
def create_order(request):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=request.POST['customer_id'])
        order = Order.objects.create(customer=customer, status='Pending')
        
        # Add order items
        material = get_object_or_404(Material, id=request.POST['material_id'])
        quantity = int(request.POST['quantity'])
        
        try:
            material.update_stock(quantity)
            order_item = OrderItem.objects.create(order=order, material=material, quantity=quantity)
        except ValueError as e:
            # Handle the error if there's not enough stock
            return render(request, 'carpentry/error.html', {'error_message': str(e)})

        return HttpResponseRedirect('/orders/')
    
    customers = Customer.objects.all()
    materials = Material.objects.all()
    return render(request, 'carpentry/create_order.html', {'customers': customers, 'materials': materials})



def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()
    
    # Create a response object with content-type set to PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    
    # Create the PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Invoice for Order #{order.id}")
    p.drawString(100, 730, f"Customer: {order.customer.name}")
    p.drawString(100, 710, f"Date: {order.date_placed}")
    
    y_position = 690
    p.drawString(100, y_position, "Materials:")
    y_position -= 20
    
    for item in order_items:
        p.drawString(100, y_position, f"{item.material.name} - {item.quantity} x ${item.material.unit_price}")
        y_position -= 20
    
    p.drawString(100, y_position, f"Total: ${order_items.aggregate(total=models.Sum('quantity'))['total']}")
    
    p.showPage()
    p.save()
    
    return response

def order_edit(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Redirect to orders list after saving
    else:
        form = OrderForm(instance=order)

    return render(request, 'carpentry/edit_order.html', {'form': form, 'order': order})

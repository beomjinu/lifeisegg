from django.shortcuts import get_object_or_404, render
from order.models import Order

def payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    context = {
    }

    return render(request, 'payment/payment.html', context)
    

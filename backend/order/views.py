from django.shortcuts import render, get_object_or_404
from shop.models import Option
import base64, json

def form(request):
    data = request.GET.get('data')
    options = json.loads(base64.b64decode(data).decode('ascii'))

    order_product = []

    for i in options:
        option = get_object_or_404(Option, pk=int(i))
        option.quantity = options[i]["quantity"]
        option.format_price = format((option.price + option.product.discounted) * option.quantity, ',')
    
        order_product.append(option)

    context = {
        'order_product': order_product
    }

    return render(request, 'order/form.html', context)

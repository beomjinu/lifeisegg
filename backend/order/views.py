from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Option
from .models import Order, Item
import base64, json, string, random

def form(request):
    data = request.GET.get('data')
    options = json.loads(base64.b64decode(data).decode('ascii'))
    
    if request.method == 'POST':
        post_data = request.POST
        
        order = Order()
        order.orderer_name     = post_data.get('orderer_name')
        order.orderer_number   = post_data.get('orderer_number')
        order.orderer_email    = post_data.get('orderer_email')
        order.recipient_name   = post_data.get('recipient_name')
        order.recipient_number = post_data.get('recipient_number')
        order.address          = post_data.get('address') + post_data.get('address_detail')
        order.request          = post_data.get('request')
        order.status           = 'WFP'
        order.save()
        order.order_id         = str(order.id) + ''.join(random.choice('xyzXYZ') for _ in range(2)) + ''.join(random.choice(string.ascii_lowercase[:-3] + string.ascii_uppercase[-3]) for _ in range(random.randint(11, 18)))
        order.save()

        for i in options:
            option = get_object_or_404(Option, pk=int(i))

            item = Item()
            item.order    = get_object_or_404(Order, pk=order.id)
            item.content  = option.product.name + ' | ' + option.content
            item.price    = option.product.discounted + option.price
            item.quantity = options[i]['quantity']
            item.save() 

        return redirect('payment:open', order_id=order.order_id)
    
    else:
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
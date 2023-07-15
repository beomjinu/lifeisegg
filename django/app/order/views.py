from django.shortcuts import render, get_object_or_404, redirect
from app.shop.models import Option
from .models import Order, Item
import base64, json, string, random

def inquiry(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    context = {
        'title': 'LIFEISEGG - 주문 조회',
        'order': order
    }

    return render(request, 'order/inquiry.html', context)

def form(request):
    data = request.GET.get('data')
    options = json.loads(base64.b64decode(data).decode('ascii'))
    
    if request.method == 'POST':
        post_data = request.POST
        
        order = Order()
        order.orderer_name     = post_data.get('orderer_name')
        order.orderer_number   = post_data.get('orderer_number')
        order.recipient_name   = post_data.get('recipient_name')
        order.recipient_number = post_data.get('recipient_number')
        order.address          = post_data.get('address') + ' ' + post_data.get('address_detail')
        order.request          = post_data.get('request')
        order.status           = 'WFP'
        order.save()
        order.order_id         = str(order.id) + ''.join(random.choice('xyzXYZ') for _ in range(2)) + ''.join(random.choice(string.ascii_lowercase[:-3] + string.ascii_uppercase[:-3]) for _ in range(random.randint(11, 18)))
        order.save()

        for i in options:
            option = get_object_or_404(Option, pk=int(i))

            item = Item()
            item.order    = get_object_or_404(Order, pk=order.id)
            item.content  = str(option)
            item.quantity = options[i]['quantity']
            item.price    = option.get_total_price()
            item.save() 

        return redirect('payment:open', order_id=order.order_id)
    
    else:
        order_items = []

        for i in options:
            option = get_object_or_404(Option, pk=int(i))
            option.quantity = options[i]["quantity"]
            option.result_price = option.get_total_price() * option.quantity

            order_items.append(option)

        context = {
            'title': 'LIFEISEGG - 주문하기',
            'order_items': order_items
        }

        return render(request, 'order/form.html', context)
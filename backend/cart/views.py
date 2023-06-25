from django.shortcuts import render, get_object_or_404
from shop.models import Option
import base64, json

def index(request):
    cart_cookie = request.COOKIES.get('cart')

    context = {
        'cart_cookie': cart_cookie,
    }

    if cart_cookie:
        data = json.loads(base64.b64decode(cart_cookie).decode('ascii'))
        
        items = []
        for id in data:
            item = get_object_or_404(Option, pk=int(id))
            item.quantity = data[id]['quantity']
            item.result_price = format(item.total_price() * item.quantity, ',')

            items.append(item)
        
        context['items'] = items

    
    return render(request, 'cart/index.html', context)
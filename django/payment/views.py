from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from order.models import Order
from .models import Payment
import http.client, base64, json, os
from django.conf import settings

def open(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.status != 'WFP':
        return HttpResponse('order.status is not WFP: 이미 결제 완료된 주문입니다.')
    
    order.amount = sum([item.total_price() for item in order.items.all()])
    order.format_amount = format(order.amount, ',')
    order.order_name = order.items.all()[0].content + (('외 ' + str(len(order.items.all()) - 1) + '개') if (len(order.items.all()) - 1) != 0 else '')

    payment = Payment()
    payment.order = order
    payment.amount = order.amount
    payment.status = 'IN_PROGRESS'
    payment.save()

    context = {
        'title': 'LIFEISEGG - 결제하기',
        'order': order,
    }

    return render(request, 'payment/payment.html', context)

def success(request):
    payment_key = request.GET.get('paymentKey')
    amount      = request.GET.get('amount')
    order_id    = request.GET.get('orderId')

    order = get_object_or_404(Order, order_id=order_id)

    if int(amount) != order.payment.amount:
        return HttpResponse('요청한 결제 금액과 실제 결제 금액이 같지 않습니다.')
    
    conn = http.client.HTTPSConnection('api.tosspayments.com')
    payload    = json.dumps({'paymentKey': payment_key, 'amount': int(amount), 'orderId': order_id})
    toss_sk    = os.environ.get('toss_sk')

    headers = {
        'Authorization': "Basic " + base64.b64encode((toss_sk + ":").encode("utf-8")).decode("ascii"),
        'Content-Type': "application/json"
    }

    conn.request('POST', '/v1/payments/confirm', payload, headers)
    res = conn.getresponse()

    data    = json.loads(res.read().decode('utf-8'))
    order.payment.status = data['status']
    order.payment.save()
    order.status = 'DP'
    order.save()

    return redirect('order:inquiry', order_id=order_id)

def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))


    

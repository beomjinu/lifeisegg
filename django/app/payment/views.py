from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from app.order.models import Order
from .models import Payment
import http.client, base64, json
from django.conf import settings
from modules import alimtalk

def open(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.status != 'WFP':
        return HttpResponse('order.status is not WFP: 이미 결제 완료된 주문입니다.')

    context = {
        'title': 'LIFEISEGG - 결제하기',
        'order': order,
        'toss_ck': settings.TOSS_CK,
    }

    return render(request, 'payment/payment.html', context)

def success(request):
    payment_key = request.GET.get('paymentKey')
    amount      = request.GET.get('amount')
    order_id    = request.GET.get('orderId')

    order = get_object_or_404(Order, order_id=order_id)

    if int(amount) != order.get_amount():
        return HttpResponse('요청한 결제 금액과 실제 결제 금액이 다릅니다.')
    
    conn = http.client.HTTPSConnection('api.tosspayments.com')
    payload    = json.dumps({'paymentKey': payment_key, 'amount': order.get_amount(), 'orderId': order_id})
    toss_sk    = settings.TOSS_SK

    headers = {
        'Authorization': "Basic " + base64.b64encode((toss_sk + ":").encode("utf-8")).decode("utf-8"),
        'Content-Type': "application/json"
    }

    conn.request('POST', '/v1/payments/confirm', payload, headers)
    res = conn.getresponse()

    if 200 <= res.status < 300:
        payment = Payment()
        payment.order = order
        payment.data  = base64.b64encode(res.read()).decode('utf-8')
        payment.save()

        order.status = 'DP'
        order.save()

        message = alimtalk.Message()
        message.create_send_data(
            {
                "to": order.orderer_number.replace("-", ""),
                "template": "주문접수",

                "var": {
                    "#{amount}": format(order.get_amount(), ",") + "원",
                    "#{order_id}": order.order_id
                }
            }
        )
        message.send()

        return redirect('order:inquiry', order_id=order_id)
    else:
        return HttpResponse('오류가 발생하였습니다. \n' + res.read())


def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))


    

from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.conf import settings

from app.order.models import Order

from utils.alimtalk import Message
from utils.tosspayments import TossPayments
from utils.tools import get_client_ip

import logging

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
    order = get_object_or_404(Order, order_id=request.GET.get('orderId'))

    if order.amount != int(request.GET.get('amount')):
        logger = logging.getLogger(__name__)
        logger.error(f'ip: {get_client_ip(request)} ')

        return HttpResponse('요청한 결제 금액과 실제 결제 금액이 다릅니다.')
    
    payload = {
        'orderId': request.GET.get('orderId'),
        'paymentKey': request.GET.get('paymentKey'),
        'amount': int(request.GET.get('amount'))
    }

    toss = TossPayments()
    response = toss.success(payload=payload)
    
    if not 200 <= response.status_code < 300:
        logger = logging.getLogger(__name__)
        logger.critical(f'order id:{order.order_id} tosspayments error data: {response.json()}')

        return HttpResponse('오류가 발생하였습니다. ' + response.json())
    
    message = Message()
    message.create_send_data(
            {
                "to": order.orderer_number.replace("-", ""),
                "template": "주문접수",

                "var": {
                    "#{amount}": format(order.amount, ",") + "원",
                    "#{order_id}": order.order_id
                }
            }
        )
    message.send()

    order.status = 'DP'
    order.save()

    return redirect('order:inquiry', order_id=order.order_id)

def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))


    

from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.conf import settings

from app.order.models import Order

from utils.alimtalk import Message
from utils.tosspayments import TossPayments
from utils.tools import get_client_ip

import logging

logger = logging.getLogger(__name__)

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
        logger.error(f'ip: {get_client_ip(request)} order_id:{order.order_id} 사용자가 변조를 시도하였습니다.')

        return HttpResponse('요청한 결제 금액과 실제 결제 금액이 다릅니다.')
    
    payload = {
        'orderId': request.GET.get('orderId'),
        'paymentKey': request.GET.get('paymentKey'),
        'amount': int(request.GET.get('amount'))
    }

    toss = TossPayments()
    response = toss.success(payload=payload)
    
    if not 200 <= response.status_code < 300:
        logger.critical(f'order_id: {order.order_id} 토스페이먼츠 결제 승인 오류 data: {response.json()}')

        return HttpResponse(f'오류가 발생하였습니다. data: {response.json()}')
    
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
    response = message.send()

    if not 200 <= response.status_code < 300:
        logger.critical(f'order_id: {order.order_id} 알림톡 발송 오류 data: {response.json()}')

    order.status = 'DP'
    order.save()

    return redirect('order:inquiry', order_id=order.order_id)

def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))


    

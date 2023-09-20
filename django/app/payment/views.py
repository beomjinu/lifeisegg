from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from app.order.models import Order

from utils.alimtalk import Message
from utils.tosspayments import TossPayments
from utils.tools import get_client_ip

import logging, json

logger = logging.getLogger(__name__)

def open(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.status != 'WFP':
        return HttpResponse('order.status is not WFP: 이미 결제 완료된 주문입니다.')

    context = {
        'title': '결제하기 - 라이프이즈에그',
        'order': order,
        'toss_ck': settings.ENV_DATA['TOSS_CK'],
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
    toss_response = toss.success(payload=payload)
    
    if not 200 <= toss_response.status_code < 300:
        logger.critical(f'order_id: {order.order_id} 토스페이먼츠 결제 승인 오류 data: {toss_response.json()}')

        return HttpResponse(f'오류가 발생하였습니다. data: {toss_response.json()}')
    
    if toss_response.json()['method'] == '가상계좌':
        order.status = 'WFD'

        # 후에 가상계좌 입금 안내에 대한 알림톡 추가

    else:
        message = Message()
        message.create_send_data(
                {
                    "to": order.orderer_number,
                    "template": "주문접수",

                    "var": {
                        "#{amount}": format(order.amount, ",") + "원",
                        "#{order_id}": order.order_id
                    }
                }
            )
        
        alimtalk_response = message.send()

        order.status = 'DP'
    
        if not 200 <= alimtalk_response.status_code < 300:
            logger.critical(f'order_id: {order.order_id} 알림톡 발송 오류 data: {alimtalk_response.json()}')
    
    order.save()

    return redirect('order:inquiry', order_id=order.order_id)

def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))

@csrf_exempt
def hook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if data['eventType'] == 'PAYMENT_STATUS_CHANGED':
            if data['data']['status'] == 'DONE':
                order = get_object_or_404(Order, order_id=data['data']['orderId'])
                
                message = Message()
                message.create_send_data(
                        {
                            "to": order.orderer_number,
                            "template": "주문접수",

                            "var": {
                                "#{amount}": format(order.amount, ",") + "원",
                                "#{order_id}": order.order_id
                            }
                        }
                    )
                
                alimtalk_response = message.send()
                
                if not 200 <= alimtalk_response.status_code < 300:
                    logger.critical(f'order_id: {order.order_id} 알림톡 발송 오류 data: {alimtalk_response.json()}')

                order.status = 'DP'
                order.save()
                
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


    

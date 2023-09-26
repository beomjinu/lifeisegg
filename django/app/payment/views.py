from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from app.order.models import Order
from app.payment.models import Payment

from utils.alimtalk import Message
from utils.tosspayments import TossPayments
from utils.tools import get_client_ip

import base64

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

        return HttpResponse('오류가 발생하였습니다. 우측 하단 채널톡 버튼을 눌러 문의 바랍니다.')
    
    payload = {
        'orderId': request.GET.get('orderId'),
        'paymentKey': request.GET.get('paymentKey'),
        'amount': int(request.GET.get('amount'))
    }

    toss = TossPayments()
    response = toss.success(payload=payload)
    
    if not 200 <= response.status_code < 300:
        logger.critical(f'토스페이먼츠 결제 승인 오류 data: {response.json()}')

        return HttpResponse('오류가 발생하였습니다. 우측 하단 채널톡 버튼을 눌러 문의 바랍니다.')
    
    payment         = Payment()
    payment.order   = order
    payment.data    = base64.b64encode(json.dumps(response.json()).encode('utf-8')).decode('utf-8')
    payment.save()
    
    if payment.status == 'WAITING_FOR_DEPOSIT':
        order.status = 'WAITING_FOR_DEPOSIT'
        
        message = Message()
        message.create_send_data(
            {
                "to": order.orderer_number,
                "template": "입금요청",

                "var": {
                    '#{order_id}': order.order_id,
                    '#{amount}': format(order.amount, ',') + '원',
                    '#{account}': order.payment.virtual_account,
                    '#{due_date}': order.payment.due_date.strftime('%Y년 %m월 %d일 %H시 %M분'),
                }
            }
        )
        message.send()

    elif payment.status == 'DONE':
        order.status = 'DONE_PAYMENT'
        
        message = Message()
        message.create_send_data(
            {
                "to": order.orderer_number,
                "template": "주문접수",

                "var": {
                    "#{amount}": format(order.amount, ',') + '원',
                    "#{order_id}": order.order_id
                }
            }
        )
        message.send()

    else:
        logger.critical(f'토스페이먼츠 결제 승인 오류 data: {response.json()}')

        return HttpResponse('오류가 발생하였습니다. 우측 하단 채널톡 버튼을 눌러 문의 바랍니다.')
    
    order.save()

    return redirect('order:inquiry', order_id=order.order_id)

def fail(request):
    return HttpResponse(request.GET.get('code') + ':' + request.GET.get('message') + ':' + request.GET.get('orderId'))

@csrf_exempt
def hook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        order = Order.objects.get(order_id=data['orderId'])
        if data['secret'] == order.payment.get_data()['secret']:
            if data['status'] == 'DONE':
                order.status = 'DONE_PAYMENT'
                order.save()

                payment = Payment.objects.get(order=order)
                payment.update_data()
                
                message = Message()
                message.create_send_data(
                    {
                        "to": order.orderer_number,
                        "template": "주문접수",

                        "var": {
                            "#{amount}": format(order.amount, ',') + '원',
                            "#{order_id}": order.order_id,
                        }
                    }
                )
                message.send()


            elif data['status'] == 'WAITING_FOR_DEPOSIT':
                order.status = 'WAITING_FOR_DEPOSIT'
                order.save()

                payment = Payment.objects.get(order=order)
                payment.update_data()

                message = Message()
                message.create_send_data(
                    {
                        "to": order.orderer_number,
                        "template": "재입금요청",

                        "var": {
                            '#{order_id}': order.order_id,
                            '#{amount}': format(order.amount, ',') + '원',
                            '#{account}': order.payment.virtual_account,
                            '#{due_date}': order.payment.due_date.strftime('%Y년 %m월 %d일 %H시 %M분'),
                        }
                    }
                )
                message.send()
            else:
                return HttpResponse(status=422)
        else:
            return HttpResponse(status=401)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
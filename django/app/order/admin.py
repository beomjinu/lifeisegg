from django.contrib import admin
from .models import Order, Item
from app.payment.models import Payment
from utils.alimtalk import Message
from utils.tosspayments import TossPayments
import base64

class ItemInline(admin.TabularInline):
    model = Item

class PaymentInline(admin.TabularInline):
    model = Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'orderer_name', 'orderer_number', 'status']
    inlines      = [ItemInline, PaymentInline]
    actions      = ['done_send', 'cancel']

    @admin.action(description="DONE SEND")
    def done_send(self, request, queryset):
        for order in queryset:
            if order.delivery and order.status == 'DONE_PAYMENT':
                message = Message()
                message.create_send_data(
                    {
                        "to": order.orderer_number,
                        "template": "발송완료",

                        "var": {
                            "#{order_id}": order.order_id,
                            "#{delivery}": order.delivery,
                        }
                    }
                )
                message.send()

                order.status = 'DONE_SEND'
                order.save()

    @admin.action(description="CANCEL")
    def cancel(self, request, queryset):
        for order in queryset:
            if order.status == 'DONE_PAYMENT':
                toss = TossPayments()
                response = toss.cancel(order_id=order.order_id)
                
                if 200 <= response.status_code < 300:
                    order.status = 'CANCELED'
                    order.save()

                    payment = Payment.objects.get(order=order)
                    payment.data = base64.b64decode(response.body.encode('utf-8')).decode('utf-8')

                    message = Message()
                    message.create_send_data(
                        {
                            "to": order.orderer_number,
                            "template": "주문취소",

                            "var": {
                                "#{order_id}": order.order_id,
                                "#{amount}": order.amount,
                            }
                        }
                    )
                    message.send()
from django.contrib import admin
from .models import Order, Item
from app.payment.models import Payment
from modules import alimtalk
from django.conf import settings
from django.shortcuts import get_object_or_404
import http, json, base64

class ItemInline(admin.TabularInline):
    model = Item

class PaymentInline(admin.TabularInline):
    model = Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'orderer_name', 'orderer_number', 'status']
    inlines      = [ItemInline, PaymentInline]
    actions      = ['done_send', 'cancle']

    @admin.action(description="Done send")
    def done_send(self, request, queryset):
        for order in queryset:
            if order.delivery and order.status == 'DP':
                message = alimtalk.Message()
                message.create_send_data(
                    {
                        "to": order.orderer_number.replace("-", ""),
                        "template": "발송완료",

                        "var": {
                            "#{delivery}": order.delivery,
                            "#{order_id}": order.order_id
                        }
                    }
                )
                message.send()
                order.status = 'DS'
                order.save()
            else:
                pass

    @admin.action(description="Cancle")
    def cancle(self, request, queryset):
        for order in queryset:
            if order.status == 'DP':
                conn = http.client.HTTPSConnection('api.tosspayments.com')
                payload    = json.dumps({'cancelReason': '고객 변심'})

                headers = {
                    'Authorization': "Basic " + base64.b64encode((settings.TOSS_SK + ":").encode("utf-8")).decode("utf-8"),
                    'Content-Type': "application/json"
                }

                conn.request("POST", f"/v1/payments/{order.payment.get_data()['paymentKey']}/cancel", payload, headers)
                res = conn.getresponse()

                payment = order.payment
                payment.data  = base64.b64encode(res.read()).decode('utf-8')
                payment.save()
                
                order.status = 'C'
                order.save()
            else:
                pass
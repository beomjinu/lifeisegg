from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import admin

from .models import Order, Item

from utils.alimtalk import Message
from utils.tosspayments import TossPayments

class ItemInline(admin.TabularInline):
    model = Item

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'orderer_name', 'orderer_number', 'status']
    inlines      = [ItemInline]
    actions      = ['done_send', 'cancle']

    @admin.action(description="Done send")
    def done_send(self, request, queryset):
        for order in queryset:
            if order.delivery and order.status == 'DP':
                message = Message()
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

    @admin.action(description="Cancle")
    def cancle(self, request, queryset):
        for order in queryset:
            if order.status == 'DP':
                toss = TossPayments()
                response = toss.cancel(order_id=order.order_id)
                
                if 200 <= response.status_code < 300:
                    order.status = 'C'
                    order.save()
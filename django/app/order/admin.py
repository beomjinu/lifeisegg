from django.contrib import admin
from .models import Order
from modules import alimtalk

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'orderer_name', 'orderer_number', 'status']
    actions      = ['start_delivery'] 

    @admin.action(description="start delivery")
    def start_delivery(self, request, queryset):
        for order in queryset:
            if order.delivery and (order.status == 'DP'):
                message = alimtalk.Message()
                message.create_send_data(
                    {
                        "to": order.orderer_number.replace("-", ""),
                        "template": "주문접수",

                        "var": {
                            "#{amount}": format(order.amount(), ",") + "원",
                            "#{order_id}": order.order_id
                        }
                    }
                )
                message.send()
            else:
                pass
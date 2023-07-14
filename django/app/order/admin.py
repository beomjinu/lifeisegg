from django.contrib import admin
from .models import Order, Item
from app.payment.models import Payment
from modules import alimtalk

class ItemInline(admin.TabularInline):
    model = Item

class PaymentInline(admin.TabularInline):
    model = Payment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'orderer_name', 'orderer_number', 'status']
    inlines      = [ItemInline, PaymentInline]
    actions      = ['done_send']

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
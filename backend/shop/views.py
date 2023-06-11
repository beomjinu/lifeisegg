from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.order_by('priority')

    for product in products:
        product.format_price      = format(product.price, ",")
        product.format_discounted = format(product.discounted, ",")
        product.solted_images     = product.images.all().order_by('priority')

    context  = {
        'products': products
    }

    return render(request, 'shop/index.html', context=context)
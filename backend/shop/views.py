from django.shortcuts import render, get_object_or_404
from .models import Product
import json

def index(request):
    products = Product.objects.order_by('priority')

    for product in products:
        product.format_price      = format(product.price, ",")
        product.format_discounted = format(product.discounted, ",")
        product.solted_images     = product.images.all().order_by('priority')

    context = {
        'products': products
    }

    return render(request, 'shop/index.html', context=context)    

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    product.format_price      = format(product.price, ",")
    product.format_discounted = format(product.discounted, ",")
    product.solted_images     = product.images.all().order_by('priority')
    product.solted_options    = product.options.all().order_by('priority')

    context = {
        'product': product,
    }

    return render(request, 'shop/detail.html', context=context)
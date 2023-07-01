from django.shortcuts import redirect, render, get_object_or_404
from .models import Product
import json

def redirect_index(request):
    return redirect("shop:index")

def index(request):
    products = Product.objects.order_by('priority')

    for product in products:
        product.solted_images = product.images.all().order_by('priority')

    context = {
        'title': 'LIFEISEGG - SHOP',
        'products': products
    }

    return render(request, 'shop/index.html', context=context)    

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    product.solted_images     = product.images.all().order_by('priority')
    product.solted_options    = product.options.all().order_by('priority')

    context = {
        'title': 'LIFEISEGG - ' + product.name,
        'product': product,
        'og_img_url': product.solted_images.first().image.url if not product.og_img else product.og_img.url
    }

    return render(request, 'shop/detail.html', context=context)
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product
import json

def redirect_index(request):
    return redirect("shop:index")

def index(request):
    products = Product.objects.order_by('priority')

    context = {
        'title': 'LIFEISEGG - SHOP',
        'products': products
    }

    return render(request, 'shop/index.html', context=context)    

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'title': 'LIFEISEGG - ' + product.name,
        'product': product,
        'og_img_url': product.get_images().first().image.url if not product.og_img else product.og_img.url
    }

    return render(request, 'shop/detail.html', context=context)
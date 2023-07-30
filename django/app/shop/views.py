from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    products = Product.objects.order_by('priority')

    context = {
        'title': '라이프이즈에그 스케이트보드',
        'products': products
    }

    return render(request, 'shop/index.html', context=context)    

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'title': f'{product.name} 구매하기 - 라이프이즈에그',
        'description': f'{product.name} {format(product.discounted, ",")}원에 구매하기', 
        'product': product,
        'og_img_url': product.solted_images.first().image.url if not product.og_img else product.og_img.url
    }

    return render(request, 'shop/detail.html', context=context)
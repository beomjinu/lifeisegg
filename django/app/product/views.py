from django.shortcuts import render, get_object_or_404, HttpResponse, reverse
from .models import Product


def index(request):
    products = Product.objects.order_by('priority')

    context = {
        'title': '라이프이즈에그 스케이트보드',
        'products': products
    }

    return render(request, 'product/index.html', context=context)    


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'title': f'{product.name} 구매하기 - 라이프이즈에그',
        'description': f'{product.name} {format(product.discounted, ",")}원에 구매하기', 
        'product': product,
        'og_img_url': product.solted_images.first().image.url,
    }

    return render(request, 'product/detail.html', context=context)


def enginePage(request, name: str):
    if name == 'naver':
        data = [
            ['id', 'title', 'price_pc', 'normal_price', 'link', 'image_link', 'category_name1', 'naver_category', 'brand', 'shipping', 'shipping_settings']
        ]

        products = Product.objects.order_by('priority')

        for product in products:
            data.append([
                product.id,
                product.name if not (n := product.naver_name) else n,
                str(product.discounted),
                str(product.price),
                f'{request.scheme}://{request.get_host()}' + reverse('product:detail', kwargs={'product_id': product.id}),
                f'{request.scheme}://{request.get_host()}' + product.solted_images.first().image.url,
                '스포츠',
                '50001538',
                '라이프이즈에그',
                '0',
                '오늘출발^20:00^택배^CJ대한통운^N^N^4000^4000^^^토요일|일요일^',
            ])
        tsv = '\n'.join(['\t'.join(value) for value in data])

        return HttpResponse(tsv, content_type='text/plain; charset=utf-8')

from django.shortcuts import render

def form(request):
    use_cart = bool(int(request.GET.get('use_cart')))

    if use_cart:
        pass
    else:
        pass
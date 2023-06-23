from django.shortcuts import render

def index(request):
    context = {
    }
    
    return render(request, 'cart/index.html', context)

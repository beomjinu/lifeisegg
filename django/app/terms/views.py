from django.shortcuts import render, get_object_or_404
from .models import Page 

def page(request, page_name: str):
    pg = get_object_or_404(Page, name=page_name)

    context = {
        'title': f'{pg.display_name if pg.display_name else pg.name} - 라이프이즈에그',
        'page': pg,
    }

    return render(request, 'terms/page.html', context)

def policy(request):
    context = {
        'title': '이용약관 - 라이프이즈에그'
    }
    return render(request, 'terms/policy.html', context)

def privacy(request):
    context = {
        'title': '개인정보처리방침 - 라이프이즈에그'
    }
    return render (request, 'terms/privacy.html', context)

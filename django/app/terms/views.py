from django.shortcuts import render

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

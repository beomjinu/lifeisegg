from django.shortcuts import render

def policy(request):
    context = {
        'title': 'LIFEISEGG - 이용약관'
    }
    return render(request, 'terms/policy.html', context)

def privacy(request):
    context = {
        'title': 'LIFEISEGG - 개인정보처리방침'
    }
    return render (request, 'terms/privacy.html', context)

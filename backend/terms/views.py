from django.shortcuts import render

def policy(request):
    return render(request, 'terms/policy.html')

def privacy(request):
    return render (request, 'terms/privacy.html')

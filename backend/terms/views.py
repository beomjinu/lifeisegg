from django.shortcuts import render

def policy(request):
    render(request, 'terms/policy.html')

def privacy(request):
    render (request, 'terms/privacy.html')

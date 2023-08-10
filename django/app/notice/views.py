from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Notice

def index(request):
    notices = Notice.objects.order_by('-created_at')

    context = {
        'title': f'공지사항 - 라이프이즈에그',
        'notices': notices
    }

    return render(request, 'notice/index.html', context)

def detail(request, id: int):
    notice = get_object_or_404(Notice, pk=id)
    
    context = {
        'title': f'{notice.title} - 라이프이즈에그',
        'notice': notice
    }

    return render(request, 'notice/detail.html', context)

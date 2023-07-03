from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin)
def index(request):
   return render(request, 'nimda/index.html')

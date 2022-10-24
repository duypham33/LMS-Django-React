from django.shortcuts import render
from django.conf import settings
import os
# Create your views here.

def index(request):
    path = os.path.join(settings.BASE_DIR, 'frontend/templates/frontend/index.html')
    return render(request, path)

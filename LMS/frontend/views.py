from django.shortcuts import render
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    path = os.path.join(settings.BASE_DIR, 'frontend/templates/frontend/index.html')
    return render(request, path, {'userID': request.user.pk})


@login_required
def chat_room(request, chatID):
    path = os.path.join(settings.BASE_DIR, 'frontend/templates/frontend/index.html')
    return render(request, path) 
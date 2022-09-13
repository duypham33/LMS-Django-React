
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import os
# Create your views here.

@login_required(login_url='login/')
def index(request):
    return render(request, 'index.html')



@login_required(login_url='login/')
def profile(request):
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar', None)
        first_name = request.POST.get('firstname', None)
        last_name = request.POST.get('lastname', None)

        user = request.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if avatar_file and avatar_file != '':
            file_name = request.user.avatar.name
            user.avatar = avatar_file

            if file_name != '' and file_name != 'media/profile_pic/anonymous-user.png':
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                os.remove(file_path)
        user.save()
        messages.success(request, 'Your profile is updated!')
        return redirect('app:profile')

    return render(request, 'profile.html')
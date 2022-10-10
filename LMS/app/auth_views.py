from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
# Create your views here.

class LoginBackend(ModelBackend):
    def authenticate(self, username, password, **kwargs):
        if username and password: 
            userModel = get_user_model()
            try:
                user = userModel.objects.get(username=username)
            except:
                try:
                    user = userModel.objects.get(email=username)
                except:
                    return None

            return user if user.check_password(password) else None
        
        return None



def login_user(request):
    if request.method == 'POST':
        user = LoginBackend.authenticate(request, 
                request.POST.get('account', None), request.POST.get('password', None))
        if user:
            login(request, user)
            return redirect('app:index')
            
        else:
            messages.warning(request, 'Your username, email, or password is incorrect!')

    return render(request, 'login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You logged out!')
    else:
        messages.info(request, 'You haven\'t logged in yet!')
    
    return redirect('app:login')
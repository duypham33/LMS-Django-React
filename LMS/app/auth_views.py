from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from .models import User

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

            user_type = user.user_type
            if user_type == '1':
                return redirect('teacher:teaHome')
            elif user_type == '2':
                return redirect('staff:staHome')
            else:
                return redirect('student:stuHome')
        else:
            messages.warning(request, 'Your username, email, or password is incorrect!')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.warning(request, 'Your confirm password does not match!')
        else:
            user1 = User.objects.filter(email = email).first()
            user2 = User.objects.filter(username = username).first()
            if user1:
                messages.warning(request, 'This email has already registered! Please, choose another one!')
            elif user2:
                messages.warning(request, 'This username has already registered! Please, choose another one!')
            else:
                User.objects.create(username = username, first_name = first_name, last_name = last_name,
                email = email, password = password, user_type = user_type)
                messages.success(request, 'Your account is created!')
                return redirect('app:login')
            
    return render(request, 'register.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You logged out!')
    else:
        messages.info(request, 'You haven\'t logged in yet!')
    
    return redirect('app:login')
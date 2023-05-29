from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
from dash.models import Admin
from django.contrib.auth import logout
from django.shortcuts import redirect

from sss.settings import LOGIN_REDIRECT_URL


def logout_user(request):
    logout(request)
    return redirect('Login')


def login_user(request):
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        return redirect(LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Return a JSON response with a success message
            return JsonResponse({'success': True, 'message': 'Logged in successfully'})
        else:
            # Return a JSON response with an error message
            return JsonResponse({'success': False, 'message': 'Username or password is incorrect'})

    return render(request, 'login.html')


def is_admin(user):
    return user.groups.filter(name='Admins').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        status = Admin.objects.all().filter(user_id=request.user.id, is_Active=True)
        if status:
            return redirect('dashboard:home')
        else:
            return redirect('error')
    else:
        return redirect('Login')

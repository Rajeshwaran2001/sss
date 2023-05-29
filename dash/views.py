from django.conf.global_settings import LOGIN_REDIRECT_URL
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return render(request, 'index.html')


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain user session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('Dashboard:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'change_password.html', context)


def logout_user(request):
    logout(request)
    return redirect('Login')


def login_user(request):
    if request.user.is_authenticated:
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

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
from dash.models import Admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import ServiceBaseForm
from sss.forms import ServiceBaseForm
from utility.models import device_list, branch
from sss.settings import LOGIN_REDIRECT_URL
from company.models import service


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


def customer_view(request):
    br = branch.objects.all().filter(is_active=True)
    if request.method == 'POST':
        username = request.POST.get('username')
        branchf = request.POST.get('branch')
        usernames = username.strip()  # Remove any leading or trailing spaces
        username_upper = usernames.upper()  # Convert ad_name to uppercase
        try:
            ad = device_list.objects.get(sys_name=username, branch_id=branchf)
            serv = service.objects.filter(branch_id=branchf, pc=ad)
            form = ServiceBaseForm()
            return render(request, 'customer/service.html', {'ad': ad, 'ser': serv, 'form': form})
        except device_list.DoesNotExist:
            messages.error(request, f"Ad with name {username} does not exist.")
            print('not fount')
            return redirect('customer')

    return render(request, 'customer/login.html', {'br': br})


def save(request):
    if request.method == 'POST':
        data = ServiceBaseForm(request.POST)
        if data.is_valid():
            data1 = data.save()
            data1.save()
            return JsonResponse({'success': True, 'message': 'Issue Raised successfully'})
        else:
            return JsonResponse({'Failed': True, 'message': 'Issue Not Raised'})

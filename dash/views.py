from django.contrib.auth.models import Group
from utility.models import device_list
from .forms import AdminBaseForm, AdminUserForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.

@login_required()
def home(request):
    return render(request, 'index.html')


@login_required()
def asset(request):
    list = device_list.objects.all()
    context = {
        'list': list,
    }
    return render(request, 'dashboard/asset.html', context)


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


def Admin_signup_view(request):
    userForm = AdminBaseForm()
    AdminUser = AdminUserForm()
    mydict = {'userForm': userForm, 'AdminUser': AdminUser}
    if request.method == 'POST':
        userForm = AdminBaseForm(request.POST)
        AdminUser = AdminUserForm(request.POST)
        if userForm.is_valid() and AdminUser.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            Admin_s = AdminUser.save(commit=False)
            Admin_s.user = user
            Admin_s.save()
            my_group = Group.objects.get_or_create(name='Admins')
            my_group[0].user_set.add(user)
        return redirect('Login')
    return render(request, 'signup/signup.html', context=mydict)

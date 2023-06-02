from django.contrib.auth.models import Group
from utility.models import device_list
from .forms import AdminBaseForm, AdminUserForm, asset_listForm, asset_editForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from company.models import service


# Create your views here.

@login_required()
def home(request):
    ser = service.objects.all().filter(status=False)
    context = {
        'service': ser
    }
    return render(request, 'index.html', context)


@login_required()
def asset(request):
    li = device_list.objects.all()
    form = asset_listForm()
    if request.method == 'POST':
        data = asset_listForm(request.POST)
        if data.is_valid():
            data1 = data.save()
            data1.save()
            return JsonResponse({'success': True, 'message': 'New Asset Added successfully'})
    context = {
        'list': li,
        'form': form
    }
    return render(request, 'dashboard/asset.html', context)


@login_required()
def edit_asset(request, pk):
    assets = get_object_or_404(device_list, pk=pk)
    if request.method == 'POST':
        form = asset_editForm(request.POST, instance=assets)
        if form.is_valid():
            form.save()
            return redirect('dashboard:asset')
    else:
        form = asset_editForm(instance=assets)
    return render(request, 'dashboard/edit_asset.html', {'form': form, 'assets': assets})


@login_required()
def delete_asset(request, pk):
    assets = device_list.objects.get(pk=pk)
    assets.delete()
    return redirect('dashboard:asset')

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

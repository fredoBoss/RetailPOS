from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def _role_redirect(user):
    try:
        role = user.profile.role
    except Exception:
        role = 'cashier'
    if role == 'superadmin':
        return redirect('superadmin_dashboard')
    if role == 'admin':
        return redirect('admin_dashboard')
    return redirect('cashier_dashboard')


def login_view(request):
    if request.user.is_authenticated:
        return _role_redirect(request.user)

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        try:
            u = User.objects.get(email__iexact=email)
            user = authenticate(request, username=u.username, password=password)
            if user:
                login(request, user)
                return _role_redirect(user)
            error = 'Invalid email or password.'
        except User.DoesNotExist:
            error = 'Invalid email or password.'

    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def superadmin_dashboard(request):
    if request.user.profile.role != 'superadmin':
        return _role_redirect(request.user)
    return render(request, 'dashboard/superadmin.html', {'user': request.user})


@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        return _role_redirect(request.user)
    return render(request, 'dashboard/admin.html', {'user': request.user})


@login_required
def cashier_dashboard(request):
    if request.user.profile.role != 'cashier':
        return _role_redirect(request.user)
    return render(request, 'dashboard/cashier.html', {'user': request.user})

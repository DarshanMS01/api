from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        messages.error(request, 'Please check your username and password.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    users = User.objects.order_by('username')
    staff_users = users.filter(is_staff=True)
    regular_users = users.filter(is_staff=False)

    return render(request, 'dashboard.html', {
        'users': users,
        'staff_users': staff_users,
        'total_users': users.count(),
        'total_staff': staff_users.count(),
        'total_members': regular_users.count(),
    })


@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')


def students(request):
    return render(request, 'students.html')

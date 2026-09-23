from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .decorators import role_required
from .forms import LoginForm, RegisterForm
from .models import User




@login_required
def home(request):
    return render(request,'home.html')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            try:
                send_mail(
                    'Welcome to Job Portal',
                    f'Hello {user.first_name},\n\n'
                    'Welcome to our Job Portal! Your account has been created successfully.',
                    None,
                    [user.email],
                )
            except Exception:
                pass

            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('home')

    else:
        form = LoginForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return redirect('home')

from multiprocessing.context import AuthenticationError

from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from accounts.forms import SignupForm, LoginForm


# Create your views here.
def signup_view(requst):
    if requst.method == 'POST':
        form = SignupForm(requst.POST)
        if form.is_valid():
            user = form.save()
            login(requst, user)
            return redirect('homepage')
    else:
        form = SignupForm()
    return render(requst, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('homepage')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('homepage')
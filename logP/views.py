from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import render, HttpResponse, redirect

# For Login and logout
from django.contrib.auth import authenticate, login, logout

# Change Password
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'logP/home.html')


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('homepage')

        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers ')
            return redirect('homepage')

        if pass1 != pass2:
            messages.error(request, "Password doesn't match")
            return redirect('homepage')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Account Created Successfully')
        return redirect('homepage')

    else:
        return HttpResponse('404: Error Found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Your Are Successfully Login")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid Credentials Please Try Again")
            return redirect('homepage')

    return HttpResponse('404: Error Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out ")
    return redirect('homepage')


@login_required
def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            logout(request)
            messages.success(request, 'Password Changed Successfully!')
            return redirect('homepage')
        else:
            messages.error(request, "Password Can't Changed")
    else:
        form = PasswordChangeForm(request.user)
    params = {
        'form': form,
    }
    return render(request, 'logP/change_pass.html', params)

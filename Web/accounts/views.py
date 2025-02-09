from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def user_login(request):
    def get_success_url(request):
        next_url = request.POST.get('next')
        if next_url:
            print(next_url)
            return redirect(next_url)
        else:
            return redirect('/')  # default URL to redirect to after login

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return get_success_url(request)
    else:
        form = AuthenticationForm()
        print('no login')
    return render(request, 'accounts/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # authenticate_user = authenticate(username=new_user.username,
            #                                  password=new_user.password)
            # login(request, authenticate_user)
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)



from django.shortcuts import render, redirect
from .forms import UserSignupform
from django.contrib.auth import logout as auth_logout

def signup(request):
    if request.method == 'POST':
        form = UserSignupform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            return redirect('/accounts/login/')  
    else:
        form = UserSignupform()
    
    return render(request, 'registration/signup.html', context={'form': form})

def logout(request):
    auth_logout(request)
    return render(request,'registration/login-again.html')
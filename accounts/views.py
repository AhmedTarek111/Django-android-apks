from django.shortcuts import render, redirect
from .forms import UserSignupform

def signup(request):
    if request.method == 'POST':
        form = UserSignupform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            return redirect('/accounts/login/')  # Redirect after successful signup
    else:
        form = UserSignupform()
    
    return render(request, 'registration/signup.html', context={'form': form})

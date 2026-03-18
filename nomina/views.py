from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
# Vista para el login
def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'nomina/login.html')

# Vista para el dashboard
def dashboard(request):
    return render(request, 'nomina/dashboard.html')
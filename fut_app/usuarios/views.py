from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def pagina_principal(request):
    return render(request, 'usuarios/pagina_principal.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        senha = request.POST.get('password') 

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('pagina_principal')  
        else:
            messages.error(request, 'Credenciais inválidas.')
            return redirect('login')  

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def cadastro_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('password_confirmation')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastro')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return redirect('cadastro')

        user = User.objects.create_user(username=email, email=email, password=senha)
        login(request, user)

        return redirect('pagina_principal')

    return render(request, 'usuarios/cadastro.html')
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        # Usando email como username
        username = request.POST.get('username')  # <- nome do campo no HTML
        senha = request.POST.get('password') # <- nome do campo no HTML

        # Autenticar o usuário usando o campo 'username' (que é o email)
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            # Se o usuário for encontrado, realiza o login
            login(request, user)
            return redirect('pagina_principal')  # Redirecionar para a página principal
        else:
            messages.error(request, 'Credenciais inválidas.')
            return redirect('login')  # Redirecionar de volta para o login

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def pagina_principal(request):
    return render(request, 'usuarios/pagina_principal.html')

def cadastro_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('password_confirmation')

        # Verificação se as senhas são iguais
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastro')

        # Verificar se o email já está em uso
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este email já está em uso.')
            return redirect('cadastro')

        # Criando o usuário no banco de dados
        user = User.objects.create_user(username=email, email=email, password=senha)

        # Login automático após cadastro
        login(request, user)

        # Redirecionar para a página principal após o cadastro
        return redirect('pagina_principal')

    return render(request, 'usuarios/cadastro.html')
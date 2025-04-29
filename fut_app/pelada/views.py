from django.shortcuts import render

# Create your views here.
def gerenciador(request):
    return render(request, 'gerencia/gerenciador.html')
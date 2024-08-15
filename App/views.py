from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Receta
from .forms import RecetaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, "app/index.html")       

def about(request):
    informacion = "Esta página de recetas fitness ofrece una variedad de recetas saludables diseñadas para apoyar un estilo de vida activo. Proporciona opciones nutritivas, fáciles de preparar y equilibradas en macronutrientes, ideales para quienes buscan mejorar su bienestar, mantener su peso o alcanzar sus objetivos de fitness. Es una herramienta práctica para inspirar y guiar a las personas en su camino hacia una alimentación consciente y saludable."
    return render(request, 'app/about.html', {'informacion': informacion})

def recetas_list(request):
    recetas = Receta.objects.all()
    return render(request, 'app/recetas.html', {'recetas': recetas})

@login_required
def publicar_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.save()
            return redirect('recetas_list')
    else:
        form = RecetaForm()
    return render(request, 'app/publicar_recetas.html', {'form': form})    

@login_required
def editar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)

    if receta.autor != request.user:
        return redirect('recetas_list')

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('recetas_list')
    else:
        form = RecetaForm(instance=receta)

    return render(request, 'app/editar_receta.html', {'form': form})    

def receta_detail(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    return render(request, 'app/receta_detail.html', {'receta': receta})


@login_required
def borrar_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    
    if request.user == receta.autor or request.user.is_staff:
        receta.delete()
        messages.success(request, 'Receta eliminada con éxito.')
        return redirect('recetas_list')
    else:
        messages.error(request, 'No tienes permiso para eliminar esta receta.')
        return redirect('receta_detail', receta_id=receta_id)
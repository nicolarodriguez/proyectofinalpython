from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserEditForm
from users.models import Avatar
from django.shortcuts import redirect
from django.contrib.auth import logout


def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username= usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return render(request, "app/index.html")

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "msg_login": msg_login})


def register(request):

    msg_register = ""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"app/index.html")
        
        msg_register = "Error en los datos ingresados"

    form = UserRegisterForm()     
    return render(request,"users/registro.html" ,  {"form":form, "msg_register": msg_register})
    
@login_required
def edit(request):
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, request.FILES)

        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data

            if informacion["password1"] != informacion["password2"]:
                miFormulario.add_error('password2', 'Las contraseñas no coinciden.')
            else:
                usuario.email = informacion['email']
                if informacion["password1"]:
                    usuario.set_password(informacion["password1"])
                usuario.last_name = informacion['last_name']
                usuario.first_name = informacion['first_name']
                usuario.save()

                # Actualiza o crea el avatar
                avatar, created = Avatar.objects.get_or_create(user=usuario)
                if informacion.get("imagen"):
                    avatar.imagen = informacion["imagen"]
                    avatar.save()

                return render(request, 'app/index.html')  # O la URL que prefieras redirigir después de guardar

    else:
        datos = {
            'first_name': usuario.first_name,
            'email': usuario.email
        }
        miFormulario = UserEditForm(initial=datos)

    return render(request, "users/edit.html", {"mi_form": miFormulario, "usuario": usuario})

@login_required
def some_view(request):
    user_avatar = None
    try:
        avatar = Avatar.objects.get(user=request.user)
        user_avatar = avatar.imagen.url
    except Avatar.DoesNotExist:
        pass
    
    context = {
        'user_avatar': user_avatar,
    }
    return render(request, 'app/index.html', context)

def logout_view(request):
    logout(request)
    return redirect('app/index.html')


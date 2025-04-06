#En este archivo se encontrara toda la logica de los middlewares que se necesiten para el funcionamiento de la aplicacion, ejemplo que los usuarios no puedan acceder si no estan logeados.

from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings

class LoginRequeridoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vistas que no requieren login (nombre definido en las urls)
        vistas_publicas = ['login']

        # Si no está autenticado...
        if not request.user.is_authenticated:
            try:
                nombre_vista = resolve(request.path_info).url_name
            except:
                nombre_vista = None

            if nombre_vista not in vistas_publicas:
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)


class EmpleadoRestringidoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            nombre_vista = resolve(request.path_info).url_name
        except:
            nombre_vista = None

        # Si el usuario está autenticado y es EMPLEADO
        if request.user.is_authenticated and request.user.groups.filter(name='Empleado').exists():


            # Vistas que el EMPLEADO puede ver
            vistas_permitidas_empleado = ['home', 'listarPeriodosDeEmpleado', 'salir']

            if nombre_vista not in vistas_permitidas_empleado:
                return redirect('home')

        return self.get_response(request)

from pathlib import Path
import os
import django
from datetime import date

import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_DIR = Path(__file__).resolve().parent.parent.parent
#settings_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\settings.py"

print(BASE_DIR)

# Agrega el directorio raíz al sys.path para que Python lo encuentre
sys.path.append(str(BASE_DIR))

# Configurar Django para el script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_dir)
django.setup()

from core.models import Cliente, Inmueble, Producto, Categoria, Empleado
from servicios.models import TipoServicio, Servicio
from facturas.models import Factura
from turnos.models import Horario, Periodo

def load_tests_data():
    # Eliminar datos previos (Opcional)
    Cliente.objects.all().delete()
    Inmueble.objects.all().delete()
    Producto.objects.all().delete()
    Categoria.objects.all().delete()
    Empleado.objects.all().delete()
    TipoServicio.objects.all().delete()
    Servicio.objects.all().delete()
    Factura.objects.all().delete()
    Horario.objects.all().delete()
    Periodo.objects.all().delete()

    print("📌 Cargando datos de prueba...")

    # Crear Clientes
    cliente1 = Cliente.objects.create(
        cuil_cuit="20-12345678-9", apellido="Gómez", nombre="Juan", correo="juan@example.com", habitual=True
    )
    cliente2 = Cliente.objects.create(
        cuil_cuit="27-87654321-5", apellido="Martínez", nombre="Ana", correo="ana@example.com", gubernamental=True
    )

    # Crear Inmuebles
    inmueble1 = Inmueble.objects.create(
        domicilio="Calle Falsa 123", metrosCuadrados=80, nroAmbientes=3, tipo="casa", cliente=cliente1
    )
    inmueble2 = Inmueble.objects.create(
        domicilio="Av. Siempre Viva 742", metrosCuadrados=120, nroAmbientes=4, tipo="oficina", cliente=cliente2
    )

    # Crear Productos
    producto1 = Producto.objects.create(
        descripcion="Limpiador Multiusos", stock=50, precioUnitario=250.00
    )
    producto2 = Producto.objects.create(
        descripcion="Escoba Industrial", stock=30, precioUnitario=500.00
    )

    # Crear Categorías
    categoria1 = Categoria.objects.create(
        nombre="Media Jornada", sueldoBase=58000.00
    )
    categoria2 = Categoria.objects.create(
        nombre="Jornada Completa", sueldoBase=120000.00
    )

    # Crear Empleados
    empleado1 = Empleado.objects.create(
        nombre="Carlos", apellido="Pérez", correo="carlos@example.com", cuil="20-11223344-9", categoria=categoria1
    )
    empleado2 = Empleado.objects.create(
        nombre="María", apellido="López", correo="maria@example.com", cuil="27-55667788-5", categoria=categoria2
    )

    # Crear Tipos de Servicio
    tipo_servicio1 = TipoServicio.objects.create(descripcion="Limpieza profunda", ganancia=30)
    tipo_servicio2 = TipoServicio.objects.create(descripcion="Mantenimiento general", ganancia=25)

    # Crear Servicios
    # servicio1 = Servicio.objects.create(
    #    desde=date.today(),
    #    hasta=date.today(),
    #    estado="contratado",
    #    cantidadEstimadaEmpleados=3,
    #    diasSemana=5,
    #    ajuste=10,
    #    inmueble=inmueble1,
    #   total=10000.00
    #)

    # Crear Facturas
    #factura1 = Factura.objects.create(
    #    servicio=servicio1, total=10000.00, emision=date.today(), formaPago="transferencia"
    #)

    print("✅ Datos de prueba cargados exitosamente.")

if __name__ == "__main__":
    load_tests_data()


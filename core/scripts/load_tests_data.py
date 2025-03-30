from pathlib import Path
import os
import django
from datetime import date, timedelta
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Agrega el directorio raíz al sys.path para que Python lo encuentre
sys.path.append(str(BASE_DIR))

# Configurar Django para el script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from core.models import Cliente, Inmueble, Producto, Categoria, Empleado
from servicios.models import TipoServicio, Servicio
from facturas.models import Factura
from turnos.models import Horario

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

    print("📌 Cargando datos de prueba...")

    # Crear Clientes
    cliente1 = Cliente.objects.create(
        cuil_cuit="20-12345678-9", apellido="Gómez", nombre="Juan", correo="juan@example.com", habitual=True
    )
    cliente2 = Cliente.objects.create(
        cuil_cuit="27-87654321-5", apellido="Martínez", nombre="Ana", correo="ana@example.com", gubernamental=True
    )
    cliente3 = Cliente.objects.create(
        cuil_cuit="23-98765432-1", apellido="Fernández", nombre="Luis", correo="luis@example.com"
    )

    # Crear Inmuebles
    inmueble1 = Inmueble.objects.create(
        domicilio="Calle Falsa 123", metrosCuadrados=80, nroAmbientes=3, tipo="casa", cliente=cliente1
    )
    inmueble2 = Inmueble.objects.create(
        domicilio="Av. Siempre Viva 742", metrosCuadrados=120, nroAmbientes=4, tipo="oficina", cliente=cliente2
    )
    inmueble3 = Inmueble.objects.create(
        domicilio="Boulevard 2000", metrosCuadrados=200, nroAmbientes=5, tipo="salon", cliente=cliente3
    )

    # Crear Productos
    producto1 = Producto.objects.create(
        descripcion="Limpiador Multiusos", stock=50, precioUnitario=250.00
    )
    producto2 = Producto.objects.create(
        descripcion="Escoba Industrial", stock=30, precioUnitario=500.00
    )
    producto3 = Producto.objects.create(
        descripcion="Desinfectante", stock=40, precioUnitario=320.00
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
    empleado3 = Empleado.objects.create(
        nombre="Lucía", apellido="Ramírez", correo="lucia@example.com", cuil="23-99887766-2", categoria=categoria1
    )

    # Crear Tipos de Servicio
    tipo_servicio1 = TipoServicio.objects.create(descripcion="Limpieza profunda", ganancia=30)
    tipo_servicio2 = TipoServicio.objects.create(descripcion="Mantenimiento general", ganancia=25)

    # Crear Servicios
    desde1 = date.today()
    hasta1 = desde1 + timedelta(weeks=1)
    servicio1 = Servicio.objects.create(
        desde=desde1,
        hasta=hasta1,
        estado="contratado", # En realidad el estado creo que no importa, porque al principio siempre se pone en presupuestado
        cantidadEstimadaEmpleados=3,
        diasSemana=5,
        ajuste=10,
        inmueble=inmueble1,
        total=10000.00
    )

    desde2 = date.today() + timedelta(days=3)
    hasta2 = desde2 + timedelta(weeks=5)
    servicio2 = Servicio.objects.create(
        desde=desde2,
        hasta=hasta2,
        estado="presupuestado",
        cantidadEstimadaEmpleados=2,
        diasSemana=3,
        ajuste=5,
        inmueble=inmueble2,
        total=7500.00
    )

    desde3 = date.today() + timedelta(days=7)
    hasta3 = desde3 + timedelta(weeks=10)
    servicio3 = Servicio.objects.create(
        desde=desde3,
        hasta=hasta3,
        estado="pagado",
        cantidadEstimadaEmpleados=4,
        diasSemana=6,
        ajuste=15,
        inmueble=inmueble3,
        total=15000.00
    )   

    # Crear Facturas
    # Factura.objects.create(servicio=servicio1, total=10000.00, emision=date.today(), formaPago="transferencia")
    # Factura.objects.create(servicio=servicio2, total=7500.00, emision=date.today(), formaPago="efectivo")
    # Factura.objects.create(servicio=servicio3, total=15000.00, emision=date.today(), formaPago="tarjeta")

    print("✅ Datos de prueba cargados exitosamente.")

if __name__ == "__main__":
    load_tests_data()


from faker import Faker
import os
import shutil
import subprocess
import django
import sys
from pathlib import Path
from datetime import date, timedelta
import random

# ========== SETUP DJANGO ========== #
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Cliente, Inmueble, Producto, Categoria, Empleado
from servicios.models import TipoServicio, Servicio, ServicioCantidadEmpleado, TipoEstado
from facturas.models import Factura
from turnos.models import Horario, Periodo

fake = Faker("es_ES")

# ========== FUNCIONES ========== #

def borrar_contenido(carpeta):
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        for elemento in os.listdir(carpeta):
            path = os.path.join(carpeta, elemento)
            if path.endswith("__init__.py"):
                continue
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                print(f"🗑️ Archivo eliminado: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"🗑️ Carpeta eliminada: {path}")
    else:
        print(f"⚠️ La carpeta no existe: {carpeta}")

def ejecutar_comando(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Error al ejecutar: {cmd}")
        exit(result.returncode)

def load_tests_data():
    Cliente.objects.all().delete()
    Inmueble.objects.all().delete()
    Producto.objects.all().delete()
    Categoria.objects.all().delete()
    Empleado.objects.all().delete()
    TipoServicio.objects.all().delete()
    ServicioCantidadEmpleado.objects.all().delete()
    Servicio.objects.all().delete()
    Factura.objects.all().delete()
    Horario.objects.all().delete()
    Periodo.objects.all().delete()

    print("📌 Cargando datos de prueba...")

    # Clientes
    clientes = []
    for _ in range(15):
        cliente = Cliente.objects.create(
            cuil_cuit=str(fake.unique.random_number(digits=11)),
            apellido=fake.last_name(),
            nombre=fake.first_name(),
            correo=fake.unique.email(),
            habitual=random.choice([True, False]),
            gubernamental=random.choice([True, False])
        )
        clientes.append(cliente)

    # Inmuebles
    inmuebles = []
    tipos = ["casa", "oficina", "salon", "departamento"]
    for _ in range(15):
        inmueble = Inmueble.objects.create(
            domicilio=fake.street_address(),
            metrosCuadrados=random.randint(50, 300),
            nroAmbientes=random.randint(2, 8),
            tipo=random.choice(tipos),
            cliente=random.choice(clientes)
        )
        inmuebles.append(inmueble)

    # Productos
    for _ in range(15):
        Producto.objects.create(
            descripcion=fake.word().capitalize() + " " + fake.word().capitalize(),
            stock=random.randint(10, 100),
            precioUnitario=round(random.uniform(100, 1000), 2)
        )

    # Categorías
    categorias = []
    for i in range(5):
        categoria = Categoria.objects.create(
            nombre=f"Categoría {i+1}",
            sueldoBase=round(random.uniform(50000, 150000), 2)
        )
        categorias.append(categoria)

    # Empleados
    for _ in range(15):
        Empleado.objects.create(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            correo=fake.unique.email(),
            cuil=str(fake.unique.random_number(digits=11)),  # <- CONVERTIDO A STRING
            categoria=random.choice(categorias)
        )

    # Tipos de Servicio
    tipos_servicio = []
    for _ in range(10):
        tipo = TipoServicio.objects.create(
            descripcion=fake.sentence(nb_words=3).rstrip('.'),
            ganancia=random.randint(10, 50)
        )
        tipos_servicio.append(tipo)

    # Servicios y cantidades por categoría
    for _ in range(10):
            desde = fake.date_between(start_date="-30d", end_date="today")
            hasta = desde + timedelta(weeks=random.randint(1, 10))

            servicio = Servicio.objects.create(
                desde=desde,
                hasta=hasta,
                diasSemana=random.randint(1, 6),
                ajuste=random.randint(0, 20),
                inmueble=random.choice(inmuebles),
                total=round(random.uniform(8000, 30000), 2),
                fecha_presupuesto=desde  # Nuevo campo agregado
            )

            # Agregar de 1 a 3 cantidades por categoría (sin duplicar categoría)
            categorias_elegidas = random.sample(categorias, k=random.randint(1, min(3, len(categorias))))
            for categoria in categorias_elegidas:
                ServicioCantidadEmpleado.objects.create(
                    servicio=servicio,
                    categoria=categoria,
                    cantidad=random.randint(1, 4)
                )



    print("✅ Datos de prueba cargados exitosamente.")

# ========== MAIN ========== #
if __name__ == "__main__":
    print("🧹 Limpiando migraciones y cachés...")

    carpetas_migrations = [
        "core/migrations", "core/__pycache__",
        "turnos/migrations", "turnos/__pycache__",
        "servicios/migrations", "servicios/__pycache__",
        "facturas/migrations", "facturas/__pycache__"
    ]
    for carpeta in carpetas_migrations:
        borrar_contenido(carpeta)

    db_path = "db.sqlite3"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗃️ Base de datos eliminada: {db_path}")

    print("\n📦 Generando nuevas migraciones...")
    ejecutar_comando("python manage.py makemigrations")

    print("\n⚙️ Aplicando migraciones...")
    ejecutar_comando("python manage.py migrate")

    print("\n👤 Creando superusuario admin/admin...")
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin")
        print("✅ Superusuario creado: admin / admin")
    else:
        print("⚠️ Ya existe un usuario llamado 'admin'")

    print("\n🧪 Cargando datos de prueba...")
    load_tests_data()

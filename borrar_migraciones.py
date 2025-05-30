import os
import shutil

def borrar_contenido(carpeta):
    if os.path.exists(carpeta) and os.path.isdir(carpeta):
        for elemento in os.listdir(carpeta):
            path = os.path.join(carpeta, elemento)
            if path.endswith("__init__.py"):
                continue
            
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)  
                print(f"Archivo eliminado: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path) 
                print(f"Carpeta eliminada: {path}")
    else:
        print(f"La carpeta no existe: {carpeta}")

if __name__ == "__main__":
    carpetas_migrations = [
        "core/migrations",
        "core/__pycache__",
        "turnos/migrations",
        "turnos/__pycache__",
        "servicios/migrations",
        "servicios/__pycache__",
        "facturas/migrations",
        "facturas/__pycache__"
    ]

    
    for carpeta in carpetas_migrations:
        borrar_contenido(carpeta)

    db_path = "db.sqlite3"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Base de datos eliminada: {db_path}")
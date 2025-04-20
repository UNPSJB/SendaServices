#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time


def run_crons():
    import django
    from django.core.management import call_command

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

    while True:
        print("⏱ Ejecutando crons en segundo plano...")
        call_command("runcrons")
        time.sleep(60)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    if 'runserver' in sys.argv:
        threading.Thread(target=run_crons, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()

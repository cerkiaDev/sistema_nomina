#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Modificar el comando runserver para usar puerto 3000 por defecto
    if 'runserver' in sys.argv and len(sys.argv) == 2:
        sys.argv.append('3000')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_nomina.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

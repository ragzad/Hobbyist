"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Get the absolute path to the directory containing manage.py (project root)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add the 'outer core' directory to sys.path.
    sys.path.insert(0, os.path.join(base_dir, 'core'))

    # Add the 'apps' directory within 'core' to sys.path.
    sys.path.insert(0, os.path.join(base_dir, 'core', 'apps'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.core.settings")
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
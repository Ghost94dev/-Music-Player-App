"""
WSGI config for MusicPlayer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicPlayer.settings')

application = get_wsgi_application()

# Add this for Render deployment
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    import sys

    # For local development
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        execute_from_command_line(sys.argv)

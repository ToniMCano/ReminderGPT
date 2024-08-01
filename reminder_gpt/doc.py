import os
import sys
import pydoc

# Configura Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'reminder_gpt.settings'
import django
django.setup()

# Lista de módulos para documentar
modules = ['core', 'core.chat_views', 'core.models', 'core.views', 'core.forms']

# Generar la documentación para cada módulo
for module in modules:
    try:
        pydoc.writedoc(module)
    except Exception as e:
        print(f"Error generating documentation for {module}: {e}")
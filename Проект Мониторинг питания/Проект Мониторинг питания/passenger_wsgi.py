import sys
import os

# Укажите путь к вашему виртуальному окружению
venv_path = '/home/YOUR_LOGIN/sites/YOUR_DOMAIN/venv/bin/activate_this.py'
exec(open(venv_path).read(), dict(__file__=venv_path))

# Укажите путь к вашему приложению
sys.path.insert(0, '/home/YOUR_LOGIN/sites/YOUR_DOMAIN')

# Импортируйте приложение Flask
from app import app as application  # Замените 'app' на имя вашего модуля, если он отличается

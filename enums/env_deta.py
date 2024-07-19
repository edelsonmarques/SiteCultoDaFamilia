import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('DETA_PROJECT_KEY'):
    projeto_key = os.getenv('DETA_PROJECT_KEY')
else:
    projeto_key = '{{DETA_PROJECT_KEY}}'

if os.getenv('FIREBASE_URL'):
    FIREBASE_URL = os.getenv('FIREBASE_URL')
else:
    FIREBASE_URL = '{{FIREBASE_URL}}'

if os.getenv('DJANGO_SECRET_KEY'):
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = '{{DJANGO_SECRET_KEY}}'

if os.getenv('MYSQL_USER'):
    MYSQL_USER = os.getenv('MYSQL_USER')
else:
    MYSQL_USER = '{{MYSQL_USER}}'
    
if os.getenv('MYSQL_PASSWORD'):
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
else:
    MYSQL_PASSWORD = '{{MYSQL_PASSWORD}}'
    
if os.getenv('MYSQL_HOST'):
    MYSQL_HOST = os.getenv('MYSQL_HOST')
else:
    MYSQL_HOST = '{{MYSQL_HOST}}'

if os.getenv('MYSQL_PORT'):
    MYSQL_PORT = os.getenv('MYSQL_PORT')
else:
    MYSQL_PORT = '{{MYSQL_PORT}}'

if os.getenv('DETA_SORTEIO'):
    DETA_SORTEIO = os.getenv('DETA_SORTEIO')
else:
    DETA_SORTEIO = '{{DETA_SORTEIO}}'

if os.getenv('DETA_USER'):
    DETA_USER = os.getenv('DETA_USER')
else:
    DETA_USER = '{{DETA_USER}}'
    
    

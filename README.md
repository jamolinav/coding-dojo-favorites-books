# Favorites Books

Crear virtual environment:
```python3 -m venv venv```

Luego instalar componentes de python:
```pip install -r requirements.txt```

## Django con Postgres(macOS) 
### Cómo solucionar problemas de instalación del controlador Psycopg2.
### Instala los controladores necesarios para la base de datos
```pip install psycopg2```

### Cambiar la configuración de la base de datos de Django
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # cambiar la base de datos a postgres
        'NAME': 'first_postgres_db', # nombre de la base de datos, se creará en el servidor de Postgres a continuación
        'USER': 'pkrull', # postgres para macOS o 'USER': 'postgres', para Windows
        'PASSWORD': 'password', # contraseña a la que la cambió al instalar Postgres
        'HOST': '127.0.0.1', # dirección IP localhost
        'PORT': '5432', # puerto del servidor postgres predeterminado
    }
}
```
### Crea el esquema de la base de datos en Postgres
```psql postgres```

Enumera las bases de datos disponibles actualmente usando \l.
```\l```

Crea una nueva base de datos postgres. CREATE DATABASE first_postgres_db;
```CREATE DATABASE first_postgres_db;```

Para conectarte a la base de datos, utiliza \c first_postgres_db;
```
\c first_postgres_db;
You are now connected to database "first_postgres_db" as user "pkrull".
```

En este punto, abre una nueva ventana de bash a nuestro proyecto Django y migra.
```python manage.py migrate```

## (macOS) Cómo solucionar problemas de instalación del controlador Psycopg2.
```brew install openssl```

Es muy probable que esto le dé una advertencia diciendo que openssl ya está instalado
Utiliza brew para vincular la libreria openssl.
```brew link openssl```

Crear variables de ambiente
```
export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"
export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"
```

Y vuelva a intentar con:
```pip install psycopg2```


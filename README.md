# E-commerce challenge with Django Rest Framework 

## Configuración inicial

Este proyecto incluye migraciones predeterminadas, también incluye una base de datos SQLITE con datos de ejemplo.

1.- Clonar este repositorio:

    git clone https://github.com/nelsonarg34/ecommerce-challenge.git

2.- Crear un entorno virtual:

    virtualenv venv

3.- Active el entorno virtual.

4.- Instalar librerias.

    (venv) pip install -r requirements.txt 

5.- Correr servidor:

    venv) python manage.py runserver 
<br>

## Autenticación y registro de usuarios

### Características
- Registrar una cuenta
- Iniciar y cerrar sesión
- Restaurar contraseña
- Obtener Token
- Refrescar Token

###     End points

####    rest-auth-jwt

    http://localhost:8000/api/user/auth/login/

    http://localhost:8000/api/user/auth/logout/

    http://localhost:8000/api/user/auth/password/reset/

    http://localhost:8000/api/user/auth/password/reset/confirm/

    http://localhost:8000/api/user/auth/user/

    http://localhost:8000/api/user/auth/obtain_token/

    http://localhost:8000/api/user/auth/refresh_token/

####    Api Root Users

Users (GET, POST): 

    http://localhost:8000/api/user/users/

Users (GET, PUT, PATCH, DELETE): 

    http://127.0.0.1:8000/api/lists/<id_user>/

<br>

## Productos y categorías de productos

### Características
- Registrar/Editar un producto
- Eliminar un producto
- Consultar un producto
- Listar todos los productos
- Modificar stock de un producto

###     End points

####    Api Root Product and Category

Listar todos los productos o crear un producto (GET, POST)

    http://127.0.0.1:8000/api/product/products/

Editar o eliminar un producto (GET, PUT, PATCH, DELETE)

    http://127.0.0.1:8000/api/product/products/<id_product>/

Listar y crear una categoría de producto (GET, POST)

    http://127.0.0.1:8000/api/product/categories/

Editar o eliminar una categoría de producto (GET, PUT, PATCH, DELETE)

    http://127.0.0.1:8000/api/product/categories/<id_category>

<br>

## Ordenes y Detalle de Orden

### Características
- Registrar/Editar una orden (inclusive sus detalles)
- Eliminar una orden
- Consultar una orden y sus detalles
- Listar todas las ordenes
- Modificar una orden

###     End points

####    Api Root Order and OrderDetail

Listar todos los detalles de las órdenes o crear una orden con sus detalles (GET, POST)
Crea un ítem de producto y lo agrega a una orden activa, si no existe una orden se crea.
Si la orden existe pero paso mas de 60 minutos desde su creación, esta última cambia su estado 
a "Cancelado" y se genera una nueva. 
Con la creación de la orden y su ítem (OrderDetail), se actualiza el stock del producto seleccionado.
No se pueden generar items de productos iguales, si se desea mas de un mismo producto, modificar el campo
quantity de la orden.

    http://127.0.0.1:8000/api/order/orders_detail/

Editar o eliminar un detalle de orden (GET, PUT, PATCH, DELETE)

    http://127.0.0.1:8000/api/order/orders_detail/<id_order_detail>/

Listar todas las ordenes con sus detalles (GET, POST)

    http://127.0.0.1:8000/api/order/orders/

Editar o eliminar una orden incluido sus detales (GET, PUT, PATCH, DELETE)

    http://127.0.0.1:8000/api/order/orders/<id_order>

<br>


## Búsquedas y filtros

- Búsqueda: Usando un texto y buscando coincidencias.
- Ordenación: Ascendente o descendente a partir de varios campos.
- Filtrado: En base a a partir de varios campos.

###     End points

http://127.0.0.1:8000/api/list_filters/

<br>

## Proyecto con Docker

1.- Creación del proyecto:

    docker-compose run web django-admin startproject <nombre-proyecto> 

2.- Construcción del contenedor:

    docker-compose -f docker-compose.yml build

3.- Modificar el archivo settings.py del proyecto:

Realizar las siguientes modificaciones para poder comunicarnos con nuestra base de datos.

    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_HOST'],
            'PORT': os.environ['POSTGRES_PORT'],
        }
    }

4.- Correr build y up:

    docker-compose -f docker-compose.yml build
    docker-compose up

5.- Correr  makemigrations y migrate:

    docker-compose -f .\docker-compose.yml run --rm web python manage.py makemigrations
    docker-compose -f .\docker-compose.yml run --rm web python manage.py migrate

6.- Crear super usuario:

    docker-compose -f .\docker-compose.yml run --rm web python manage.py createsuperuser

6.- Con el contenedor corriendo:

    Acceder a http://localhost:8000/admin



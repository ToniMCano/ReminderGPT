# Demo GPT

Demo GPT es una aplicación Django que permite consultar información de tu base de datos mediante conversaciones con una inteligencia artificial basada en OpenAI. La aplicación incluye funcionalidades de registro, inicio de sesión, chat y más.

## Índice

- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Pruebas](#pruebas)


## Instalación

1. **Clonar el Repositorio**


   ```sh
    git clone https://github.com/ToniMCano/ReminderGPT
   ```

2. **Crear y Activar el Entorno Virtual**

   ```sh
    python -m venv venv
    source venv/bin/activate  # Para Windows usa `venv\Scripts\activate`
   ```

3. **Instalar las Dependencias**

   ```sh
    pip install -r requirements.txt
    ```

3. **Configurar el Proyecto**

    * Crea un archivo ***.env*** en el directorio raíz del  proyecto con las siguientes variables:

    ```sh
     OPENAI_API_KEY=tu_clave_api_openai
    ```

* Ejecuta las migraciones para configurar la base de datos:
    ```
     python manage.py migrate
    ```
---
## Uso

1. **Iniciar el Servidor de Desarrollo**

```
python manage.py runserver
```
2. **Navegar la aplicación**

Abre tu navegador y ve a http://127.0.0.1:8000/ para interactuar con la aplicación.

O puedes probarla desde aquí https://tonitest.pythonanywhere.com .

---
# Estructura del Proyecto

## Paquete `core` de la aplicación.
 
El paquete `core` incluye los módulos principales para la funcionalidad de la aplicación, como vistas, modelos y formularios. Estos módulos gestionan la lógica de negocio, la interacción con la base de datos y los formularios para la creación y autenticación de usuarios.
 
**Módulos:**
 
- `views.py`: Define las vistas que manejan la lógica de negocio de la aplicación, incluyendo la autenticación de usuarios
- `chat_views.py`: Define las vistas que manejan la lógica de negocio de la aplicación relacionada con la interacción con OpenAI para el chat.y la interacción con OpenAI para el chat.
- `models.py`: Define los modelos de datos utilizados en la aplicación, incluyendo un perfil de usuario extendido con un número de teléfono.
- `forms.py`: Define los formularios utilizados en la aplicación para la creación y autenticación de usuarios.
 
**Uso:**
 
Este paquete se utiliza para gestionar la funcionalidad principal de la aplicación, incluyendo la lógica de negocio, la interacción con la base de datos y la validación de formularios.


<br>

### Módulos Principales

**`core/views.py:`** Este módulo contiene las vistas para la aplicación principal, gestionando la autenticación de usuarios y el registro.
 
Las funciones incluidas son:

>.
>**- home(request):** Renderiza la página de inicio y maneja el formulario de inicio de sesión.
>**- sign_up(request):** Renderiza la página de registro de >usuario y maneja el formulario de registro.
>**- create_user(request):** Renderiza la página de creación de >usuario con el formulario de registro.
> 
>Cada vista procesa las solicitudes HTTP y devuelve respuestas HTTP correspondientes, incluyendo la lógica para autenticación de usuarios y gestión de formularios.
> <br>
>**Importaciones:** <br>
>**- django.shortcuts:** Utilizado para renderizar plantillas y >redirigir vistas.
>**- django.contrib.auth.models:** Modelos de autenticación >proporcionados por Django.
>**- django.contrib.auth:** Funciones de autenticación >proporcionadas por Django.
>**- .forms:** Formularios personalizados para el inicio de >sesión y registro de usuarios.
>**- django.urls:** Herramientas para la gestión de rutas URL.
>**- django.http:** Utilizado para generar respuestas HTTP.
><br>

<br>

 
**Uso:**
Estas vistas son utilizadas en las plantillas de la aplicación principal para gestionar la autenticación y el registro de usuarios, proporcionando una interfaz sencilla y segura para los usuarios de la aplicación.
 
<br>

**Funciones**


```
home(request)

    Maneja la solicitud para la página de inicio, que incluye la lógica de autenticación de usuarios.

    Esta vista gestiona la visualización y procesamiento de un formulario de inicio de sesión. Si la solicitud es 
    de tipo POST, se intenta autenticar al usuario con las credenciales proporcionadas. Si la autenticación es exitosa, 
    el usuario se registra en la sesión y se redirige a la página de chat. Si la autenticación falla, se muestra un mensaje 
    de error en el formulario. Si la solicitud es de tipo GET, se muestra un formulario vacío.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.

    Retorna:
    HttpResponse: La respuesta renderizada que contiene el formulario de inicio de sesión y el título de la página.
    
    En caso de autenticación exitosa, redirige al usuario a la vista 'chat'. En caso de error de autenticación, muestra
    un mensaje de error en el formulario de inicio de sesión.

```
```
sign_up(request)
Renderiza la página de registro de usuario y maneja el formulario de registro.
 
Args:
request (HttpRequest): La solicitud HTTP.
 
Returns:
HttpResponse: La respuesta HTTP con el formulario de registro y un indicador de validez.
Si nos válido muestra un mensaje en el FrontEnd.
```
```
create_user(request)
Renderiza la página de creación de usuario con el formulario de registro.
 
Args:
request (HttpRequest): La solicitud HTTP.
 
Returns:
HttpResponse: La respuesta HTTP con el formulario de registro.
```


<br>

---

<br>

**`core/chat_views.py:`** Módulo que gestiona las vistas de la aplicación, incluyendo la autenticación de usuarios y la integración con OpenAI.
 
Este módulo incluye las siguientes funciones:
>.
>**- chat(request):** Renderiza la página del chat.
>
>**- send_message(request):** Maneja el envío de mensajes desde el chat >y retorna una respuesta de OpenAI.
>
>**- openai_response(request, query):** Genera una respuesta de OpenAI >basada en la consulta del usuario y mantiene el historial de la >conversación.
>
>**Importaciones:** <br>
>**- django.shortcuts:** Utilizado para renderizar plantillas y redirigir vistas.
>**- django.contrib.auth.models:** Modelos de autenticación proporcionados por Django.
>**- django.contrib.auth:** Funciones de autenticación proporcionadas por Django.
>**- .forms:** Formularios personalizados para el inicio de sesión y >registro de usuarios.
>**- django.urls:** Herramientas para la gestión de rutas URL.
>**- django.http:** Utilizado para generar respuestas HTTP.
>**- openai:** Biblioteca para interactuar con la API de OpenAI.
>**- decouple:** Utilizado para manejar variables de entorno.
>**- ast:** Utilizado para evaluar expresiones en cadena.
>**- logging:** Utilizado para el registro de eventos y errores.
>**- django.contrib.auth.decorators**: Decoradores para vistas que requieren autenticación.
> <br>

<br>

**Uso:**
Estas vistas son utilizadas en las plantillas de la aplicación principal para gestionar la autenticación y el registro de usuarios, así como la interacción con la API de OpenAI para generar respuestas en el chat.

<br>

**Funciones** 


```
chat(request)
Renderiza la página del chat. Requiere que el usuario esté autenticado.
 
Args:
request (HttpRequest): La solicitud HTTP.
 
Returns:
HttpResponse: La respuesta HTTP con la página del chat.
```

```
openai_response(request, query)
Genera una respuesta de OpenAI basada en la consulta del usuario y mantiene el historial de la conversación.
 
Args:
request (HttpRequest): La solicitud HTTP.
query (str): La consulta del usuario para OpenAI.
 
Returns:
list: Una lista con la respuesta de OpenAI y el número de ancla como cadena.
```

```
send_message(request)
Maneja el envío de mensajes desde el chat y retorna una respuesta de OpenAI.
 
Args:
request (HttpRequest): La solicitud HTTP.
 
Returns:
JsonResponse: La respuesta en formato JSON con el mensaje de OpenAI o un error.
```

<br>

---

<br>


**`core/chat_views.py:`** Módulo que gestiona los modelos de la aplicación, incluyendo la validación y extensión del modelo de usuario.
 
Este módulo incluye las siguientes clases y funciones:
>.
>***Clases:***<br>
>**- Profile:** Extiende el modelo de usuario con un número de teléfono.
><br>
>
>***Funciones:*** <br>
>**- validate_phone(value):** Valida que el número de teléfono tenga exactamente 9 dígitos y contenga solo números. 
><br>
>**Importaciones:** <br>
>**- django.db.models:** Utilizado para definir modelos en Django.
>**- django.utils.timezone.now:** Utilizado para trabajar con fechas y horas.
>**- django.contrib.auth.models.User:** Modelo de usuario proporcionado por Django.
>**- django.core.exceptions.ValidationError:** Utilizado para manejar errores de validación.
> <br>

<br>

**Uso:**

Este módulo se utiliza para definir y manejar los datos adicionales del perfil del usuario, específicamente el número de teléfono, y para validar estos datos.
<br>

### class Profile(django.db.models.base.Model)
<br>

``` 
Clase Profile
Extiende el modelo de usuario con un número de teléfono.
 
Args:
user (User): Relaciona el perfil con un objeto de la clase User.
tlf (str): El número de teléfono del usuario (debe tener exactamente 9 dígitos).
 
Methods:
__str__(): Retorna una cadena que representa el perfil del usuario.
    
```
**Funciones** 
``` 
validate_phone(value)
Valida que el número de teléfono tenga exactamente 9 dígitos y contenga solo números.
 
Args:
value (str): El número de teléfono a validar.
 
Raises:
ValidationError: Si el número de teléfono no tiene exactamente 9 dígitos o contiene caracteres no numéricos.
    
```

<br>

---

<br>

**`core/forms.py:`** Módulo que define los formularios utilizados en la aplicación para la creación y autenticación de usuarios.
 
Este módulo incluye las siguientes clases:
 


>.
>**- SignUpForm:** Formulario para registrar un nuevo usuario,>incluyendo un número de teléfono.
>
>**- LoginForm:** Formulario para que un usuario inicie sesión.
> 
>***Importaciones:***
> 
>**- django.forms:** Utilizado para definir los campos del >formulario.
> 
>**- django.contrib.auth.forms.UserCreationForm:** Utilizado como >base para el formulario de registro de usuarios.
> 
>**- django.contrib.auth.models.User, Group:** Modelos de usuario y >grupo proporcionados por Django.
><br>
 
**Uso:**
Este módulo se utiliza para gestionar los formularios de registro y autenticación de usuarios, validando los datos introducidos y asociando perfiles y grupos a los usuarios creados.
<br>

### class SignUpForm(django.contrib.auth.forms.UserCreationForm)
<br>

```
SignUpForm(*args, **kwargs)
 
Clase SignUpForm
Incluye los campos necesarios para registrar un nuevo usuario, incluyendo un número de teléfono. 
Por defecto, todos los campos son obligatorios.
 
Args:
username : Es un string que compone el nombre de usuario.
email : Es un string que compone el correo electrónico del usuario.
password1 : Es un string que compone la primera entrada de la contraseña del usuario.
password2 : Es un string que compone la segunda entrada de la contraseña del usuario para verificarla.
tlf : Es un string que compone el número de teléfono del usuario (debe ser numérico y tener exactamente 9 dígitos).
 
Methods:
clean_tlf: Comprueba que el teléfono solo contenga números y que la longitud sea de 9 dígitos.
save: Guarda el usuario creado y le asigna un perfil y grupo.
    
```
 <br>

```
clean_tlf(self)
Comprueba que el teléfono solo contenga números y que la longitud sea de 9 dígitos.
 
Raises:
forms.ValidationError: Si el teléfono contiene caracteres no numéricos o no tiene exactamente 9 dígitos.
 
Returns:
str: El número de teléfono validado.
```
 <br>

```
save(self, commit=True)

Guarda el usuario creado y le asigna un perfil y grupo.
 
Crea un usuario, su perfil asociado con el número de teléfono, y lo añade a un grupo predeterminado.
 
Args:
commit (bool): Indica si el objeto debe ser guardado en la base de datos inmediatamente.
 
Returns:
User: El usuario creado
```

 <br>

### LoginForm(django.forms.forms.Form)

```
Clase LoginForm
Incluye los campos necesarios para que un usuario inicie sesión.
 
Args:
user : Es un string que compone el nombre de usuario.
password :** Es un string que compone la contraseña del usuario.
```
 <br>

---

 <br>

## Pruebas
Para asegurarte de que todo el código funciona correctamente, puedes ejecutar las pruebas incluidas en el proyecto.

Ejecutar las Pruebas

```sh
   python manage.py test
```
Las pruebas están ubicadas en el directorio **tests/** y verifican la funcionalidad de vistas, modelos y formularios.

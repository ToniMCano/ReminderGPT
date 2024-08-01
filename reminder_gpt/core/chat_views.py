"""
Módulo que gestiona las vistas de la aplicación, incluyendo la autenticación de usuarios y la integración con OpenAI.

Este módulo incluye las siguientes funciones:

- chat(request): Renderiza la página del chat.
- send_message(request): Maneja el envío de mensajes desde el chat y retorna una respuesta de OpenAI.
- openai_response(request, query): Genera una respuesta de OpenAI basada en la consulta del usuario y mantiene el historial de la conversación.
- test_openai(query): (No utilizada) Genera una respuesta de OpenAI para pruebas específicas.
- test(request): Renderiza una página de prueba.
- send_messageWAIT(request): Proporciona un mensaje de prueba en formato JSON.

Importaciones:
- django.shortcuts: Utilizado para renderizar plantillas y redirigir vistas.
- django.contrib.auth.models: Modelos de autenticación proporcionados por Django.
- django.contrib.auth: Funciones de autenticación proporcionadas por Django.
- .forms: Formularios personalizados para el inicio de sesión y registro de usuarios.
- django.urls: Herramientas para la gestión de rutas URL.
- django.http: Utilizado para generar respuestas HTTP.
- openai: Biblioteca para interactuar con la API de OpenAI.
- decouple: Utilizado para manejar variables de entorno.
- ast: Utilizado para evaluar expresiones en cadena.
- logging: Utilizado para el registro de eventos y errores.
- django.contrib.auth.decorators: Decoradores para vistas que requieren autenticación.

Uso:
Estas vistas son utilizadas en las plantillas de la aplicación principal para gestionar la autenticación y el registro de usuarios, así como la interacción con la API de OpenAI para generar respuestas en el chat.
"""
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from .forms import SignUpForm , LoginForm
from django.urls import path , reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from openai import OpenAI
from decouple import config
import ast
import logging
#import markdown
from django.contrib.auth.decorators import login_required





#------------Chat------------

@login_required
def chat(request):
    """
    Renderiza la página del chat. Requiere que el usuario esté autenticado.

    Args:
    request (HttpRequest): La solicitud HTTP.

    Returns:
    HttpResponse: La respuesta HTTP con la página del chat.
    """
    
    return render(request , "core/chat.html")


def send_message(request):
    """
    Maneja el envío de mensajes desde el chat y retorna una respuesta de OpenAI.

    Args:
    request (HttpRequest): La solicitud HTTP.

    Returns:
    JsonResponse: La respuesta en formato JSON con el mensaje de OpenAI o un error.
    """
    
    try:
        if request.method == 'POST':
            message_text = request.POST.get('message')
            message = openai_response(request , message_text)
            #print(message)
            return JsonResponse({'message': message} , status = 200)
        
        return JsonResponse({'error': 'Invalid request'}, status=400)

    except:
        logging.exception("Ha habido un problema al envíar el mensaje")
        return JsonResponse({'error': 'Ha habido un problema al envíar el mensaje'}, status=500)



#------------ChatGPT------------

@login_required
def openai_response(request , query):
    """
    Genera una respuesta de OpenAI basada en la consulta del usuario y mantiene el historial de la conversación.

    Args:
    request (HttpRequest): La solicitud HTTP.
    query (str): La consulta del usuario para OpenAI.

    Returns:
    list: Una lista con la respuesta de OpenAI y el número de ancla como cadena.
    """
    
    try:
    
        client = OpenAI(
            
            api_key=config("OPENAI_API_KEY"),       
        )

        messages = request.session.get('messages', []) # Carga los mensajes de la sesión de este usuario si los hay. La sesión expira al cerrar la página o hcaer logout
        anchor = request.session.get('anchor_number', 0)
        anchor += 1
        
        if not messages:
            
            if request.user.username == "Luis":
                
                messages = [{'role' : 'system',
                        'content': "Me llamo Luis y soy muy severo, estoy obsesionado con las buenas prácticas de programación el testing y la documentación del código. Deber dirigir la conversación e intentar aprovechar en todo momento hacer alusión a esto para ganarte mi simpatía. No lo trates como una obsesión si no como una virtud"
                    }]
                
            else:
                print("ha entrado en su rol")

        messages.append({"role" : "user",
                    "content": query,
                    })

        chat_completion = client.chat.completions.create(       # Crea la respuesta en función a los messages, basándose en el modelo indicado (gpt-4o-mini)
                messages = messages , model="gpt-4o-mini", )
        
        answer = chat_completion.choices[0].message.content   #Devuelve el contenido
        
        messages.append({"role" : "assistant",
                    "content": answer ,}
        )
        
        request.session['messages'] = messages
        request.session['anchor_number'] = anchor
        print(len(request.session['messages']))
        return [answer , str(anchor)]
    
    except:
        return ["Algo ha salido mal" , str(0)]
    


def test_openai(query= "Creación del registro de usuarios en el  proyecto web de la universidad"): # No se usa, la eliminaré

    client = OpenAI(
        
        api_key=config("OPENAI_API_KEY"),       
    )

    messages = [{'role' : 'system',
                  'content': "Eres una asistente muy eficiente a la hora de guardar registros con la estructura nombre del proyecto , contenido de la nota, sabes determinar de manera precisa estos 2 campos y devolverlos como una lista de python. Ejemplo: ['Proyecto web de la universidad' , 'Creación del registro de usuarios'] "
                }]

    messages.append({"role" : "user",
                "content": query,
                })

    chat_completion = client.chat.completions.create(
            messages = messages , model="gpt-4o-mini", )
  
    messages.append({"role" : "assistant",
                "content": chat_completion ,}
    )
    
    output = ast.literal_eval(chat_completion.choices[0].message.content)
    if len(output) == 2:
        ok = "Cuela!!"
        print(output , type(output))
    else:
        ok = "No cuela"
    
    
    print(len(messages))

    return HttpResponse(f"{chat_completion.choices[0].message.content}---{ok}")  # Siempre debe devolverse algo en Django.

    

# Para hacer pruebas



def test(request):
    
    return render(request , "core/test.html")


def send_messageWAIT(request):
  
        message = ['''La propiedad `height: auto;` en CSS es una configuración muy útil que permite que la altura de un elemento se ajuste automáticamente al contenido que contiene. Aquí tienes más información sobre su uso, beneficios y ejemplos prácticos.\n\n### Detalles sobre `height: auto;`\n\n- **Ajuste Automático**: Cuando se establece `height: auto;`, el navegador calcula la altura del elemento de modo que se ajuste al contenido, evitando así que se produzcan desbordes o espacios no deseados.\n\n- **Comportamiento Predeterminado**: La mayoría de los elementos de bloque (`<div>`, `<p>`, etc.) tienen `height: auto;` por defecto. Esto significa que no es necesario especificarlo, pero es útil mencionarlo cuando se discuten otros estilos.\n\n- **Flexibilidad en Diseño**: Esta propiedad es perfecta para diseños responsivos, ya que permite que un elemento se expanda o contraiga automáticamente según sea necesario.\n\n### Ejemplo Práctico\n\nAquí tienes un ejemplo simple que demuestra cómo funciona `height: auto;`:\n\n```html\n<!DOCTYPE html>\n<html lang="es">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Ejemplo de height: auto;</title>\n    <style>\n        .contenedor {\n            width: 300px;                   /* Ancho del contenedor */\n            padding: 20px;                  /* Espaciado interno */\n            border: 2px solid #007BFF;      /* Borde azul */\n            background-color: #f0f8ff;      /* Fondo claro */\n            height: auto;                   /* Ajuste automático a contenido */\n       
 }\n    </style>\n</head>\n<body>\n\n<div class="contenedor">\n    <h2>Contenedor con altura automática</h2>\n    <p>Este es un ejemplo de cómo el contenedor se ajusta a la altura de su contenido.</p>\n    <p>Añadir más contenido aquí hará que el contenedor crezca automáticamente.</p>\n</div>\n\n</body>\n</html>\n```\n\n### Beneficios de `height: auto;`\n\n1. **Previene Desbordamientos**: Ayuda a evitar que el contenido se salga de los límites del contenedor.\n   \n2. **Ideal para Contenido Dinámico**: En aplicaciones web donde el contenido puede cambiar (como formularios o chats), la altura automática permite una mejor gestión del espacio.\n\n3. **Estética Mejorada**: Mantiene 
un diseño limpio y organizado al ajustar el tamaño del contenedor a lo que realmente necesita mostrar.\n\n### Conclusión\n\nUsar `height: auto;` es un enfoque común y recomendable para gestionar la altura de los elementos de manera dinámica. Si tienes alguna pregunta específica o necesitas más ejemplos relacionados con `height: auto;`, ¡déjamelo saber! Estoy aquí para ayudar.''', '29']

        print(message)
        return JsonResponse({'message': message})




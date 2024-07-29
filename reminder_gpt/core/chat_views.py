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
#import markdown
import base64





#------------Chat------------

def test(request):
    
    return render(request , "core/test.html")


def chat(request):
    
    return render(request , "core/chat.html")


def send_messageWAIT(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        message = openai_response(request , message_text)
        print(message)
        return JsonResponse({'message': message})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def send_message(request):
  
        message = ['''La propiedad `height: auto;` en CSS es una configuración muy útil que permite que la altura de un elemento se ajuste automáticamente al contenido que contiene. Aquí tienes más información sobre su uso, beneficios y ejemplos prácticos.\n\n### Detalles sobre `height: auto;`\n\n- **Ajuste Automático**: Cuando se establece `height: auto;`, el navegador calcula la altura del elemento de modo que se ajuste al contenido, evitando así que se produzcan desbordes o espacios no deseados.\n\n- **Comportamiento Predeterminado**: La mayoría de los elementos de bloque (`<div>`, `<p>`, etc.) tienen `height: auto;` por defecto. Esto significa que no es necesario especificarlo, pero es útil mencionarlo cuando se discuten otros estilos.\n\n- **Flexibilidad en Diseño**: Esta propiedad es perfecta para diseños responsivos, ya que permite que un elemento se expanda o contraiga automáticamente según sea necesario.\n\n### Ejemplo Práctico\n\nAquí tienes un ejemplo simple que demuestra cómo funciona `height: auto;`:\n\n```html\n<!DOCTYPE html>\n<html lang="es">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Ejemplo de height: auto;</title>\n    <style>\n        .contenedor {\n            width: 300px;                   /* Ancho del contenedor */\n            padding: 20px;                  /* Espaciado interno */\n            border: 2px solid #007BFF;      /* Borde azul */\n            background-color: #f0f8ff;      /* Fondo claro */\n            height: auto;                   /* Ajuste automático a contenido */\n       
 }\n    </style>\n</head>\n<body>\n\n<div class="contenedor">\n    <h2>Contenedor con altura automática</h2>\n    <p>Este es un ejemplo de cómo el contenedor se ajusta a la altura de su contenido.</p>\n    <p>Añadir más contenido aquí hará que el contenedor crezca automáticamente.</p>\n</div>\n\n</body>\n</html>\n```\n\n### Beneficios de `height: auto;`\n\n1. **Previene Desbordamientos**: Ayuda a evitar que el contenido se salga de los límites del contenedor.\n   \n2. **Ideal para Contenido Dinámico**: En aplicaciones web donde el contenido puede cambiar (como formularios o chats), la altura automática permite una mejor gestión del espacio.\n\n3. **Estética Mejorada**: Mantiene 
un diseño limpio y organizado al ajustar el tamaño del contenedor a lo que realmente necesita mostrar.\n\n### Conclusión\n\nUsar `height: auto;` es un enfoque común y recomendable para gestionar la altura de los elementos de manera dinámica. Si tienes alguna pregunta específica o necesitas más ejemplos relacionados con `height: auto;`, ¡déjamelo saber! Estoy aquí para ayudar.''', '29']

        print(message)
        return JsonResponse({'message': message})




#------------Chat------------




def openai_response(request , query):
    
    #query = base64.b64decode(query).decode('utf-8')
    
    client = OpenAI(
        
        api_key=config("OPENAI_API_KEY"),       
    )

    messages = request.session.get('messages', [])
    anchor = request.session.get('anchor_number', 0)
    anchor += 1
    
    if not messages:
        messages = [{'role' : 'system',
                'content': "Me llamo Luis y te estoy ayudando, debes de ser muy amable conmigo mientras te uso."
            }]

    messages.append({"role" : "user",
                "content": query,
                })

    chat_completion = client.chat.completions.create(
            messages = messages , model="gpt-4o-mini", )
    
    answer = chat_completion.choices[0].message.content
    
    messages.append({"role" : "assistant",
                "content": answer ,}
    )
    
    request.session['messages'] = messages
    request.session['anchor_number'] = anchor
    
    #answer = markdown.markdown(answer)

    return [answer , str(anchor)]
    

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

    
def gpt_entry(): # Lo usaré para crear una nueva instancia de Registry

    user = User.objects.get(username='')

    
    registry_entry = Registry(
        project_name="",
        log="",
        user=user
    )

    
    registry_entry.save()
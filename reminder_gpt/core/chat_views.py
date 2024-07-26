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
import markdown
import base64





#------------Chat------------



def chat(request):
    
    return render(request , "core/chat.html")


def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        message = openai_response(request , message_text)
        print(message)
        return JsonResponse({'message': message})
    return JsonResponse({'error': 'Invalid request'}, status=400)




#------------Chat------------




def openai_response(request , query):
    
    query = base64.b64decode(query).decode('utf-8')
    
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
    
    answer = markdown.markdown(answer)
    answer =  f'<a id=" {anchor}"></a>' + answer
    
    answer_link = f'<a href="# {anchor}">'
    
    return [answer , answer_link]
    

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
from django.shortcuts import render
from openai import OpenAI
from decouple import Config , config , Csv
from django.http import JsonResponse, HttpResponse
import ast
from pages.models import Registry
from django.contrib.auth.models import User




# Create your views here.



def openai_response(query):
    
    client = OpenAI(
        
        api_key=config("OPENAI_API_KEY"),       
    )


    messages = [{'role' : 'system',
                  'content': "Me llamo Luis y te estoy ayudando, debes de ser muy amable conmigo mientras te uso."
                }]


    messages.append({"role" : "user",
                "content": query,
                })

    chat_completion = client.chat.completions.create(
            messages = messages , model="gpt-4o-mini", )
  
    messages.append({"role" : "assistant",
                "content": chat_completion ,}
    )
    
    answer = chat_completion.choices[0].message.content
    print(chat_completion.choices[0])
    
    return answer
    

def test_openai(query= "Creación del registro de usuarios en el  proyecto web de la universidad"):

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

    
def gpt_entry(): # Lo usaré para crear una nueva intancia de Registry

    user = User.objects.get(username='')

    
    registry_entry = Registry(
        project_name="",
        log="",
        user=user
    )

    
    registry_entry.save()
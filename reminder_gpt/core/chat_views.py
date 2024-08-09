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
from django.shortcuts import render 
from django.http import JsonResponse
from django.shortcuts import render
from openai import OpenAI
from decouple import config
import logging
from django.contrib.auth.decorators import login_required

from decouple import config
import os
from langchain_community.utilities import SQLDatabase
#from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
#from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.agent_toolkits import create_sql_agent



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
    
    messages = request.session.get('messages', []) # Carga los mensajes de la sesión de este usuario si los hay. La sesión expira al cerrar la página o hcaer logout
    anchor = request.session.get('anchor_number', 0)
    anchor += 1
        
    try:
    
        client = OpenAI(
            
            api_key=config("OPENAI_API_KEY"),       
        )

        messages.append({"role" : "user",
                    "content": query,
                    })

        chat_completion = client.chat.completions.create(       # Crea la respuesta en función a los messages, basándose en el modelo indicado (gpt-4o-mini)
                messages = messages , model="gpt-4o-mini", )
        
        if query[0:2] != "**":
            answer = chat_completion.choices[0].message.content  #Devuelve el contenido
        
        else:
            answer = agent(query)
        #answer = agent(query)
        
        messages.append({"role" : "assistant",
                    "content": answer ,}
        )
        
        request.session['messages'] = messages
        request.session['anchor_number'] = anchor

        return [answer , str(anchor)]
    
    except:
        return ["Algo ha salido mal [Consulta General]" , str(0)]
        


def agent(query): # Con el agente funciona.
    """
    Esta función utiliza un agente de LangChain para realizar consultas en lenguaje natural a una base de datos SQL.

    Parámetros:
    query (str): La consulta en lenguaje natural que el usuario desea realizar a la base de datos.

    Retorno:
    str: La respuesta a la consulta realizada en lenguaje natural, obtenida de la base de datos SQL.

    Descripción:
    1. Establece la clave de la API de OpenAI desde las variables de entorno.
    2. Crea una conexión a la base de datos SQL 'ecommerce.db'.
    3. Inicializa un modelo de lenguaje GPT-4 de OpenAI con ciertos parámetros.
    4. Configura un agente ejecutor para interactuar con la base de datos utilizando herramientas de OpenAI.
    5. Ejecuta la consulta proporcionada en lenguaje natural y devuelve la respuesta.

    Dependencias:
    - os
    - config
    - langchain
    - langchain.sql_database.SQLDatabase
    - langchain.agents.create_sql_agent
    - langchain.llms.openai.ChatOpenAI

    Ejemplo de uso:
    ```python
    respuesta = agent("¿Cuál es el producto más vendido en 2023?")
    print(respuesta)
    ```

    """
    
    os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

    db = SQLDatabase.from_uri("sqlite:///ecommerce_ok.db")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

    response = agent_executor.invoke(
        {
            "input": f"{query}. Asegurate si te pido una fecha  que realices la consulta con el siguiente formato 12/1/2010 8:26 y debes contestarme siempre en español "
        }
    )
    
    return response['output']

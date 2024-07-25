

from django.shortcuts import render
from django.http import JsonResponse
from chatgpt.views_copy import openai_response
#from .models import Message



def chat(request):
    
    return render(request , "chat/chat.html")


def send_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        message = openai_response(request , message_text)
        print(message)
        return JsonResponse({'message': message})
    return JsonResponse({'error': 'Invalid request'}, status=400)


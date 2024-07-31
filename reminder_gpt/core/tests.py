from django.test import TestCase, Client, RequestFactory
from . import views 
from . chat_views import openai_response
from . forms import SignUpForm , LoginForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login
from unittest.mock import patch, MagicMock

# Create your tests here.



#forms.py


class SignUpFormTest(TestCase):

    def test_valid_form(self):
        
        form_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'tlf': '123456789',
        }
        
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_invalid_tlf_non_digit(self):
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'tlf': '12345abcd',
        }
        
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tlf', form.errors)
        self.assertEqual(form.errors['tlf'], ["El tlf debe contener solo números."])


    def test_invalid_tlf_length(self):
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'tlf': '12345678',  # Only 8 digits
        }
        
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tlf', form.errors)
        self.assertEqual(form.errors['tlf'], ["El tlf debe tener exactamente 9 dígitos."])


    def test_passwords(self):
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpassword123',
            'password2': 'differentpassword123',
            'tlf': '123456789',
        }
        
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ["The two password fields didn’t match."])



class LoginFormTest(TestCase):

    def test_valid_form(self):
        
        form_data = {
            'user': 'testuser',
            'password': 'complexpassword123',
        }
        
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_user(self):

        form_data = {
            'user': '',
            'password': 'complexpassword123',
        }

        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user', form.errors)
        self.assertEqual(form.errors['user'], ["This field is required."])


    def test_password(self):

        form_data = {
            'user': 'testuser',
            'password': '',
        }

        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertEqual(form.errors['password'], ["This field is required."])



# views.py




class HomeViewTest(TestCase):

    def setUp(self):
        
        self.client = Client()
        self.url = reverse('home')


    def test_login_form_renders(self):
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertIsInstance(response.context['form'], LoginForm)


    def test_login_true(self):
        
        User.objects.create_user(username='testuser', password='testpassword123')
        response = self.client.post(self.url, {
            'user': 'testuser',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirige a 'chat'
        self.assertRedirects(response, reverse('chat'))
        self.assertTrue('_auth_user_id' in self.client.session)



    def test_login_false(self):
        
        response = self.client.post(self.url, {
            'user': 'wronguser',
            'password': 'wrongpassword'
        })

        self.assertTemplateUsed(response, 'core/index.html')
        form = response.context.get('form')
        
        self.assertIsNotNone(form, "El formulario no está en el contexto de la respuesta")
        self.assertFalse(form.is_valid(), "El formulario debería ser inválido")

        # Asegúrate de que el mensaje de error coincida
        non_field_errors = form.non_field_errors()
        
        self.assertIn('Usuario o contraseña incorrectos', non_field_errors, 
                    "El mensaje de error no es el esperado en los errores no relacionados con campos específicos")




#chat_views.py



class ChatViewTest(TestCase):
    
    def setUp(self):
        
        self.client = Client()
        self.url = reverse('chat')  # Asegúrate de que 'chat' es el nombre correcto de la URL


    def test_chat_view(self):
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/chat.html')
        
        
        

class SendMessageViewTest(TestCase):
    
    def setUp(self):
        
        self.client = Client()
        self.url = reverse('send_message')  


    @patch('core.chat_views.openai_response')  
    def test_send_message_success(self, mock_openai_response):
        
        mock_openai_response.return_value = ['Test response', '1']

        response = self.client.post(self.url, {'message': 'Hello'})
        
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': ['Test response', '1']})


    def test_send_message_invalid_request(self):
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid request'})
    
    
    @patch('core.chat_views.openai_response')  
    def test_send_message_exception(self, mock_openai_response):
        
        url = reverse('send_message')  
        response = self.client.post(url, {'message': 'test'})
        
        self.assertEqual(response.status_code, 500)
        
        self.assertEqual(response.content.decode(), "Ha habido un problema al envíar el mensaje")  # Verifica que el contenido de la respuesta sea el esperado



class OpenAIResponseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    @patch('core.chat_views.openai_response')
    def test_openai_response_success(self, MockOpenAI):
        # Configura el mock para simular una respuesta exitosa del cliente OpenAI
        mock_client = MockOpenAI.return_value
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock(message=MagicMock(content='Test response'))]
        mock_client.chat.completions.create.return_value = mock_chat_completion

        # Llama a la función
        response = self.client.post('/fake-url/', {'message': 'test query'})

        # Verifica que la respuesta es correcta
        self.assertEqual(response.json()['message'][0], 'Test response')
        self.assertEqual(response.json()['message'][1], '1')  # Suponiendo que el `anchor_number` es 1 después de la primera llamada

    @patch('core.chat_views.openai_response')
    def test_openai_response_exception(self, MockOpenAI):
        # Configura el mock para lanzar una excepción
        MockOpenAI.side_effect = Exception("Test exception")

        # Llama a la función
        response = self.client.post('/fake-url/', {'message': 'test query'})

        # Verifica que la función maneja la excepción correctamente
        self.assertEqual(response.status_code, 500)
        self.assertIn('Ha habido un problema al envíar el mensaje', response.content.decode())

    @patch('core.chat_views.openai_response')
    def test_openai_response_user_luis(self, MockOpenAI):
        # Cambia el usuario a "Luis"
        self.user.username = 'Luis'
        self.user.save()

        # Configura el mock para simular una respuesta exitosa del cliente OpenAI
        mock_client = MockOpenAI.return_value
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock(message=MagicMock(content='Test response'))]
        mock_client.chat.completions.create.return_value = mock_chat_completion

        # Llama a la función
        response = self.client.post('/fake-url/', {'message': 'test query'})

        # Verifica que la respuesta es correcta y el mensaje de sistema para Luis está presente
        self.assertEqual(response.json()['message'][0], 'Test response')
        self.assertEqual(response.json()['message'][1], '1')

        # Verifica el contenido de la sesión
        # No podemos verificar directamente el contenido de la sesión, pero podemos verificar el estado
        session = self.client.session
        session.save()  # Guardar la sesión para que sea persistente

    @patch('core.chat_views.openai_response')
    def test_openai_response_session_management(self, MockOpenAI):
        # Configura el mock para simular una respuesta exitosa del cliente OpenAI
        mock_client = MockOpenAI.return_value
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock(message=MagicMock(content='Test response'))]
        mock_client.chat.completions.create.return_value = mock_chat_completion

        # Llama a la función
        response = self.client.post('/fake-url/', {'message': 'test query'})

        # Verifica el estado de la sesión
        session = self.client.session
        session.save()  # Guardar la sesión para que sea persistente
        messages = session.get('messages', [])
        self.assertTrue(len(messages) > 0)  # Verifica que se añadieron mensajes
        self.assertEqual(session.get('anchor_number', 0), 1)

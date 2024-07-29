function base64Encode(str) {
    return btoa(encodeURIComponent(str));
}

// Se ejecuta cuando el formulario se envía
$('#chat-form').on('submit', function(event) {
    event.preventDefault(); // Evita el envío normal del formulario y recarga de la página

    let message = $('#message-input').val(); // Obtiene el valor del campo de entrada de mensaje

    const chatBox = $('#chat-box');
    const chatLink = $('#chat-link');

    const userMessageElement = $('<div class="user"></div>').text(message);   // Esto es lo agregado
    userMessageElement.html(userMessageElement.html().replace(/\n/g, '<br>'));   // Esto es lo agregado
    chatBox.append(userMessageElement);   // Esto es lo agregado
   // chatBox.append('<div class="user"></div>').find('.user:last').text(message);
    
    $('#message-input').val('');

    chatBox.scrollTop(chatBox[0].scrollHeight);

    // Codifica el mensaje en Base64 antes de enviarlo
    let to_truncate = message;
    let encodedMessage = base64Encode(message);

    $.ajax({
        url: '/sended/', // URL a la que se envía la solicitud AJAX
        method: 'POST', // Método HTTP para la solicitud
        data: {
            'message': encodedMessage, // Datos a enviar en la solicitud (el mensaje del usuario en Base64)
            'csrfmiddlewaretoken': '{{ csrf_token }}' // Token CSRF para seguridad
        },
        success: function(response) {
            const maxLength = 30;

            // Trunca el mensaje original y añade '...' al final si es necesario
            let truncatedMessage = to_truncate.length > maxLength
                ? to_truncate.substring(0, maxLength) + '...'
                : to_truncate;
            chatBox.append('<div class="bot">' + response.message[0] + '</div>');
            chatLink.append('<div class="aside_link">' + response.message[1] + truncatedMessage + '</a></div>');

            // Desplaza el contenedor de mensajes al final para que el nuevo mensaje sea visible
            chatBox.scrollTop(chatBox[0].scrollHeight);
            // Limpia el campo de entrada de mensaje
        },
        error: function(xhr, status, error) {
            console.error('Error:', error); // Muestra cualquier error en la consola del navegador
        }
    });
});
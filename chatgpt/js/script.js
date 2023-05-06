document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const messagesContainer = document.querySelector('.messages');

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (!userMessage) {
            return;
        }

        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user-message');
        userMessageElement.textContent = `Usuario: ${userMessage}`;
        messagesContainer.appendChild(userMessageElement);

        userInput.value = '';

        // Simulación de respuesta de ChatGPT
        setTimeout(() => {
            const chatGPTResponse = 'Este es un ejemplo de respuesta de ChatGPT.';
            const chatGPTMessageElement = document.createElement('div');
            chatGPTMessageElement.classList.add('chatgpt-message');
            chatGPTMessageElement.textContent = `ChatGPT: ${chatGPTResponse}`;
            messagesContainer.appendChild(chatGPTMessageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 1000);

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});

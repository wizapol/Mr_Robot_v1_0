// scripts.js

document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const messages = document.querySelector(".messages");

    chatForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Añadir el mensaje del usuario al chat
        const userMessage = document.createElement("div");
        userMessage.textContent = `Usuario: ${message}`;
        messages.appendChild(userMessage);

        userInput.value = "";

        // Enviar el mensaje al servidor y recibir la respuesta del modelo
        fetch("/chat/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        })
            .then((response) => response.json())
            .then((data) => {
                const botMessage = document.createElement("div");
                botMessage.textContent = `MR_Robot: ${data.response}`;
                messages.appendChild(botMessage);
            })
            .catch((error) => {
                console.error("Error:", error);
                const errorMessage = document.createElement("div");
                errorMessage.textContent = "MR_Robot: Lo siento, ha ocurrido un error.";
                messages.appendChild(errorMessage);
            });
    });
});

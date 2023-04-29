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
    userMessage.classList.add("chat-bubble", "user");
    userMessage.textContent = `Usuario: ${message}`;
    messages.appendChild(userMessage);

    userInput.value = "";

    // Enviar el mensaje al servidor y recibir la respuesta del modelo usando AJAX
    $.ajax({
      type: "POST",
      url: "/chat/message",
      data: JSON.stringify({ message }),
      contentType: "application/json",
      dataType: "json",
      success: (data) => {
        const botMessage = document.createElement("div");
        botMessage.classList.add("chat-bubble");
        botMessage.textContent = `MR_Robot: ${data.message}`;
        messages.appendChild(botMessage);
      },
      error: (error) => {
        console.error("Error:", error);
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("chat-bubble");
        errorMessage.textContent = "MR_Robot: Lo siento, ha ocurrido un error.";
        messages.appendChild(errorMessage);
      },
    });
  });

  // Agregar controladores de eventos para los botones de borrar memoria
  document.getElementById("delete-short-term-memory").addEventListener("click", () => {
    $.ajax({
      type: "POST",
      url: "/chat/delete_short_term_memory",
      success: function (response) {
        console.log(response);
        alert(response.message);
      },
      error: function (error) {
        console.error(error);
      },
    });
  });

  document.getElementById("delete-long-term-memory").addEventListener("click", () => {
    $.ajax({
      type: "POST",
      url: "/chat/delete_long_term_memory",
      success: function (response) {
        console.log(response);
        alert(response.message);
      },
      error: function (error) {
        console.error(error);
      },
    });
  });

  document.getElementById("delete-all-memory").addEventListener("click", () => {
    $.ajax({
      type: "POST",
      url: "/chat/delete_all_memory",
      success: function (response) {
        console.log(response);
        alert(response.message);
      },
      error: function (error) {
        console.error(error);
      },
    });
  });
});

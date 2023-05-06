import { createCodeSnippet } from "./codeSnippet.js";
import { saveMessageToLocalStorage, loadMessagesFromLocalStorage, clearLocalStorage } from "./localStorage.js";

export function addMessageToChat(content, type) {
  const message = document.createElement("div");
  message.classList.add("chat-bubble", type);

  const regex = /```(\w*)\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(content)) !== null) {
    const codeSnippet = content.slice(lastIndex, match.index).trim();
    const codeElement = createCodeSnippet(match[1], match[2].trim());
    message.appendChild(document.createTextNode(codeSnippet));
    message.appendChild(codeElement);
    lastIndex = regex.lastIndex;
  }

  const remainingText = content.slice(lastIndex).trim();
  if (remainingText) {
    message.appendChild(document.createTextNode(remainingText));
  }

  const messages = document.querySelector(".messages");
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
  saveMessageToLocalStorage(content, type);
}

document.addEventListener("DOMContentLoaded", () => {
  loadMessagesFromLocalStorage();
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Añadir el mensaje del usuario al chat
    addMessageToChat(`Usuario: ${message}`, "user");

    userInput.value = "";

    // Enviar el mensaje al servidor y recibir la respuesta del modelo usando AJAX
    $.ajax({
      type: "POST",
      url: "/chat/message",
      data: JSON.stringify({ message }),
      contentType: "application/json",
      dataType: "json",
      success: (data) => {
        addMessageToChat(`MR_Robot: ${data.message}`, "assistant");
      },
      error: (error) => {
        console.error("Error:", error);
        addMessageToChat("MR_Robot: Error, cant reach app server.", "assistant");
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
    clearChat();
    clearLocalStorage();
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

function clearChat() {
  const messages = document.querySelector(".messages");
  messages.innerHTML = "";
}
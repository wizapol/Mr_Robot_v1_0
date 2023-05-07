// chat.js
import { createCodeSnippet } from "./codeSnippet.js";
import { saveMessageToLocalStorage, loadMessagesFromLocalStorage } from "./localStorage.js";
import { initializeEditControls } from "./editControls.js";
import { initializeMemoryControls } from "./memoryControls.js";

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

async function sendMessage(message) {
  try {
    const response = await fetch("/chat/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Error:", error);
    return "MR_Robot: Error, cant reach app server.";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadMessagesFromLocalStorage();
  initializeEditControls();
  initializeMemoryControls();
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Añadir el mensaje del usuario al chat
    addMessageToChat(`Usuario: ${message}`, "user");

    userInput.value = "";

    // Enviar el mensaje al servidor y recibir la respuesta del modelo usando fetch y async/await
    const responseMessage = await sendMessage(message);
    addMessageToChat(`MR_Robot: ${responseMessage}`, "assistant");
  });
});

export function clearChat() {
  const messages = document.querySelector(".messages");
  messages.innerHTML = "";
}

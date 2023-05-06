// scripts.js

function createCodeSnippet(language, code) {
    const codeCard = document.createElement("div");
    codeCard.classList.add("code-card");
  
    const codeHeader = document.createElement("div");
    codeHeader.classList.add("code-header");
  
    const codeLanguage = document.createElement("span");
    codeLanguage.innerText = language;
  
    const copyButton = document.createElement("button");
    copyButton.classList.add("copy-code-button");
    copyButton.innerText = "Copiar";
    copyButton.onclick = function () {
      copyTextToClipboard(code);
    };
  
    codeHeader.appendChild(codeLanguage);
    codeHeader.appendChild(copyButton);
    codeCard.appendChild(codeHeader);
  
    const codeSnippet = document.createElement("pre");
    const codeElement = document.createElement("code");
    codeElement.classList.add("code");
    codeElement.textContent = code;
    codeSnippet.appendChild(codeElement);
    codeCard.appendChild(codeSnippet);
  
    return codeCard;
  }
  
  
function addMessageToChat(content, type) {
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
        addMessageToChat("MR_Robot: Lo siento, ha ocurrido un error.", "assistant");
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

function copyTextToClipboard(text) {
const textArea = document.createElement("textarea");
textArea.value = text;
document.body.appendChild(textArea);
textArea.focus();
textArea.select();
try {
    const successful = document.execCommand("copy");
    const msg = successful ? "successful" : "unsuccessful";
    console.log("Copying text command was " + msg);
} catch (err) {
    console.error("Oops, unable to copy", err);
    document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed"; // Evita que se desplace la página al añadir el textarea
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand("copy");
    } catch (err) {
        console.error("No se pudo copiar el texto al portapapeles", err);
    }
    
    document.body.removeChild(textArea);
    }
}
function saveMessageToLocalStorage(content, type) {
  const storedMessages = JSON.parse(localStorage.getItem("chatMessages") || "[]");
  storedMessages.push({ content, type });
  localStorage.setItem("chatMessages", JSON.stringify(storedMessages));
}

function loadMessagesFromLocalStorage() {
  const storedMessages = JSON.parse(localStorage.getItem("chatMessages") || "[]");
  storedMessages.forEach((message) => {
    addMessageToChat(message.content, message.type);
  });
}
function clearChat() {
    const messages = document.querySelector(".messages");
    messages.innerHTML = "";
  }
  
    
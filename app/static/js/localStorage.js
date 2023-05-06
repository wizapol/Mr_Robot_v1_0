import { addMessageToChat } from "./chat.js";

export function saveMessageToLocalStorage(content, type) {
    const storedMessages = JSON.parse(localStorage.getItem("chatMessages") || "[]");
    storedMessages.push({ content, type });
    localStorage.setItem("chatMessages", JSON.stringify(storedMessages));
  }
  
  export function loadMessagesFromLocalStorage() {
    const storedMessages = JSON.parse(localStorage.getItem("chatMessages") || "[]");
    storedMessages.forEach((message) => {
      addMessageToChat(message.content, message.type);
    });
  }
  
  export function clearLocalStorage() {
    localStorage.removeItem("chatMessages");
  }
  
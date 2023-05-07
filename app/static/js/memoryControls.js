// memoryControls.js
import { clearChat } from "./chat.js";
import { clearLocalStorage } from "./localStorage.js";

export function initializeMemoryControls() {
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
}

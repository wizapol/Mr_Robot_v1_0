export function initializeEditControls() {
    document.addEventListener("click", (e) => {
      const target = e.target;
  
      if (target.classList.contains("edit-btn")) {
        enableEditMode(target);
      } else if (target.classList.contains("save-btn")) {
        saveChanges(target);
      } else if (target.classList.contains("cancel-btn")) {
        cancelChanges(target);
      } else if (target.classList.contains("regenerate-btn")) {
        regenerateResponse(target);
      }
    });
  }
  
  function enableEditMode(target) {
    const messageBubble = target.parentElement;
    const messageText = messageBubble.querySelector(".message-text");
    const textarea = document.createElement("textarea");
  
    textarea.classList.add("edit-textarea");
    textarea.value = messageText.textContent.trim();
    messageText.style.display = "none";
    messageBubble.insertBefore(textarea, target);
    target.style.display = "none";
  
    const saveBtn = document.createElement("button");
    saveBtn.classList.add("save-btn");
    saveBtn.textContent = "Guardar";
    messageBubble.insertBefore(saveBtn, target);
  
    const cancelBtn = document.createElement("button");
    cancelBtn.classList.add("cancel-btn");
    cancelBtn.textContent = "Cancelar";
    messageBubble.insertBefore(cancelBtn, target);
  
    const regenerateBtn = document.createElement("button");
    regenerateBtn.classList.add("regenerate-btn");
    regenerateBtn.textContent = "Regenerar respuesta";
    messageBubble.insertBefore(regenerateBtn, target);
  }
  
  function saveChanges(target) {
    const messageBubble = target.parentElement;
    const messageText = messageBubble.querySelector(".message-text");
    const textarea = messageBubble.querySelector(".edit-textarea");
  
    messageText.textContent = textarea.value.trim();
    messageText.style.display = "block";
    textarea.remove();
    target.remove();
  
    const cancelBtn = messageBubble.querySelector(".cancel-btn");
    cancelBtn.remove();
  
    const regenerateBtn = messageBubble.querySelector(".regenerate-btn");
    regenerateBtn.remove();
  
    const editBtn = messageBubble.querySelector(".edit-btn");
    editBtn.style.display = "block";
  }
  
  function cancelChanges(target) {
    const messageBubble = target.parentElement;
    const messageText = messageBubble.querySelector(".message-text");
    const textarea = messageBubble.querySelector(".edit-textarea");
  
    messageText.style.display = "block";
    textarea.remove();
    target.remove();
  
    const saveBtn = messageBubble.querySelector(".save-btn");
    saveBtn.remove();
  
    const regenerateBtn = messageBubble.querySelector(".regenerate-btn");
    regenerateBtn.remove();
  
    const editBtn = messageBubble.querySelector(".edit-btn");
    editBtn.style.display = "block";
  }
  
  function regenerateResponse(target) {
    const messageBubble = target.parentElement;
    const messageText = messageBubble.querySelector(".message-text");
    const textarea = messageBubble.querySelector(".edit-textarea");
  
    // Realizar una llamada AJAX para obtener una nueva respuesta
    $.ajax({
      type: "POST",
      url: "/chat/regenerate",
      data: JSON.stringify({ message: textarea.value.trim() }),
      contentType: "application/json",
      dataType: "json",
      success: (data) => {
        messageText.textContent = data.message;
        messageText.style.display = "block";
        textarea.remove();
        target.remove();
  
        const saveBtn = messageBubble.querySelector(".save-btn");
        saveBtn.remove();
  
        const cancelBtn = messageBubble.querySelector(".cancel-btn");
        cancelBtn.remove();
  
        const editBtn = messageBubble.querySelector(".edit-btn");
        editBtn.style.display = "block";
      },
      error: (error) => {
        console.error("Error:", error);
        alert("No se pudo regenerar la respuesta. Inténtalo de nuevo más tarde.");
      },
    });
  }
    
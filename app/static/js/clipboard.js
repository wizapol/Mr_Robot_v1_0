export function copyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
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
  
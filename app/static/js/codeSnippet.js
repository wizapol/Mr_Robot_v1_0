import { copyTextToClipboard } from "./clipboard.js";

export function createCodeSnippet(language, code) {
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
  
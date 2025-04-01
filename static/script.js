function toggleChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
    loadChatHistory();
}

function generateResponse() {
    const prompt = document.getElementById("prompt").value;
    if (!prompt) return;

    appendMessage("user", prompt);
    document.getElementById("prompt").value = "";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            appendMessage("ai", data.response);
            saveChatHistory();
        } else {
            appendMessage("ai", `<strong>Error:</strong> ${data.error}`);
        }
    })
    .catch(() => {
        appendMessage("ai", `<strong>Error:</strong> Failed to get response.`);
    });
}

function appendMessage(sender, message) {
    const chatMessages = document.getElementById("chat-messages");
    const msgElement = document.createElement("div");

    msgElement.classList.add(sender === "user" ? "sent" : "received");
    msgElement.innerHTML = formatText(message);

    chatMessages.appendChild(msgElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatText(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Bold text
    text = text.replace(/```([\s\S]*?)```/g, function(match, code) {
        return "<pre>" + escapeHtml(code) + "</pre>";
    }); // Code block
    text = text.replace(/\n/g, "<br>"); // New lines for AI responses
    return text;
}

function escapeHtml(unsafe) {
    return unsafe.replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function saveChatHistory() {
    const chatMessages = document.getElementById("chat-messages").innerHTML;
    localStorage.setItem("chatHistory", chatMessages);
}

function loadChatHistory() {
    const chatHistory = localStorage.getItem("chatHistory");
    if (chatHistory) {
        document.getElementById("chat-messages").innerHTML = chatHistory;
    }
}

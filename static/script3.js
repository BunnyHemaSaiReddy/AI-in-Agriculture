document.addEventListener("DOMContentLoaded", function () {
    loadMessages(); // Load messages when the page loads
    setInterval(loadMessages, 2000); // Refresh chat every 2 seconds
});

// Toggle the universal chat visibility
function toggleUniversalChat() {
    let chatBox = document.getElementById("universal-chat");
    chatBox.style.display = (chatBox.style.display === "none" || chatBox.style.display === "") ? "block" : "none";
}

// Load previous messages from the server
function loadMessages() {
    fetch("/get_messages")
        .then(response => response.json())
        .then(messages => {
            let chatBox = document.getElementById("universal-chat-messages");
            chatBox.innerHTML = ""; // Clear previous messages

            if (messages.length === 0) {
                chatBox.innerHTML = "<p style='color:gray; text-align:center;'>No messages yet.</p>";
                return;
            }

            messages.forEach(msg => {
                let userEmail = msg.user_email || "Unknown"; // Handle undefined user_email
                let messageText = msg.message || "No message"; // Handle undefined message

                // Remove @gmail.com from email
                userEmail = userEmail.replace(/@gmail.com$/, "");

                // Determine message alignment and color
                let isUserMessage = msg.is_user_message || false; // Assuming the server sends this info to identify the user
                let messageClass = isUserMessage ? "user-message" : "other-message";
                let backgroundColor = isUserMessage ? "#d1e7ff" : "#f1f1f1"; // Light blue for user messages, light gray for others

                let msgElement = document.createElement("div");
                msgElement.classList.add("message", messageClass);
                msgElement.style.backgroundColor = backgroundColor;

                msgElement.innerHTML = `
                    <strong>${userEmail}:</strong> ${messageText}
                `;
                chatBox.appendChild(msgElement);
            });

            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
        })
        .catch(error => {
            console.error("Error fetching messages:", error);
            let chatBox = document.getElementById("universal-chat-messages");
            chatBox.innerHTML = "<p style='color:red; text-align:center;'>Unable to load messages.</p>";
        });
}

// Send a new message
function sendMessage() {
    let messageInput = document.getElementById("chat-input");
    let message = messageInput.value.trim();

    if (message !== "") {
        fetch("/send_message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageInput.value = ""; // Clear input field after sending
                loadMessages(); // Refresh chat after sending a message
            } else {
                alert("Failed to send message. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error sending message:", error);
            alert("An error occurred while sending the message.");
        });
    } else {
        alert("Message cannot be empty.");
    }
}

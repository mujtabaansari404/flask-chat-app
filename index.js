let username;

document.addEventListener("DOMContentLoaded", () => {
    const socket = io();
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message");
    const sound = new Audio("/static/sound/msgpop.wav");
    username = prompt("Enter your username:");
    if (!username || username.trim() === "") {
        username = "Unknown";
    }

    socket.emit("user_joined", username);

    socket.on("message", (msg) => {
        const msgDiv = document.createElement("div");
        msgDiv.textContent = msg;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        sound.play()
    });

    socket.on("user_joined", (user) => {
        const msgDiv = document.createElement("div");
        msgDiv.style.fontStyle = "italic";
        msgDiv.textContent = `${user} joined the chat.`;
        chatBox.appendChild(msgDiv);
    });

    window.sendMessage = function () {
        const message = messageInput.value.trim();
        if (message) {
            socket.send(`${username}: ${message}`);
            messageInput.value = "";
        }
    };

    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

// Wait for the page to finish loading
document.addEventListener("DOMContentLoaded", () => {
  // Grab DOM elements
  const chatForm = document.getElementById("chat-form");
  const messagesBox = document.getElementById("chat-messages");
  const userText = document.getElementById("user-text");
  const modeSelect = document.getElementById("chat-type");
  const imageInput = document.getElementById("user-images");

  // Handle form submit
  chatForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent page reload

    const message = userText.value.trim();
    const mode = modeSelect.value;
    const files = imageInput.files;

    if (!message) {
      console.warn("No message entered");
      return;
    }

    // Show user message
    const userMessage = document.createElement("div");
    userMessage.className = "message-box you";
    userMessage.innerHTML = `<strong>You:</strong> ${message}`;
    messagesBox.appendChild(userMessage);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    userText.value = "";

    // Build form data for backend
    const formData = new FormData();
    formData.append("message", message);
    formData.append("mode", mode);
    for (let i = 0; i < Math.min(files.length, 10); i++) {
      formData.append("images", files[i]);
    }

    // 🔵 Show typing animation
    const typingMsg = document.createElement("div");
    typingMsg.id = "typing";
    typingMsg.className = "message-box bot";
    typingMsg.innerHTML = `<em>Plumber Bot is typing<span class="dot-one">.</span><span class="dot-two">.</span><span class="dot-three">.</span></em>`;
    messagesBox.appendChild(typingMsg);
    messagesBox.scrollTop = messagesBox.scrollHeight;

    try {
      // Send data to the backend
      const res = await fetch("http://localhost:8000/chat/upload", {
        method: "POST",
        body: formData,
      });

      // Remove typing indicator once response comes in
      const typing = document.getElementById("typing");
      if (typing) typing.remove();

      const data = await res.json();
      console.log("Response from backend:", data);

      // Show assistant reply
      const botMessage = document.createElement("div");
      botMessage.className = "message-box bot";
      botMessage.innerHTML = `<strong>Plumber Bot:</strong> ${data.response}`;
      messagesBox.appendChild(botMessage);
      messagesBox.scrollTop = messagesBox.scrollHeight;

    } catch (error) {
      // Remove typing if there's an error
      const typing = document.getElementById("typing");
      if (typing) typing.remove();

      console.error("Error:", error);
      const errorMessage = document.createElement("div");
      errorMessage.className = "message-box error";
      errorMessage.innerHTML = `<strong>Error:</strong> Couldn't reach the server.`;
      messagesBox.appendChild(errorMessage);
    }
  });
});

// When the page is ready...
document.addEventListener("DOMContentLoaded", () => {
  // Grab the form and message display area
  const chatForm = document.getElementById("chat-form");
  const messagesBox = document.getElementById("messages");
  const userText = document.getElementById("user-text");

  // Handle form submission (when user clicks "Send")
  chatForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // stop the page from refreshing

    const message = userText.value.trim(); // get the message text
    const mode = document.getElementById("chat-type").value; // get which mode (general, sms, mentor)
    const files = document.getElementById("user-images").files; // get uploaded files

    if (!message) {
      console.warn("No message entered");
      return;
    }

    // Add the user's message to the chat visually
    const userMessage = document.createElement("div");
    userMessage.className = "message-box you";
    userMessage.innerHTML = `<strong>You:</strong> ${message}`;
    messagesBox.appendChild(userMessage);
    messagesBox.scrollTop = messagesBox.scrollHeight; // scroll to bottom
    userText.value = ""; // clear the text box

    // Build the data we're sending (text + mode + files)
    const formData = new FormData();
    formData.append("message", message);
    formData.append("mode", mode);

    for (let i = 0; i < Math.min(files.length, 10); i++) {
      formData.append("images", files[i]); // attach up to 10 images
    }

    try {
      // Send the form to our backend (FastAPI)
      const res = await fetch("http://localhost:8000/chat/upload", {
        method: "POST",
        body: formData,
      });

      // Convert the response to JSON
      const data = await res.json();
      console.log("Response from backend:", data);

      // Add the assistant's response to the chat visually
      const botMessage = document.createElement("div");
      botMessage.className = "message-box bot";
      botMessage.innerHTML = `<strong>Plumber Bot:</strong> ${data.response}`;
      messagesBox.appendChild(botMessage);
      messagesBox.scrollTop = messagesBox.scrollHeight; // scroll to bottom

    } catch (error) {
      // Show an error in the chat if something breaks
      console.error("Error:", error);
      const errorMessage = document.createElement("div");
      errorMessage.className = "message-box error";
      errorMessage.innerHTML = `<strong>Error:</strong> Couldn't reach the server.`;
      messagesBox.appendChild(errorMessage);
    }
  });
});

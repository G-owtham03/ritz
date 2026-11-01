async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    
    chatBox.innerHTML += `<div class="message user">${message}</div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingId = 'loading-' + Date.now();
    chatBox.innerHTML += `<div class="message ai" id="${loadingId}">Typing...</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        document.getElementById(loadingId).innerText = data.reply;
    } catch (error) {
        document.getElementById(loadingId).innerText = "Oops, the server choked on a shawarma. Try again.";
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});
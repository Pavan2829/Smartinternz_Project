async function sendMessage() {
    const input = document.getElementById('user-input');
    const window = document.getElementById('chat-window');
    const text = input.value;
    if(!text) return;

    window.innerHTML += `<div class="msg user"><b>You:</b> ${text}</div>`;
    input.value = '';

    try {
        const res = await fetch('http://127.0.0.1:8000/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question: text})
        });
        const data = await res.json();
        window.innerHTML += `<div class="msg bot"><b>Smartinternz_Project:</b> ${data.answer}</div>`;
    } catch (e) {
        window.innerHTML += `<div class="msg bot" style="color:red;">Error: Server not running</div>`;
    }
    window.scrollTop = window.scrollHeight;
}

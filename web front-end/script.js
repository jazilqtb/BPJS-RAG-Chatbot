const nameInput = document.getElementById('name-input');
const chatInput = document.getElementById('chat-input');
const sendButton = document.querySelector('button');
const responseBox = document.getElementById('response-box');

sendButton.addEventListener('click', async function(){
    const nameValue = nameInput.value;
    const queryValue = chatInput.value;

    if (!nameValue||!queryValue){
        alert("Nama dan Pertanyaan Wajib diisi.");
        return;
    }

    // Berikan feedback visual bahwa proses sedang berjalan
    responseBox.innerText = "Halo "+nameValue+", server sedang berpikir, tunggu sebentar ya...";
    sendButton.disabled = true;

    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: nameValue,
                query: queryValue
            })
        });

        const data = await response.json();

        if (response.ok){
            responseBox.innerText = data.answer;
        }else{
            responseBox.innerText = "Error dari Server: "+ JSON.stringify(data.detail);
        }
    } catch(error){
        responseBox.innerText = "Gagal terhubung ke Backend, Pastikan Uvicorn sudah jalan.";
        console.error("Network Error:", error);
    } finally{
        sendButton.disabled = false;
    }
});

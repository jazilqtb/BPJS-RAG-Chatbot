// Inisialisasi: Memegang elemen "Hardware" (DOM Selection)
const nameInput = document.getElementById('name-input');
const chatInput = document.getElementById('chat-input');
const sendButton = document.querySelector('button'); //mengambil tombol pertama
const responseBox = document.getElementById('response-box');

// Event Listener: Menunggu "Interupsi" (Input dari User)
sendButton.addEventListener('click', async function(){
    // Data Acquisition: Mengambil nilai saat ini
    const nameValue = nameInput.value;
    const queryValue = chatInput.value;

    if (!nameValue||!queryValue){
        alert("Nama dan Pertanyaan Wajib diisi.");
        return;
    }

    // Berikan feedback visual bahwa proses sedang berjalan
    responseBox.innerText = "Halo "+nameValue+", server sedang berpikir, tunggu sebentar ya...";
    sendButton.disabled = true; // Matikan sementara tombol agar tidak diklik berkali-kali

    try {
        // THE BRIDGE: Mengirim data ke FastAPI
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

        // Menangani response
        const data = await response.json();

        if (response.ok){
            // Jika sukses (Status 200), Tampilkan jawaban dari Backend
            responseBox.innerText = data.answer;
        }else{
            responseBox.innerText = "Error dari Server: "+ JSON.stringify(data.detail);
        }
    } catch(error){
        // Jika server mati atau masalah koneksi jaringan
        responseBox.innerText = "Gagal terhubung ke Backend, Pastikan Uvicorn sudah jalan.";
        console.error("Network Error:", error);
    } finally{
        // Aktifkan kembali tombol
        sendButton.disabled = false;
    }
});

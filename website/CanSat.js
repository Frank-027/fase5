// Verbind met websocket server
const socket = new WebSocket("ws://localhost:8765");

socket.onopen = function() {
    console.log("Verbonden met WebSocket server");
};

socket.onmessage = function(event) {

    // JSON data ontvangen
    const data = JSON.parse(event.data);

    console.log("Ontvangen:", data);

    // HTML updaten
    document.getElementById("temp").textContent = data.temperature;
    document.getElementById("pressure").textContent = data.pressure;
    document.getElementById("altitude").textContent = data.altitude;
};

socket.onerror = function(error) {
    console.error("WebSocket fout:", error);
};

socket.onclose = function() {
    console.log("WebSocket gesloten");
};
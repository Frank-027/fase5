// Verbind met websocket server
// Dynamisch IP of hostname van de server bepalen
const host = window.location.hostname;
const port = 8765;

// WebSocket openen per http of https protocol
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${window.location.hostname}:${port}/`);

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
// ======================================
// PUNE WATERLOGGING ML SYSTEM - MAP SCRIPT
// ======================================

let map;
let marker;

// Initialize Map centered on Pune
document.addEventListener("DOMContentLoaded", () => {
    map = L.map("map").setView([18.5204, 73.8567], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // Optional: Press Enter key to trigger search
    const input = document.getElementById("locationInput");
    if (input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") checkRisk();
        });
    }
});

// Fetch ML Prediction from Flask API (app.py)
async function checkRisk() {
    const locationName = document.getElementById("locationInput").value.trim();

    if (!locationName) {
        alert("Please enter or select a Pune locality name.");
        return;
    }

    document.getElementById("risk").innerText = "Waterlogging Risk: ⏳ Evaluating ML Model...";

    try {
        // Send request to Flask backend endpoint
        const response = await fetch("http://127.0.0.1:5001/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ location: locationName })
        });

        const data = await response.json();

        if (data.status === "SUCCESS") {
            displayMLResult(data);
        } else {
            document.getElementById("risk").innerText = "Waterlogging Risk: ⚠️ Error evaluating location";
        }
    } catch (error) {
        console.error("Connection Error:", error);
        document.getElementById("risk").innerText = "Waterlogging Risk: ❌ ML Server Offline (Check app.py)";
    }
}

// Display ML Prediction & Update Map Pin
function displayMLResult(data) {
    const { latitude, longitude } = data.coordinates;

    // Update UI text
    document.getElementById("cityName").innerText = "Location: " + data.location;
    document.getElementById("coordinates").innerText = `Coordinates: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
    document.getElementById("forecast").innerText = "Waterlogging Forecast: " + (data.is_waterlogged ? "Waterlogging Expected ⚠️" : "Normal Conditions ✅");

    // Format risk badge and pin color
    let riskBadge = "🟢 LOW";
    let pinColor = "#28a745";

    if (data.risk_category === "HIGH") {
        riskBadge = "🔴 HIGH";
        pinColor = "#dc3545";
    } else if (data.risk_category === "MEDIUM") {
        riskBadge = "🟡 MEDIUM";
        pinColor = "#ffc107";
    }

    document.getElementById("risk").innerText = `Waterlogging Risk: ${riskBadge} (${data.risk_percentage})`;

    // Display PMC Alert Banner if triggered
    const alertBox = document.getElementById("alertBox");
    if (data.pmc_authority_alert) {
        alertBox.innerHTML = `
            <div style="margin-top: 15px; padding: 12px; background: #f8d7da; border-left: 5px solid #dc3545; color: #721c24; border-radius: 5px;">
                <strong>🚨 PMC Authority Alert Issued:</strong><br>
                ${data.pmc_authority_alert.action_required}
            </div>`;
    } else {
        alertBox.innerHTML = "";
    }

    // Animate map view to location
    map.flyTo([latitude, longitude], 14, { duration: 1.2 });

    // Clear previous marker
    if (marker) {
        map.removeLayer(marker);
    }

    // Place new color-coded circular marker
    marker = L.circleMarker([latitude, longitude], {
        radius: 12,
        fillColor: pinColor,
        color: "#000",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
    }).addTo(map);

    marker.bindPopup(`
        <b>${data.location}</b><br>
        Risk Level: <b>${riskBadge} (${data.risk_percentage})</b>
    `).openPopup();
} 
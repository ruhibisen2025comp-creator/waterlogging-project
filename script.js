// ======================================
// PUNE WATERLOGGING ML SYSTEM - MAP SCRIPT
// ======================================

let map;
let marker;
let eventMarkersGroup;

// Initialize Map centered on Pune
document.addEventListener("DOMContentLoaded", () => {
    map = L.map("map").setView([18.5204, 73.8567], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    eventMarkersGroup = L.layerGroup().addTo(map);

    // Load initial map markers from event.json and hotspots
    loadHistoricalEvents();

    // Trigger search on Enter key
    const input = document.getElementById("locationInput");
    if (input) {
        input.addEventListener("keypress", (e) => {
            if (e.key === "Enter") checkRisk();
        });
    }
});

// Load historical events from event.json via root app.py API
async function loadHistoricalEvents() {
    try {
        const response = await fetch("/api/events");
        if (!response.ok) return;
        const events = await response.json();

        events.forEach(evt => {
            if (evt.latitude && evt.longitude) {
                const isHigh = evt.severity === "High";
                const color = isHigh ? "#dc3545" : (evt.severity === "Medium" ? "#ffc107" : "#28a745");

                const circle = L.circleMarker([evt.latitude, evt.longitude], {
                    radius: 8,
                    fillColor: color,
                    color: "#333",
                    weight: 1,
                    fillOpacity: 0.7
                });

                circle.bindPopup(`
                    <b>${evt.location} (${evt.city || 'Pune'})</b><br>
                    Date: ${evt.date || 'N/A'}<br>
                    Severity: <b>${evt.severity}</b><br>
                    <small>${evt.description}</small>
                `);

                eventMarkersGroup.addLayer(circle);
            }
        });
    } catch (err) {
        console.warn("Could not load initial events:", err);
    }
}

// Fetch ML Prediction from Root Backend API (app.py)
async function checkRisk() {
    const locationInput = document.getElementById("locationInput");
    const locationName = locationInput ? locationInput.value.trim() : "";

    if (!locationName) {
        alert("Please enter or select a Pune locality name.");
        return;
    }

    const riskElement = document.getElementById("risk");
    if (riskElement) {
        riskElement.innerText = "Waterlogging Risk: ⏳ Evaluating ML Model...";
    }

    try {
        // Send request to Root Flask Backend endpoint (/api/risk)
        const response = await fetch(`/api/risk?location=${encodeURIComponent(locationName)}`);
        
        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const data = await response.json();
        displayMLResult(data);

    } catch (error) {
        console.error("Connection Error:", error);
        if (riskElement) {
            riskElement.innerText = "Waterlogging Risk: ❌ ML Server Offline (Check app.py)";
        }
    }
}

// Display ML Prediction, 7 Features & Update Map Pin
function displayMLResult(data) {
    const loc = data.location || {};
    const weather = data.weather || {};
    const terrain = data.terrain || {};
    const pred = data.prediction || {};

    const lat = loc.latitude || 18.5204;
    const lng = loc.longitude || 73.8567;
    const locName = loc.name || "Pune Area";

    // 1. Update UI Locality & Coordinates
    document.getElementById("cityName").innerText = "Location: " + locName;
    document.getElementById("coordinates").innerText = `Coordinates: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;

    // 2. Display all 7 Dataset Parameters on Screen
    if (document.getElementById("precipVal")) {
        document.getElementById("precipVal").innerText = `${weather.precipitation || weather.rain || 0} mm`;
    }
    if (document.getElementById("humidityVal")) {
        document.getElementById("humidityVal").innerText = `${weather.humidity || 60}%`;
    }
    if (document.getElementById("elevationVal")) {
        document.getElementById("elevationVal").innerText = `${terrain.elevation || 550} m`;
    }
    if (document.getElementById("slopeVal")) {
        document.getElementById("slopeVal").innerText = `${terrain.slope || 1.5}°`;
    }
    if (document.getElementById("basinVal")) {
        document.getElementById("basinVal").innerText = terrain.is_basin === 1 ? "Yes (High Risk)" : "No";
    }

    // 3. Format Risk Level and Probability Badge
    const probability = pred.probability !== undefined ? pred.probability : (pred.risk_score || 50);
    const riskLevelStr = (pred.risk_level || pred.risk_category || "Moderate").toUpperCase();

    let riskBadge = "🟢 LOW";
    let pinColor = "#28a745";
    let forecastText = "Normal Conditions ✅";

    if (riskLevelStr.includes("HIGH")) {
        riskBadge = `🔴 HIGH (${probability.toFixed(1)}%)`;
        pinColor = "#dc3545";
        forecastText = "Waterlogging Expected ⚠️";
    } else if (riskLevelStr.includes("MODERATE") || riskLevelStr.includes("MEDIUM")) {
        riskBadge = `🟡 MEDIUM (${probability.toFixed(1)}%)`;
        pinColor = "#ffc107";
        forecastText = "Moderate Waterlogging Risk ⚠️";
    } else {
        riskBadge = `🟢 LOW (${probability.toFixed(1)}%)`;
    }

    document.getElementById("forecast").innerText = "Waterlogging Forecast: " + forecastText;
    document.getElementById("risk").innerText = `Waterlogging Risk: ${riskBadge}`;

    // 4. Display Alert Banner if triggered
    const alertBox = document.getElementById("alertBox");
    if (alertBox) {
        if (pred.pmc_authority_alert) {
            alertBox.innerHTML = `
                <div style="margin-top: 15px; padding: 12px; background: #f8d7da; border-left: 5px solid #dc3545; color: #721c24; border-radius: 5px;">
                    <strong>🚨 PMC Authority Alert Issued:</strong><br>
                    ${pred.pmc_authority_alert.action_required || "Caution advised in low-lying areas."}
                </div>`;
        } else if (riskLevelStr.includes("HIGH")) {
            alertBox.innerHTML = `
                <div style="margin-top: 15px; padding: 12px; background: #f8d7da; border-left: 5px solid #dc3545; color: #721c24; border-radius: 5px;">
                    <strong>🚨 High Risk Waterlogging Alert:</strong><br>
                    High probability of drainage overflow. Avoid underpasses and low-lying roads.
                </div>`;
        } else {
            alertBox.innerHTML = "";
        }
    }

    // 5. Animate Map & Place Primary Location Marker
    map.flyTo([lat, lng], 14, { duration: 1.2 });

    if (marker) {
        map.removeLayer(marker);
    }

    marker = L.circleMarker([lat, lng], {
        radius: 13,
        fillColor: pinColor,
        color: "#000",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.9
    }).addTo(map);

    marker.bindPopup(`
        <b>${locName}</b><br>
        Risk Level: <b>${riskBadge}</b><br>
        Precipitation: <b>${weather.precipitation || 0} mm</b>
    `).openPopup();
} 
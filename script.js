// ======================================
// WATERLOGGING SYSTEM
// ======================================


// PUT YOUR OPENWEATHER API KEY HERE

const API_KEY = "YOUR_API_KEY_HERE";


// ======================================
// CITY COORDINATES
// ======================================

const cities = {

    Pune: {
        lat: 18.5204,
        lon: 73.8567
    },

    Mumbai: {
        lat: 19.0760,
        lon: 72.8777
    },

    Delhi: {
        lat: 28.6139,
        lon: 77.2090
    },

    Bengaluru: {
        lat: 12.9716,
        lon: 77.5946
    },

    Chennai: {
        lat: 13.0827,
        lon: 80.2707
    },

    Hyderabad: {
        lat: 17.3850,
        lon: 78.4867
    },

    Kolkata: {
        lat: 22.5726,
        lon: 88.3639
    },

    Ahmedabad: {
        lat: 23.0225,
        lon: 72.5714
    },

    Nagpur: {
        lat: 21.1458,
        lon: 79.0882
    },

    Nashik: {
        lat: 19.9975,
        lon: 73.7898
    }

};


// ======================================
// CREATE MAP
// ======================================

var map = L.map("map").setView(
    [18.5204, 73.8567],
    11
);


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
        "&copy; OpenStreetMap contributors"
    }
).addTo(map);


var marker;


// ======================================
// GET WEATHER
// ======================================

function getWeather() {

    const city =
        document.getElementById("city").value;


    const location =
        cities[city];


    document.getElementById("cityName")
        .innerText = city;


    const url =
        `https://api.openweathermap.org/data/2.5/weather` +
        `?lat=${location.lat}` +
        `&lon=${location.lon}` +
        `&appid=${API_KEY}` +
        `&units=metric`;


    fetch(url)

        .then(response => {

            if (!response.ok) {

                throw new Error(
                    "Unable to get weather data"
                );

            }

            return response.json();

        })

        .then(data => {

            displayWeather(
                data,
                city,
                location
            );

        })

        .catch(error => {

            console.error(error);

            document.getElementById("weather")
                .innerText =
                "Unable to load current data.";

        });

}


// ======================================
// DISPLAY WEATHER
// ======================================

function displayWeather(
    data,
    city,
    location
) {


    const temperature =
        data.main.temp;


    const humidity =
        data.main.humidity;


    const weather =
        data.weather[0].description;


    let rainfall = 0;


    if (data.rain &&
        data.rain["1h"]) {

        rainfall =
            data.rain["1h"];

    }


    document.getElementById("weather")
        .innerText =
        "Weather: " + weather;


    document.getElementById("temperature")
        .innerText =
        "Temperature: " +
        temperature +
        " °C";


    document.getElementById("humidity")
        .innerText =
        "Humidity: " +
        humidity +
        " %";


    document.getElementById("rainfall")
        .innerText =
        "Rainfall: " +
        rainfall +
        " mm/h";


    calculateRisk(rainfall);


    // Move map

    map.setView(
        [location.lat, location.lon],
        11
    );


    // Remove previous marker

    if (marker) {

        map.removeLayer(marker);

    }


    // Add new marker

    marker = L.marker([
        location.lat,
        location.lon
    ]).addTo(map);


    marker.bindPopup(
        "<b>" + city + "</b><br>" +
        "Rainfall: " +
        rainfall +
        " mm/h"
    ).openPopup();

}


// ======================================
// WATERLOGGING RISK
// ======================================

function calculateRisk(rainfall) {

    let risk;

    if (rainfall >= 15) {

        risk =
            "🔴 HIGH";

    }

    else if (rainfall >= 5) {

        risk =
            "🟠 MEDIUM";

    }

    else {

        risk =
            "🟢 LOW";

    }


    document.getElementById("risk")
        .innerText =
        "Waterlogging Risk: " +
        risk;

}
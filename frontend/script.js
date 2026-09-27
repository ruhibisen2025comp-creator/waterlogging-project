// ==========================================
// PUNE WATERGUARD - SCRIPT.JS
// ==========================================


// ------------------------------------------
// SCROLL TO RISK CHECKER
// ------------------------------------------

function scrollToRisk() {

    const riskSection = document.getElementById("risk");

    riskSection.scrollIntoView({
        behavior: "smooth"
    });

}


// ------------------------------------------
// CHECK WATERLOGGING RISK
// ------------------------------------------

function checkRisk() {

    // Get the location entered by the user
    const locationInput = document.getElementById("location");

    // Get the result container
    const result = document.getElementById("result");

    // Get and clean the entered location
    const location = locationInput.value.trim();


    // --------------------------------------
    // CHECK EMPTY INPUT
    // --------------------------------------

    if (location === "") {

        result.innerHTML = `
            <div class="result-box moderate-result">

                <h3>⚠️ Enter a Location</h3>

                <p>
                    Please enter a Pune area to check
                    the waterlogging risk.
                </p>

            </div>
        `;

        return;
    }


    // --------------------------------------
    // HIGH-RISK AREAS
    // DEMO DATA
    // --------------------------------------

    const highRiskAreas = [

        "karve nagar",
        "kothrud",
        "sangamwadi",
        "yerwada",
        "hadapsar"

    ];


    // --------------------------------------
    // MODERATE-RISK AREAS
    // DEMO DATA
    // --------------------------------------

    const moderateRiskAreas = [

        "shivajinagar",
        "pimpri",
        "chinchwad",
        "baner"

    ];


    // Convert user input to lowercase
    // so that "Kothrud", "KOTHRUD",
    // and "kothrud" work the same way.

    const enteredLocation = location.toLowerCase();


    // --------------------------------------
    // CHECK HIGH RISK
    // --------------------------------------

    const isHighRisk = highRiskAreas.some(function(area) {

        return enteredLocation.includes(area);

    });


    if (isHighRisk) {

        result.innerHTML = `
            <div class="result-box high-result">

                <h3>🔴 High Risk</h3>

                <p>
                    ${location} has been identified as
                    a higher historical waterlogging-risk
                    area in this demo.
                </p>

            </div>
        `;

        return;
    }


    // --------------------------------------
    // CHECK MODERATE RISK
    // --------------------------------------

    const isModerateRisk = moderateRiskAreas.some(function(area) {

        return enteredLocation.includes(area);

    });


    if (isModerateRisk) {

        result.innerHTML = `
            <div class="result-box moderate-result">

                <h3>🟡 Moderate Risk</h3>

                <p>
                    ${location} has experienced
                    waterlogging under certain conditions
                    in this demo.
                </p>

            </div>
        `;

        return;
    }


    // --------------------------------------
    // LOW / UNKNOWN RISK
    // --------------------------------------

    result.innerHTML = `
        <div class="result-box low-result">

            <h3>🟢 Low / Unknown Risk</h3>

            <p>
                No high-risk location was found in
                the current demo data for ${location}.
            </p>

        </div>
    `;
}
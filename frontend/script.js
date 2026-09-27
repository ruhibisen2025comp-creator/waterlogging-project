// ==========================================
// PUNE WATERGUARD - SCRIPT.JS
// ==========================================


// ==========================================
// SCROLL TO RISK CHECKER
// ==========================================

function scrollToRisk() {

    const riskSection = document.getElementById("risk");

    if (riskSection) {
        riskSection.scrollIntoView({
            behavior: "smooth"
        });
    }
}


// ==========================================
// PUNE WATERLOGGING DATA
// ==========================================

const puneAreas = {

    // ======================================
    // HIGH RISK AREAS
    // ======================================

    "hadapsar": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 18,

        details:
            "Hadapsar-Mundhwa had 18 identified waterlogging spots in the 2025 PMC monsoon-preparedness list.",

        impact:
            "Traffic and local road movement may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "mundhwa": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 18,

        details:
            "Hadapsar-Mundhwa had 18 identified waterlogging spots in the 2025 PMC monsoon-preparedness list.",

        impact:
            "Local roads and traffic may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "wanowrie": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 14,

        details:
            "Wanowrie had 14 identified waterlogging spots in the 2025 PMC list.",

        impact:
            "Traffic and local road movement may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "bibwewadi": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 13,

        details:
            "Bibwewadi had 13 identified waterlogging spots in the 2025 PMC list.",

        impact:
            "Local roads may experience water accumulation during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "kondhwa": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 12,

        details:
            "Kondhwa-Yewalewadi had 12 identified waterlogging locations in the 2025 PMC list.",

        impact:
            "Some local roads may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "yewalewadi": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 12,

        details:
            "Kondhwa-Yewalewadi had 12 identified waterlogging locations in the 2025 PMC list.",

        impact:
            "Some local roads may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },

    "kasba peth": {
        risk: "High",
        status: "Multiple Identified Spots",
        spotCount: 10,

        details:
            "Kasba-Vishrambaugwada had 10 identified waterlogging locations in the 2025 PMC list.",

        impact:
            "Road movement may be affected during heavy rainfall.",

        source:
            "PMC 2025 waterlogging list"
    },


    // ======================================
    // MODERATE RISK AREAS
    // ======================================

    "kothrud": {
        risk: "Moderate",
        status: "Specific Locations Documented",

        spots: [
            "Omkar Garden Chowk",
            "Ashish Garden Chowk",
            "Pragati Hardware",
            "Maharashtra Bank",
            "Baltika Estate"
        ],

        details:
            "PMC reported waterlogging locations in Kothrud after rainfall in May 2025.",

        impact:
            "The documented locations may experience water accumulation during heavy rainfall.",

        source:
            "PMC report, May 2025"
    },

    "bavdhan": {
        risk: "Moderate",
        status: "Specific Locations Documented",

        spots: [
            "Bavdhan Police Chowki",
            "Ranwara Bridge",
            "Near Pradnya Ark Society",
            "Vasudha Itaasha Underpass",
            "Kalagram Society, Bhugaon Road"
        ],

        details:
            "PMC reported waterlogging locations in Bavdhan after rainfall in May 2025.",

        impact:
            "The documented locations may experience water accumulation during heavy rainfall.",

        source:
            "PMC report, May 2025"
    },

    "aundh": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Spicer College Road"
        ],

        details:
            "Spicer College Road in Aundh was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "Road movement may be affected at the documented location during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "karve nagar": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Pratigya Hall"
        ],

        details:
            "Pratigya Hall in Karve Nagar was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "karvenagar": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Pratigya Hall"
        ],

        details:
            "Pratigya Hall in Karve Nagar was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "dhayari": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "PARI Company"
        ],

        details:
            "The PARI Company location in Dhayari was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "lohegaon": {
        risk: "Moderate",
        status: "Specific Locations Documented",

        spots: [
            "Lohegaon Bus Stop",
            "Khese Park"
        ],

        details:
            "PMC included locations around Lohegaon Bus Stop and Khese Park in its 2025 waterlogging mitigation work.",

        impact:
            "Road movement may be affected at these documented locations during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "vadgaon sheri": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Near Arnold School"
        ],

        details:
            "PMC included a location near Arnold School in Vadgaon Sheri among its 2025 waterlogging mitigation works.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "bhavani peth": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Chandan Sweet Chowk"
        ],

        details:
            "Chandan Sweet Chowk in Bhavani Peth was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "kondhwa budruk": {
        risk: "Moderate",
        status: "Specific Location Documented",

        spots: [
            "Shraddha Nagar"
        ],

        details:
            "Shraddha Nagar in Kondhwa Budruk was included in PMC's 2025 waterlogging mitigation work.",

        impact:
            "The documented location may experience water accumulation during heavy rainfall.",

        source:
            "PMC monsoon-preparedness work, 2025"
    },

    "yerawada": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Yerawada-Kalas-Dhanori had multiple identified waterlogging spots in PMC records.",

        impact:
            "Some local roads may experience water accumulation during heavy rainfall.",

        source:
            "PMC waterlogging records"
    },

    "dhanori": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Dhanori has appeared in PMC historical waterlogging documentation.",

        impact:
            "Local road movement may be affected during heavy rainfall.",

        source:
            "PMC waterlogging records"
    },

    "baner": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Aundh-Baner has appeared in PMC waterlogging and monsoon-preparedness records.",

        impact:
            "Some roads may experience water accumulation during heavy rainfall.",

        source:
            "PMC waterlogging records"
    },

    "shivajinagar": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Shivajinagar-Ghole Road has appeared in PMC waterlogging records.",

        impact:
            "Busy roads may experience traffic disruption during heavy rainfall.",

        source:
            "PMC waterlogging records"
    },

    "viman nagar": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Viman Nagar has appeared in waterlogging-related records.",

        impact:
            "Road traffic may be affected during heavy rainfall.",

        source:
            "PMC / traffic-related records"
    },

    "kharadi": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Kharadi appears in broader Pune flood-control documentation.",

        impact:
            "Local roads may be affected during heavy rainfall.",

        source:
            "Pune flood-control documentation"
    },

    "wakad": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Wakad appears in broader Pune-region flood-control documentation.",

        impact:
            "Local roads may be affected during heavy rainfall.",

        source:
            "Flood-control documentation"
    },

    "hinjewadi": {
        risk: "Moderate",
        status: "Documented Historical Area",

        details:
            "Hinjewadi appears in broader Pune-region flood-control documentation.",

        impact:
            "Commuter routes may be affected during heavy rainfall.",

        source:
            "Flood-control documentation"
    },


    // ======================================
    // LOW / LIMITED DATA AREAS
    // ======================================

    "wagholi": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current Pune WaterGuard dataset does not contain enough specific spot-level evidence for Wagholi to assign a higher risk category.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "manjari": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Manjari.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "fursungi": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Fursungi.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "undri": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Undri.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "mohammadwadi": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Mohammadwadi.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "narhe": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Narhe.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "ambegaon": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for Ambegaon.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    },

    "nibm": {
        risk: "Low",
        status: "Limited Historical Data",

        details:
            "The current dataset contains limited specific information for NIBM.",

        impact:
            "Conditions may vary depending on rainfall intensity and the specific road.",

        source:
            "Pune WaterGuard demonstration dataset"
    }
};


// ==========================================
// CHECK WATERLOGGING RISK
// ==========================================

function checkRisk() {

    const locationInput =
        document.getElementById("location");

    const result =
        document.getElementById("result");


    if (!locationInput || !result) {
        return;
    }


    const location =
        locationInput.value.trim();


    // ======================================
    // EMPTY INPUT
    // ======================================

    if (location === "") {

        result.innerHTML = `

            <div class="result-box moderate-result">

                <h3>⚠️ Enter a Location</h3>

                <p>
                    Please enter a Pune area or locality
                    to check the waterlogging risk.
                </p>

            </div>

        `;

        return;
    }


    // ======================================
    // NORMALIZE INPUT
    // ======================================

    const enteredLocation =
        location.toLowerCase();


    let foundArea = null;
    let foundAreaName = "";


    // ======================================
    // SEARCH AREA
    // ======================================

    for (const areaName in puneAreas) {

        if (enteredLocation.includes(areaName)) {

            foundArea =
                puneAreas[areaName];

            foundAreaName =
                areaName;

            break;
        }
    }


    // ======================================
    // AREA FOUND
    // ======================================

    if (foundArea) {


        // ----------------------------------
        // RISK EMOJI
        // ----------------------------------

        let riskEmoji = "⚪";

        if (foundArea.risk === "High") {

            riskEmoji = "🔴";

        }
        else if (foundArea.risk === "Moderate") {

            riskEmoji = "🟡";

        }
        else if (foundArea.risk === "Low") {

            riskEmoji = "🟢";
        }


        // ----------------------------------
        // RESULT BOX CLASS
        // ----------------------------------

        let resultClass =
            "moderate-result";

        if (foundArea.risk === "High") {

            resultClass =
                "high-result";

        }
        else if (foundArea.risk === "Low") {

            resultClass =
                "low-result";
        }


        // ----------------------------------
        // DOCUMENTED SPOTS
        // ----------------------------------

        let spotsHTML = "";

        if (foundArea.spots) {

            spotsHTML = `

                <div class="result-detail">

                    <strong>
                        📍 Documented Location(s)
                    </strong>

                    <ul>

                        ${foundArea.spots
                            .map(
                                spot =>
                                    `<li>${spot}</li>`
                            )
                            .join("")}

                    </ul>

                </div>

            `;
        }


        // ----------------------------------
        // SPOT COUNT
        // ----------------------------------

        let spotCountHTML = "";

        if (foundArea.spotCount) {

            spotCountHTML = `

                <div class="result-detail">

                    <strong>
                        📊 Identified Spots:
                    </strong>

                    <span>
                        ${foundArea.spotCount}
                    </span>

                </div>

            `;
        }


        // ----------------------------------
        // FINAL RESULT
        // ----------------------------------

        result.innerHTML = `

            <div class="result-box ${resultClass}">

                <h3>
                    📍 ${foundAreaName.toUpperCase()}
                </h3>


                <h2>
                    ${riskEmoji}
                    ${foundArea.risk} Risk
                </h2>


                <p class="risk-status">
                    ${foundArea.status}
                </p>


                <div class="result-detail">

                    <strong>
                        📝 Details
                    </strong>

                    <p>
                        ${foundArea.details}
                    </p>

                </div>


                ${spotCountHTML}


                ${spotsHTML}


                <div class="result-detail">

                    <strong>
                        🚗 Possible Impact
                    </strong>

                    <p>
                        ${foundArea.impact}
                    </p>

                </div>


                <div class="result-detail">

                    <strong>
                        📚 Data Basis
                    </strong>

                    <p>
                        ${foundArea.source}
                    </p>

                </div>


                <div class="result-note">

                    <strong>
                        ⚠️ Important:
                    </strong>

                    This result is based on historical
                    or demonstration data. It is not a
                    live flood prediction. Actual
                    waterlogging can vary depending on
                    rainfall intensity, drainage conditions,
                    road location and other local factors.

                </div>

            </div>

        `;

        return;
    }


    // ======================================
    // UNKNOWN AREA
    // ======================================

    result.innerHTML = `

        <div class="result-box unknown-result">

            <h3>
                📍 ${location}
            </h3>


            <h2>
                ⚪ Risk Level: Unknown
            </h2>


            <p class="risk-status">
                No Data Available
            </p>


            <div class="result-detail">

                <strong>
                    📝 Details
                </strong>

                <p>
                    This locality is not currently
                    included in the Pune WaterGuard
                    demonstration dataset.
                </p>

            </div>


            <div class="result-note">

                <strong>
                    ⚠️ Important:
                </strong>

                No data does not mean that the area
                is completely safe from waterlogging.
                More historical information would be
                required to classify this location.

            </div>

        </div>

    `;

}
// google.charts.load("current", {packages:['corechart']});
// google.charts.setOnLoadCallback(drawChart);
// function drawChart() {
//   var data = google.visualization.arrayToDataTable([
//     ["Element", "Density", { role: "style" } ],
//     ["THEFT", 8.94, "#b87333"],
//     ["RIOTS", 10.49, "silver"],
//     ["DOWARY DEATH", 19.30, "gold"],
//     ["CASE OF HURT", 21.45, "color: #e5e4e2"],
//     ["OTHERS", 28.45, "color: RED"]

//   ]);

//   var view = new google.visualization.DataView(data);
//   view.setColumns([0, 1,
//                    { calc: "stringify",
//                      sourceColumn: 1,
//                      type: "string",
//                      role: "annotation" },
//                    2]);

//   var options = {
//     title: "Density of Precious Metals, in g/cm^3",
//     // width: 100,
//     // height: 100,
//     bar: {groupWidth: "95%"},
//     legend: { position: "none" },
//     backgroundColor:"white",
    
//   };
//   var chart = new google.visualization.ColumnChart(document.getElementById("columnchart_values"));
//   chart.draw(view, options);
// }






//Map



        // // Create a map centered around Karnataka
        // var map = L.map('map').setView([12.9716, 77.5946], 7);

        // // Add OpenStreetMap base layer to the map
        // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //     maxZoom: 19,
        //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        // }).addTo(map);

        // // Sample points in Karnataka with number of crimes
        // var points = [
            
        //     { name: "Bangalore", coordinates: [12.9716, 77.5946], crimes: 100 },
        //     { name: "Mysore", coordinates: [12.2958, 76.6394], crimes: 500 },
        //     { name: "Hubli", coordinates: [15.3647, 75.124], crimes: 20 }
        //     // Add more points as needed
        // ];

        // // Function to calculate marker color based on number of crimes
        // function getMarkerColor(crimes) {
        //     var opacity = Math.min(crimes / 100, 1); // Normalize crimes to range 0-100
        //     var color = 'rgba(255, 0, 0, ' + opacity + ')'; // Red color with opacity
        //     return color;
        // }

        // // Plot the points on the map
        // points.forEach(point => {
        //     var markerColor = getMarkerColor(point.crimes);
        //     L.marker(point.coordinates, { icon: L.divIcon({ html: '<div style="background-color: ' + markerColor + '; width: 25px; height: 25px; border-radius: 50%;"></div>' }) }).addTo(map)
        //         .bindPopup(point.name + '<br>Crimes: ' + point.crimes);
        // });



//handle clicking event in dropdown

document.getElementById('districts').addEventListener('change', function() {
    var selectedOption = this.value;
    fetch('/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({selectedOption: selectedOption})
    })
    .then(response => response.json())
    .then(data => {
        var secondDropdown = document.getElementById('places');
        secondDropdown.innerHTML = '                    <option value="">All</option>'; // Clear previous options
        data.forEach(option => {
            var optionElement = document.createElement('option');
            optionElement.textContent = option;
            optionElement.value=this.value+","+option;
            secondDropdown.appendChild(optionElement);
        });
    });
});

document.getElementById('districts').addEventListener('change', function() {
    var selectedOption = this.value;
    fetch('/process_crimeType_data1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({selectedOption:selectedOption})
    })
    .then(response => response.json())
    .then(data => {
        var secondDropdown = document.getElementById('crimeType');
        secondDropdown.innerHTML = '                    <option value="">All</option>'; // Clear previous options
        data.forEach(option => {
            var optionElement = document.createElement('option');
            optionElement.textContent = option;
            optionElement.value=option;
            secondDropdown.appendChild(optionElement);
        });
    });
});


document.getElementById('places').addEventListener('change', function() {
    var selectedOption = this.value;
    fetch('/process_crimeType_data2', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({selectedOption:selectedOption})
    })
    .then(response => response.json())
    .then(data => {
        var secondDropdown = document.getElementById('crimeType');
        secondDropdown.innerHTML = '                    <option value="">All</option>'; // Clear previous options
        data.forEach(option => {
            var optionElement = document.createElement('option');
            optionElement.textContent = option;
            optionElement.value=option;
            secondDropdown.appendChild(optionElement);
        });
    });
});






document.addEventListener('touchmove', function(event) {
    event.preventDefault();
}, { passive: false });




















document.getElementById("triggerButton0").addEventListener("click", function() {
    // Make an AJAX request to the Flask route
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/AccusedAnalysis", true);
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log("Flask route triggered successfully.");
            window.location.href = "/AccusedAnalysis";

        } else {
            console.error("Error triggering Flask route.");
        }
    };
    xhr.send();
});



document.getElementById("triggerButton1").addEventListener("click", function() {
    // Make an AJAX request to the Flask route
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/vitcimAnalysis", true);
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log("Flask route triggered successfully.");
            window.location.href = "/vitcimAnalysis";

        } else {
            console.error("Error triggering Flask route.");
        }
    };
    xhr.send();
});




document.getElementById("triggerButton2").addEventListener("click", function() {
    // Make an AJAX request to the Flask route
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/TimeSeries", true);
    xhr.onload = function () {
        if (xhr.status == 200) {
            console.log("Flask route triggered successfully.");
            window.location.href = "/TimeSeries";

        } else {
            console.error("Error triggering Flask route.");
        }
    };
    xhr.send();
});











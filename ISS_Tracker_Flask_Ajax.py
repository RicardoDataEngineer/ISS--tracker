from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# Function to get the current latitude and longitude of the ISS
def get_iss_position():
    # Make a GET request to the ISS API
    response = requests.get("http://api.open-notify.org/iss-now.json")
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the JSON response
    data = response.json()
    # Extract latitude and longitude from the response
    latitude = data["iss_position"]["latitude"]
    longitude = data["iss_position"]["longitude"]
    return latitude, longitude

# Route for the home page
@app.route("/")
def home():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ISS Tracker</title>
            <!-- Include jQuery and Leaflet libraries -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css"/>
            <style>
                #map { height: 400px; }
            </style>
        </head>
        <body>
            <h1>ISS TRACKER</h1>
            <!-- Create a div for the map -->
            <div id="map"></div>
            <!-- Display current position -->
            <h3>CURRENT POSITION</h3>
            <p>Latitude: <span id="latitude"></span>, Longitude: <span id="longitude"></span></p>
            <script>
                // Initialize the map
                var map = L.map('map').setView([0, 0], 2);
                // Add OpenStreetMap tile layer to the map
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
                // Add a marker for the ISS position
                var marker = L.marker([0, 0]).addTo(map);

                // Function to update ISS position
                function updateISSPosition() {
                    // Make a GET request to the server to get ISS position
                    $.get("/iss_position", function(data) {
                        // Split the response data into latitude and longitude
                        var position = data.split(",");
                        var latitude = parseFloat(position[0]);
                        var longitude = parseFloat(position[1]);
                        // Update latitude and longitude display
                        $("#latitude").text(latitude.toFixed(2));
                        $("#longitude").text(longitude.toFixed(2));
                        // Update marker position on the map
                        marker.setLatLng([latitude, longitude]);
                        // Set the map view to the ISS position
                        map.setView([latitude, longitude]);
                    });
                }

                // Call updateISSPosition when the document is ready
                $(document).ready(function() {
                    updateISSPosition();
                    // Update ISS position every 1000 milliseconds (1 second)
                    setInterval(updateISSPosition, 1000);
                });
            </script>
        </body>
        </html>
    """)

# Route to get ISS position
@app.route("/iss_position")
def iss_position():
    # Call get_iss_position function to get latitude and longitude
    latitude, longitude = get_iss_position()
    # Return latitude and longitude as a string
    return f"{latitude},{longitude}"

# Run the Flask app
if __name__ == "__main__":
    # Run the app on host '0.0.0.0' and port 50100 in debug mode
    app.run(host="0.0.0.0", port=50100, debug=True)

#!/usr/bin/env python3

"""
Create a Folium Map with GPS Data Visualization

This Python script reads GPS data from a log file and uses the Folium library to create
an interactive map that displays markers for GPS coordinates and connects them with a blue line.

The script follows these steps:
1. Load environment variables using dotenv for configuration.
2. Initialize a Folium map with the specified starting location and zoom settings.
3. Read GPS data from a log file ('logs/location_log.txt').
4. Extract latitude and longitude coordinates from the log file lines.
5. Add markers for each GPS coordinate on the Folium map.
6. Create a polyline to connect the markers, making it blue.
7. Save the interactive map to an HTML file ('log_gps_map.html').

Make sure to replace the environment variables 'FoliumStartpointLat', 'FoliumStartpointLon', 'FoliumMaxZoom', and 'FoliumStartZoom' with your specific values in your .env file.

Required Libraries:
- os: for working with the file system.
- dotenv: for loading environment variables from a .env file.
- folium: for creating interactive maps.
"""


import os
from dotenv import load_dotenv
import folium

from geopy.distance import great_circle

# Import dotenv 
load_dotenv()
FoliumStartpointLat = os.getenv('FoliumStartpointLat')
FoliumStartpointLon = os.getenv('FoliumStartpointLon')
FoliumMaxZoom = os.getenv('FoliumMaxZoom')
FoliumStartZoom = os.getenv('FoliumStartZoom')

# Inittialize Folium Map
FoliumMap = folium.Map(location=[FoliumStartpointLat, FoliumStartpointLon], zoom_start= FoliumStartZoom, max_zoom = FoliumMaxZoom)

def calculate_distance(coord1, coord2):
    return great_circle(coord1, coord2).kilometers

prev_coord = None  # Um die vorherige Koordinate zu verfolgen
total_distance = 0  # Um die gesamte Entfernung zu verfolgen

# Read the file with GPS data (replace 'your_data_file.txt' with your file's path)
with open('logs/location_log.txt', 'r') as LogFile:
    lines = LogFile.readlines()

# Lists to store values
serveDateTimes = []
clientIpAdresses = []
ClientIMEIs = []
locationDateTimes = []
gpsSatellites = []
latitudes = []
longitudes = []
accuracys = []
gpsSpeeds = []
headings = []

# Iterate through lines and extract GPS coordinates
for line in lines:
    if 'GPS' in line:
        parts = line.split('\t')
        serveDateTime = str(parts[0])
        clientIpAdress = str(parts[1])
        ClientIMEI = int(parts[2])
        locationDateTime = str(parts[4])
        gpsSatellite = int(parts[6])
        latitude = float(parts[7])
        longitude = float(parts[8])
        accuracy = float(parts[9])
        gpsSpeed = float(parts[10])
        heading = float(parts[11])
        
        serveDateTimes.append(serveDateTime)
        clientIpAdresses.append(clientIpAdress)
        ClientIMEIs.append(ClientIMEI)
        locationDateTimes.append(locationDateTime)
        gpsSatellites.append(gpsSatellite)
        latitudes.append(latitude)
        longitudes.append(longitude)
        accuracys.append(accuracy)
        gpsSpeeds.append(gpsSpeed)
        headings.append(heading)

# Add markers for each GPS coordinate
for lat, lon, imei, speed, heading, datetime, gpssatellite, accuracy in zip(latitudes, longitudes, ClientIMEIs, gpsSpeeds, headings, locationDateTimes, gpsSatellites, accuracys):
    info_text = f"<b>IMEI:</b> {imei}<br>"
    info_text += f"<b>Speed:</b> {speed} km/h<br>"
    info_text += f"<b>Heading:</b> {heading}°<br>"
    info_text += f"<b>Date/Time:</b> {datetime}<br>"
    info_text += f"<b>Accuracy:</b> {accuracy}<br>"
    info_text += f"<b>Satellites:</b> {gpsSatellite}"

    if prev_coord:
        current_coord = (lat, lon)
        distance = calculate_distance(prev_coord, current_coord)
        total_distance += distance
        info_text += f"<br><b>Distance:</b> {distance:.4f} km"

    prev_coord = (lat, lon)

    folium.Marker(
        [lat, lon],
        popup=folium.Popup(info_text, max_width=300),
        tooltip=f"IMEI: {imei}"
    ).add_to(FoliumMap)

# Show the total distance traveled in the tooltip of the last marker
if total_distance > 0:
    final_popup_text = info_text + f"<br><b>Total distance:</b> {total_distance:.2f} km"
    folium.Marker(
        [latitude, longitude],
        popup=folium.Popup(final_popup_text, max_width=300),
        tooltip=f"IMEI: {ClientIMEI}",
        icon=folium.Icon(color="red",icon="info-sign")
    ).add_to(FoliumMap)

# Create a PolyLine to connect the markers
coordinates = list(zip(latitudes, longitudes))
folium.PolyLine(locations=coordinates, color='blue').add_to(FoliumMap)

# Save the map to an HTML file
FoliumMap.save('log_gps_map.html')
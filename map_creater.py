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

# Import dotenv 
load_dotenv()
FoliumStartpointLat = os.getenv('FoliumStartpointLat')
FoliumStartpointLon = os.getenv('FoliumStartpointLon')
FoliumMaxZoom = os.getenv('FoliumMaxZoom')
FoliumStartZoom = os.getenv('FoliumStartZoom')

# Inittialize Folium Map
FoliumMap = folium.Map(location=[FoliumStartpointLat, FoliumStartpointLon], zoom_start= FoliumStartpointLat, max_zoom = FoliumStartZoom)

# Read the file with GPS data (replace 'your_data_file.txt' with your file's path)
with open('logs/location_log.txt', 'r') as LogFile:
    lines = LogFile.readlines()

# Lists to store latitude and longitude coordinates
latitudes = []
longitudes = []

# Iterate through lines and extract GPS coordinates
for line in lines:
    if 'GPS' in line:
        parts = line.split('\t')
        latitude = float(parts[-5])
        longitude = float(parts[-4])
        latitudes.append(latitude)
        longitudes.append(longitude)

# Add markers for each GPS coordinate
for lat, lon in zip(latitudes, longitudes):
    folium.Marker([lat, lon]).add_to(FoliumMap)

# Create a PolyLine to connect the markers
coordinates = list(zip(latitudes, longitudes))
folium.PolyLine(locations=coordinates, color='blue').add_to(FoliumMap)

# Save the map to an HTML file
FoliumMap.save('log_gps_map.html')
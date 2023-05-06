import subprocess
import googlemaps
import requests

API_KEY = 'YOUR_API_KEY_HERE'
url = 'google.com'

output = subprocess.check_output(['ping', '-c', '4', url]).decode('utf-8')

locations = []
for line in output.split('\n'):
    if 'time=' in line:
        ip_address = line.split()[3][1:-1]
        response = requests.get(f'https://ipapi.co/{ip_address}/latlong/').text
        location = tuple(map(float, response.split(',')))
        locations.append(location)

gmaps = googlemaps.Client(key=API_KEY)
fig = gmaps.figure()

for i, location in enumerate(locations):
    marker = gmaps.marker(location, label=f'{location[0]}, {location[1]}')
    fig.add_layer(marker)

route = gmaps.directions.Directions(locations[0], locations[-1], waypoints=locations[1:-1])
fig.add_layer(gmaps.directions.DirectionsRenderer(directions_result=route))

fig

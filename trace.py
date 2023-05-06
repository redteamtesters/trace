from flask import Flask, request, jsonify
import subprocess
import requests

app = Flask(__name__)

@app.route('/ping')
def ping():
    url = request.args.get('url', 'google.com')
    output = subprocess.check_output(['ping', '-c', '4', url]).decode('utf-8')
    locations = []
    for line in output.split('\n'):
        if 'time=' in line:
            ip_address = line.split()[3][1:-1]
            response = requests.get(f'https://ipapi.co/{ip_address}/latlong/').text
            location = tuple(map(float, response.split(',')))
            locations.append(location)
    return jsonify({'locations': locations})

if __name__ == '__main__':
    app.run

import time
import random
import usb.core
import usb.util
from flask import Flask, request

app = Flask(__name__)

def get_gps_location():
    # Simulate GPS data
    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    return latitude, longitude

# Function to communicate with the USB device
def communicate_with_usb_device(data):
    # Implement USB communication logic here
    # Example: Find USB device and send data
    dev = usb.core.find(idVendor=0x1234, idProduct=0x5678)
    if dev is not None:
        usb.util.claim_interface(dev, 0)
        dev.write(1, data, 1000)
        usb.util.release_interface(dev, 0)

@app.route('/update_location', methods=['POST'])
def update_location():
    vehicle_id = request.form.get('vehicle_id')
    latitude, longitude = get_gps_location()
    
    # Prepare data to send to USB device
    data = f"Vehicle ID: {vehicle_id}, Latitude: {latitude}, Longitude: {longitude}".encode('utf-8')
    
    # Call the function to communicate with the USB device
    communicate_with_usb_device(data)
    
    return f"Vehicle ID: {vehicle_id}, Latitude: {latitude}, Longitude: {longitude}"

@app.route('/trigger_alert', methods=['POST'])
def trigger_alert():
    vehicle_id = request.form.get('vehicle_id')
    horn_frequency = random.uniform(400, 500)
    
    if 400 <= horn_frequency <= 500:
        # Prepare data to send to USB device
        data = f"Alert triggered for Vehicle ID: {vehicle_id}".encode('utf-8')
        
        # Call the function to communicate with the USB device
        communicate_with_usb_device(data)
        
        return "Horn frequency in range! Alert triggered."
    
    return "No alert triggered."

@app.route('/status', methods=['GET'])
def get_status():
    # Check the status of the USB device or any other relevant information
    status = "Device connected"
    return status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

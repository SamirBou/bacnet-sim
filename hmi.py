import time
from flask import Flask, render_template, jsonify, request
import BAC0

# Create Flask application
app = Flask(__name__)

# BACnet configuration
DEVICE_ID = 3056
SERVER_IP = "0.0.0.0"

# Single global BAC0 client instance
bacnet_client = None

def initialize_bacnet():
    """Initialize the BAC0 client for BACnet communication"""
    try:
        # Use BAC0's direct client mode - creates minimal BACnet client
        print("Connecting to BACnet network...")
        BAC0.log_level('error')  # Reduce log noise
        return BAC0.lite()
    except Exception as e:
        print(f"Error connecting to BACnet: {e}")
        return None

def read_points():
    """Read current values from BACnet server (PLC)"""
    global bacnet_client
    
    # Default points
    points = {
        "fanStatus": False,
        "switchStatus": False,
        "emergencyStop": False
    }
    
    # Ensure we have a connection
    if bacnet_client is None:
        try:
            bacnet_client = initialize_bacnet()
        except Exception as e:
            print(f"Failed to initialize BACnet client: {e}")
            return points
    
    # Read each point from the BACnet server
    try:
        # Read fan status (binary output 1)
        try:
            fan_value = bacnet_client.read(f"{SERVER_IP} {DEVICE_ID} binary-output 1 present-value")
            points["fanStatus"] = str(fan_value).lower() in ('active', 'true', '1', 'on')
        except Exception as e:
            print(f"Error reading fan status: {e}")
        
        # Read switch status (binary value 1)
        try:
            switch_value = bacnet_client.read(f"{SERVER_IP} {DEVICE_ID} binary-value 1 present-value")
            points["switchStatus"] = str(switch_value).lower() in ('active', 'true', '1', 'on') 
        except Exception as e:
            print(f"Error reading switch status: {e}")
        
        # Read emergency stop (binary value 2)
        try:
            emergency_value = bacnet_client.read(f"{SERVER_IP} {DEVICE_ID} binary-value 2 present-value")
            points["emergencyStop"] = str(emergency_value).lower() in ('active', 'true', '1', 'on')
        except Exception as e:
            print(f"Error reading emergency stop: {e}")
            
    except Exception as e:
        print(f"Error reading points: {e}")
    
    return points

def write_point(point_name, value):
    """Write a value to a BACnet point on the server (PLC)"""
    global bacnet_client
    
    # Ensure we have a connection
    if bacnet_client is None:
        try:
            bacnet_client = initialize_bacnet()
            if bacnet_client is None:
                print("Failed to initialize BACnet client")
                return False
        except Exception as e:
            print(f"Failed to initialize BACnet client: {e}")
            return False
    
    # Map point names to BACnet objects
    point_map = {
        "SwitchStatus": "binary-value 1",
        "EmergencyStop": "binary-value 2"
    }
    
    if point_name not in point_map:
        print(f"Unknown point name: {point_name}")
        return False
    
    try:
        # Convert to BACnet active/inactive 
        value_str = "active" if value else "inactive"
        
        # Write to the BACnet server
        bacnet_client.write(f"{SERVER_IP} {DEVICE_ID} {point_map[point_name]} present-value {value_str}")
        print(f"Wrote {value_str} to {point_name}")
        return True
    except Exception as e:
        print(f"Error writing to {point_name}: {e}")
        return False

# Web routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/points', methods=['GET'])
def get_points():
    return jsonify(read_points())

@app.route('/api/write', methods=['POST'])
def api_write_point():
    data = request.json
    point_name = data.get('point')
    value = data.get('value')
    
    if point_name and value is not None:
        success = write_point(point_name, value)
        return jsonify({"success": success})
    
    return jsonify({"success": False, "error": "Invalid request"})

if __name__ == "__main__":
    print("Starting BACnet HMI...")
    print("Will read directly from BACnet server at", SERVER_IP)
    
    # Initialize BACnet client 
    bacnet_client = initialize_bacnet()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

# BACnet Simulator

A simple BACnet server and web interface for testing BACnet functionality.

## Quick Start

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Start the BACnet server:
```
python bacnetServer.py
```

3. In another terminal, start the web interface:
```
python hmi.py
```

4. Open http://localhost:5000 in your browser

## What It Does

This simulator creates a virtual BACnet device with three binary values:
- Fan status (controlled by the logic)
- Switch (can be toggled on/off)
- Emergency stop (overrides the switch)

The fan turns on when the switch is on AND the emergency stop is not activated.

## Architecture

This project uses BAC0 (a Python BACnet library) for both components:
- The server (bacnetServer.py) creates a virtual BACnet device with three points
- The HMI (hmi.py) provides a simple web interface to monitor and control the device

## Requirements

- Python 3.7+
- Flask
- BAC0
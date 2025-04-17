# BACnet Simulator PLC

A simple BACnet server simulator that emulates a PLC with readable and writable points.

## Quick Start

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Start the BACnet server:
```
python bacnetServer.py
```

## What It Does

This simulator creates a virtual BACnet device with three binary values:
- Fan status (controlled by the logic)
- Switch (can be toggled on/off)
- Emergency stop (overrides the switch)

The fan turns on when the switch is on AND the emergency stop is not activated.

## BACnet Points

The simulator exposes the following BACnet points:
- Binary Output 1: Fan status
- Binary Value 1: Switch state (writable)
- Binary Value 2: Emergency stop (writable)

You can read these points using standard BACnet clients and write to the writable points to test control logic.

## Architecture

This project uses BAC0 (a Python BACnet library) to create a virtual BACnet device that simulates PLC behavior. The logic implemented in the server automatically controls the fan based on the switch and emergency stop states.

## Requirements

- Python 3.7+
- BAC0
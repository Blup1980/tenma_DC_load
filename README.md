# tenma_dc_load

A simple Python package to control the Tenma DC Load model 72-13200 via serial interface.

## Features

- Set and read voltage, current, resistance, and power setpoints and limits
- Switch output ON/OFF
- Query device status and mode
- Measure real-time voltage, current, and power

## Requirements

- Python 3.7+
- [pyserial](https://pypi.org/project/pyserial/)
- [matplotlib](https://pypi.org/project/matplotlib/) (for the example only)

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

You can use the tenma72_13200 class to control the device:

```python
from tenma import tenma72_13200

with tenma72_13200(port='COM4', baudrate=9600, timeout=1) as load:
    load.set_output_state(True)
    voltage = load.measure_V()
    current = load.measure_I()
    print(f"Voltage: {voltage} V, Current: {current} A")
    load.set_output_state(False)
```

See more usage examples in the __main__ section of tenma/tenma72_13200.py.

## File Structure
- tenma/tenma72_13200.py: Main device control class
- basicBatteryLogger.py: Example script for battery logging
- requirements.txt: Python dependencies

## Notes
- The default serial port is COM4. Change it as needed for your system.
- The device must be connected via USB/serial and powered on.
- This package is designed for the Tenma 72-13200 DC Load only.

## License
MIT No Attribution License

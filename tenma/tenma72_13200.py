import serial


class tenma72_13200:
    def __init__(self, port='COM4', baudrate=9600, timeout=1):
        self.model = "Tenma 72-13200"
        self.description = "DC Load, 0-60V, 0-30A, 300W"
        self.serial_connection = None
        self.connected = False
        self.serial_connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
        
    def __enter__(self):
        """Context manager entry method to establish connection."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit method to close connection."""
        self.disconnect()
            

    def set_output_state(self, state: bool) -> None:
        """Set the output state of the device."""
        if self.connected:
            command = f':INP {"ON" if state else "OFF"}\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set output state.")

    def get_output_state(self) -> bool:
        """Get the current output state of the device."""
        if self.connected:
            self.serial_connection.write(b':INP?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            return response == 'ON'
        else:
            print("Device not connected. Cannot get output state.")
            return False
        
    def connect(self) -> None:
        """Establish a serial connection to the device."""
        try:
            self.serial_connection.open()
        except serial.SerialException as e:
            print(f"Error connecting to {self.model}: {e}")
        # check if the connection is open and ready by sending the *IDN? command

        self.serial_connection.write(b'*IDN?\n')
        response = self.serial_connection.readline().decode('utf-8').strip()
        if response:
            self.connected = True
        else:
            print("No response from device.")
            self.connected = False

    def disconnect(self) -> None:
        """Close the serial connection to the device."""
        if self.serial_connection:
            self.serial_connection.close()
            self.connected = False
        else:
            print("No active connection to disconnect.")

    def trigger(self) -> None:
        """Send a trigger command to the device."""
        if self.connected:
            self.serial_connection.write(b'*TRG\n')
        else:
            print("Device not connected. Cannot send trigger command.")

    def set_CV_V(self, voltage: float) -> None:
        """Set the output voltage of the device."""
        if self.connected:
            command = f':VOLT {voltage}V\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set voltage.")

    def get_CV_V(self) -> float:
        """Get the current output voltage of the device."""
        if self.connected:
            self.serial_connection.write(b':VOLT?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('V', ''))
            except ValueError:
                print("Invalid response for voltage.")
                return 0.0
        else:
            print("Device not connected. Cannot get voltage.")
            return 0.0
        

    def set_CV_V_min(self, voltage: float) -> None:
        """Set the minimum voltage limit."""
        if self.connected:
            command = f':VOLT:LOW {voltage}V\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set minimum voltage.") 


    def get_CV_V_min(self) -> float:
        """Get the minimum voltage limit."""
        if self.connected:
            self.serial_connection.write(b':VOLT:LOW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('V', ''))
            except ValueError:
                print("Invalid response for minimum voltage.")
                return 0.0
        else:
            print("Device not connected. Cannot get minimum voltage.")
            return 0.0
        

    def set_CV_V_max(self, voltage: float) -> None:
        """Set the maximum voltage limit."""
        if self.connected:
            command = f':VOLT:UPP {voltage}V\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set maximum voltage.")

    def get_CV_V_max(self) -> float:
        """Get the maximum voltage limit."""
        if self.connected:
            self.serial_connection.write(b':VOLT:UPP?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('V', ''))
            except ValueError:
                print("Invalid response for maximum voltage.")
                return 0.0
        else:
            print("Device not connected. Cannot get maximum voltage.")
            return 0.0

    def set_CC_I(self, current: float) -> None:
        """Set the output current of the device."""
        if self.connected:
            command = f':CURR {current}A\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set current.")

    def get_CC_I(self) -> float:
        """Get the current output current of the device."""
        if self.connected:
            self.serial_connection.write(b':CURR?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('A', ''))
            except ValueError:
                print("Invalid response for current.")
                return 0.0
        else:
            print("Device not connected. Cannot get current.")
            return 0.0

    def set_CC_I_min(self, current: float) -> None:
        """Set the minimum current limit."""
        if self.connected:
            command = f':CURR:LOW {current}A\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set minimum current.")

    def get_CC_I_min(self) -> float:
        """Get the minimum current limit."""
        if self.connected:
            self.serial_connection.write(b':CURR:LOW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('A', ''))
            except ValueError:
                print("Invalid response for minimum current.")
                return 0.0
        else:
            print("Device not connected. Cannot get minimum current.")
            return 0.0
        
    def set_CC_I_max(self, current: float) -> None:
        """Set the maximum current limit."""
        if self.connected:
            command = f':CURR:UPP {current}A\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set maximum current.")

    def get_CC_I_max(self) -> float:
        """Get the maximum current limit."""
        if self.connected:
            self.serial_connection.write(b':CURR:UPP?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('A', ''))
            except ValueError:
                print("Invalid response for maximum current.")
                return 0.0
        else:
            print("Device not connected. Cannot get maximum current.")
            return 0.0
        
    def set_CR_R(self, resistance: float) -> None:
        """Set the output resistance of the device."""
        if self.connected:
            command = f':RES {resistance}OHM\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set resistance.")

    def get_CR_R(self) -> float:
        """Get the current output resistance of the device."""
        if self.connected:
            self.serial_connection.write(b':RES?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('OHM', ''))
            except ValueError:
                print("Invalid response for resistance.")
                return 0.0
        else:
            print("Device not connected. Cannot get resistance.")
            return 0.0
        
    def set_CR_R_min(self, resistance: float) -> None:
        """Set the minimum resistance limit."""
        if self.connected:
            command = f':RES:LOW {resistance}OHM\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set minimum resistance.")

    def get_CR_R_min(self) -> float:
        """Get the minimum resistance limit."""
        if self.connected:
            self.serial_connection.write(b':RES:LOW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('OHM', ''))
            except ValueError:
                print("Invalid response for minimum resistance.")
                return 0.0
        else:
            print("Device not connected. Cannot get minimum resistance.")
            return 0.0
        
    def set_CR_R_max(self, resistance: float) -> None:
        """Set the maximum resistance limit."""
        if self.connected:
            command = f':RES:UPP {resistance}OHM\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set maximum resistance.")

    def get_CR_R_max(self) -> float:
        """Get the maximum resistance limit."""
        if self.connected:
            self.serial_connection.write(b':RES:UPP?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('OHM', ''))
            except ValueError:
                print("Invalid response for maximum resistance.")
                return 0.0
        else:
            print("Device not connected. Cannot get maximum resistance.")
            return 0.0
        
    def set_CW_W(self, power: float) -> None:
        """Set the output power of the device."""
        if self.connected:
            command = f':POW {power}W\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set power.")
        
    def get_CW_W(self) -> float:
        """Get the current power of the device."""
        if self.connected:
            self.serial_connection.write(b':POW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('W', ''))
            except ValueError:
                print("Invalid response for power.")
                return 0.0
        else:
            print("Device not connected. Cannot get power.")
            return 0.0
        
    def set_CW_W_min(self, power: float) -> None:
        """Set the minimum power limit."""
        if self.connected:
            command = f':POW:LOW {power}W\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set minimum power.")

    def get_CW_W_min(self) -> float:
        """Get the minimum power limit."""
        if self.connected:
            self.serial_connection.write(b':POW:LOW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('W', ''))
            except ValueError:
                print("Invalid response for minimum power.")
                return 0.0
        else:
            print("Device not connected. Cannot get minimum power.")
            return 0.0
    
    def set_CW_W_max(self, power: float) -> None:
        """Set the maximum power limit."""
        if self.connected:
            command = f':POW:UPP {power}W\n'.encode('utf-8')
            self.serial_connection.write(command)
        else:
            print("Device not connected. Cannot set maximum power.")

    def get_CW_W_max(self) -> float:
        """Get the maximum power limit."""
        if self.connected:
            self.serial_connection.write(b':POW:UPP?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('W', ''))
            except ValueError:
                print("Invalid response for maximum power.")
                return 0.0
        else:
            print("Device not connected. Cannot get maximum power.")
            return 0.0
        
    def set_mode(self, mode: str) -> None:
        """Set the operating mode of the device. the possible modes are 'VOLC', 'CURR', 'RES', and 'POW'. Other a ValueError will be raised."""
        if self.connected:
            if mode in ['VOLC', 'CURR', 'RES', 'POW']:
                command = f':FUNC {mode}\n'.encode('utf-8')
                self.serial_connection.write(command)
            else:
                raise ValueError("Invalid mode. Use 'VOLC', 'CURR', 'RES', or 'POW'.")
        else:
            print("Device not connected. Cannot set mode.")

    def get_mode(self) -> str:
        """Get the current operating mode of the device."""
        if self.connected:
            self.serial_connection.write(b':FUNC?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            return response
        else:
            print("Device not connected. Cannot get mode.")
            return ""

    def measure_V(self) -> float:
        """Measure the voltage at the load."""
        if self.connected:
            self.serial_connection.write(b':MEAS:VOLT?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('V', ''))
            except ValueError:
                print("Invalid response for measured voltage.")
                return 0.0
        else:
            print("Device not connected. Cannot measure voltage.")
            return 0.0
        
    def measure_I(self) -> float:
        """Measure the current at the load."""
        if self.connected:
            self.serial_connection.write(b':MEAS:CURR?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('A', ''))
            except ValueError:
                print("Invalid response for measured current.")
                return 0.0
        else:
            print("Device not connected. Cannot measure current.")
            return 0.0
        
    def measure_P(self) -> float:
        """Measure the power at the load."""
        if self.connected:
            self.serial_connection.write(b':MEAS:POW?\n')
            response = self.serial_connection.readline().decode('utf-8').strip()
            try:
                return float(response.replace('W', ''))
            except ValueError:
                print("Invalid response for measured power.")
                return 0.0
        else:
            print("Device not connected. Cannot measure power.")
            return 0.0
        

if __name__ == "__main__":
    # Example usage
    
    with tenma72_13200(port='COM4', baudrate=9600, timeout=1) as load:
        v = load.get_CV_V() 
        v_min = load.get_CV_V_min()
        v_max = load.get_CV_V_max()
        print(f"CV {v}V - Min: {v_min}V, Max: {v_max}V")  # Get current voltage

        a = load.get_CC_I()
        a_min = load.get_CC_I_min()
        a_max = load.get_CC_I_max()
        print(f"CC {a}A - Min: {a_min}A, Max: {a_max}A")  # Get current current

        r = load.get_CR_R()
        r_min = load.get_CR_R_min()
        r_max = load.get_CR_R_max()
        print(f"CR {r}OHM - Min: {r_min}OHM, Max: {r_max}OHM")  # Get current resistance

        w = load.get_CW_W()
        w_min = load.get_CW_W_min()
        w_max = load.get_CW_W_max()
        print(f"CW {w}W - Min: {w_min}W, Max: {w_max}W")  # Get current power

        f = load.get_mode()
        print(f"Current mode: {f}")  # Get current mode

        V = load.measure_V()
        I = load.measure_I()
        P = load.measure_P()
        print(f"Measured Voltage: {V}V, Current: {I}A, Power: {P}W")  # Measure voltage, current, and power

        state = load.get_output_state()
        print(f"Output state: {'ON' if state else 'OFF'}")  # Get output state
        
    
    # Initialize serial connection (example, adjust parameters as needed

    
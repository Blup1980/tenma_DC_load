from tenma import tenma72_13200
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Log the voltage and current from the Tenma 72-13200 DC load every second
# and save the data to a CSV file.
# graceful stop on Ctrl+C from the user

voltages = []
timestamps = []
cumulative_capacities = []

DURATION = 10  # seconds to log data

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Voltage')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ax.set_title('Voltage and Capacity over Time')

# Add secondary y-axis for capacity
ax2 = ax.twinx()
line2, = ax2.plot([], [], 'g-', label='Capacity')
ax2.set_ylabel('Capacity (Ah)')


with tenma72_13200(port='COM4', baudrate=9600, timeout=1) as load:
    with open('battery_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Time', 'Voltage (V)', 'Current (A)', 'Cumulative Capacity (Ah)'])

        try:
            load.set_output_state(True)  # Ensure the load is ON
            print("Logging started. Press Ctrl+C to stop.")
            start_time = datetime.now()
            now_old = start_time

            while True:
                voltage = load.measure_V()
                current = load.measure_I()
                now = datetime.now()
                timestamp = (datetime.now() - start_time).total_seconds()
                delta_t = (now - now_old).total_seconds()
                now_old = now    

                capacity = current * delta_t / 3600.0  # Convert to Ah
                cumulative_capacities.append(capacity if not cumulative_capacities else cumulative_capacities[-1] + capacity)

                writer.writerow([timestamp, voltage, current, cumulative_capacities[-1]])
                print(f'Time: {timestamp}; Voltage: {voltage} V; Current: {current} A; Capacity: {cumulative_capacities[-1]:.4f} Ah')

                # Update data for plotting
                voltages.append(voltage)
                timestamps.append(timestamp)

                # Update plot
                line.set_data(timestamps, voltages)
                # Cumulative capacity for plotting
                line2.set_data(timestamps, cumulative_capacities)
                ax.relim()
                ax.autoscale_view()
                ax2.relim()
                ax2.autoscale_view()
                plt.draw()
                plt.pause(DURATION)
                if not load.get_output_state():
                    break

            print("Logging stopped by device switching OFF.")
            while True:
                # Keep the plot open
                plt.pause(0.1)

        except KeyboardInterrupt:
            print("Logging stopped by user.")
            plt.show()

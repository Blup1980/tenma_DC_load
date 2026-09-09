from tenma import tenma72_13200
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Log the voltage and current from the Tenma 72-13200 DC load every second
# and save the data to a CSV file.
# graceful stop on Ctrl+C from the user

voltages = []
timestamps = []
cumulative_capacities = []

DURATION = 5  # seconds between samples
PRE_OUTPUT_DURATION = 20  # seconds to log before enabling the output
EXPECTED_CAPACITY_AH = 0.6  # Set this to the capacity printed on the battery pack
CUTOFF_VOLTAGE_V = 2.0  # Set this to the test cutoff voltage

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Voltage')
cutoff_voltage_line = ax.axhline(
    CUTOFF_VOLTAGE_V,
    color='blue',
    linestyle=':',
    label='Cutoff voltage',
)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ax.set_title('Voltage and Capacity over Time')
ax.grid(True, which='both', axis='both')

# Add secondary y-axis for capacity
ax2 = ax.twinx()
line2, = ax2.plot([], [], 'g-', label='Capacity')
expected_capacity_line = ax2.axhline(
    EXPECTED_CAPACITY_AH,
    color='red',
    linestyle=':',
    label='Expected capacity',
)
ax2.set_ylabel('Capacity (Ah)')

try:
    with tenma72_13200(port='COM10', baudrate=9600, timeout=1) as load, open('battery_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Time', 'Voltage (V)', 'Current (A)', 'Cumulative Capacity (Ah)'])

    
        load.set_output_state(False)
        output_enable_time = datetime.now() + timedelta(seconds=PRE_OUTPUT_DURATION)
        print(f"Logging started. Output will be enabled in {PRE_OUTPUT_DURATION} seconds. Press Ctrl+C to stop.")
        now_old = datetime.now()
        output_enabled = False

        while True:
            if not output_enabled and datetime.now() >= output_enable_time:
                load.set_output_state(True)
                output_enabled = True
                print("Output enabled (t=0).")

            voltage = load.measure_V()
            current = load.measure_I()
            now = datetime.now()
            timestamp = (now - output_enable_time).total_seconds()
            delta_t = (now - now_old).total_seconds()
            now_old = now    

            capacity = current * delta_t / 3600.0  # Convert to Ah
            cumulative_capacities.append(capacity if not cumulative_capacities else cumulative_capacities[-1] + capacity)

            writer.writerow([timestamp, voltage, current, cumulative_capacities[-1]])
            file.flush()
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
            ax.set_ylim(bottom=min(ax.get_ylim()[0], CUTOFF_VOLTAGE_V * 0.95), top=ax.get_ylim()[1])
            ax2.relim()
            ax2.autoscale_view()
            ax2.set_ylim(bottom=0, top=max(ax2.get_ylim()[1], EXPECTED_CAPACITY_AH * 1.05))
            plt.draw()
            plt.pause(DURATION)
            if output_enabled and not load.get_output_state():
                break

    print("Logging stopped by device switching OFF.")
    while True:
        # Keep the plot open
        plt.pause(0.1)

except KeyboardInterrupt:
    print("Logging stopped by user.")
    plt.show()

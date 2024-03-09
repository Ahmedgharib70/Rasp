import csv
from gpiozero import MCP3008
from time import sleep, time
from datetime import datetime

# Initialize MCP3008 objects
pot = MCP3008(0)
pot1 = MCP3008(1)
pot2 = MCP3008(2)

# Open CSV file for writing
with open('sensor_readings.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Time', 'Potentiometer', 'Current', 'Voltage'])
    print('| {0:>15} | {1:>16} | {2:>16} | {3:>16}|'.format('Time', 'Potentiometer', 'V1', 'V2'))

    # Print header separator
    print('-' * 65)

    try:
        while True:
            # Get current time
            current_time = datetime.now().strftime("%H:%M:%S")

            # Get potentiometer values
            pot_value = pot.value
            pot_value1 = pot1.value
            pot_value2 = pot2.value

            # Write data to CSV
            csv_writer.writerow([current_time, pot_value, pot_value1, pot_value2])

            # Print data to console
            print('| {0:>15} | {1:>15.3f} | {2:>15.3f} | {3:>15.3f} |'.format(current_time, pot_value, pot_value1, pot_value2))

            # Sleep for 1 second
            sleep(1.0)

    except KeyboardInterrupt:
        print("\nMeasurement stopped. Data stored in 'sensor_readings.csv'.")


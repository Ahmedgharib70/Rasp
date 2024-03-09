import spidev
import time
import math
import csv

# Setup SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0

# Variables to store sensor values and results for each sensor
sensor_values = [[0] * 100, [0] * 100, [0] * 100]
max_v = [0, 0, 0]
VmaxD = [0, 0, 0]  # Max voltage for each sensor
VeffD = [0, 0, 0]  # Effective voltage for each sensor
Veff = [0, 0, 0]   # Resulting voltage for each sensor

# Open CSV file for writing
csv_file = open('sensor_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'V1', 'V2', 'V3'])

# Print header separator
print('| {0:>15} | {1:>15} | {2:>15} | {3:>15} |'.format('Time', 'V1', 'V2', 'V3'))
print('-' * 65)

# Function to read ADC channel
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

try:
    while True:
        # Record start time
        start_time = time.strftime("%H:%M:%S", time.localtime())

        # Read and process sensor values for each sensor
        for sensor_num in range(3):
            for i in range(100):
                sensor_value = read_adc(sensor_num)  # Read from ADC channel based on sensor number
                sensor_values[sensor_num].append(sensor_value)
                time.sleep(0.001)  # Short delay for stability

            # Find the maximum sensor value in the array
            max_v[sensor_num] = max(sensor_values[sensor_num])

            # Calculate effective voltage based on the maximum sensor value for each sensor
            if max_v[sensor_num] != 0:
                VmaxD[sensor_num] = max_v[sensor_num]  # Set VmaxD to the maximum sensor value
                VeffD[sensor_num] = VmaxD[sensor_num] / math.sqrt(2)  # Calculate effective voltage (RMS) from VmaxD
                Veff[sensor_num] = (((VeffD[sensor_num] - 420.76) / -90.24) * -210.2) + 210.2  # Apply calibration and scaling to Veff
            else:
                Veff[sensor_num] = 0  # If no maximum value, set Veff to 0

        # Write the data to the CSV file
        csv_writer.writerow([start_time, Veff[0], Veff[1], Veff[2]])

        # Print data to console
        print('| {0:>15} | {1:>15.3f} | {2:>15.3f} | {3:>15.3f} |'.format(start_time, Veff[0], Veff[1], Veff[2]))
            
        # Reset values for the next iteration
        for sensor_num in range(3):
            VmaxD[sensor_num] = 0
            max_v[sensor_num] = 0
            sensor_values[sensor_num] = [0] * 100

        time.sleep(1.0)  # Delay for 100 milliseconds before the next loop

except KeyboardInterrupt:
    print("\nMeasurement stopped. Data stored in 'sensor_readings.csv'.")
    # Close CSV file and SPI on keyboard interrupt
    csv_file.close()
    spi.close()


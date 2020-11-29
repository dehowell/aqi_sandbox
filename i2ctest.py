import time

import smbus

# The number of the i2c bus - corresponds to /dev/i2c-CHANNELNUMBER
channel = 1
# Address of the sensor on the I2C bus, set by the manufacturer and fixed for a particular sensor.
address = 0x58

bus = smbus.SMBus(channel)

bus.write_i2c_block_data(address, 0x20, [0x03]) # init air quality command (see datasheet)
time.sleep(0.5)

t0 = time.time()
initialized = False
print("Ignoring start-up samples for first 15 seconds")
while 1: # Continuously measure air quality and print results
    bus.write_i2c_block_data(address, 0x20, [0x08]) # Send command to start measuring (see datasheet)
    time.sleep(0.5)
    data = bus.read_i2c_block_data(address, 0)[0:6]
    co2 = (data[0] << 8) + data[1]
    tvoc = (data[3] << 8) + data[4]
    if initialized:
        print("CO2: {} ppm, TVOC: {} ppb".format(co2, tvoc))
    else:
        t1 = time.time()
        initialized = t1 - t0 > 15
    time.sleep(0.5)


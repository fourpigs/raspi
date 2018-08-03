#!/usr/bin/env python3
#encoding=utf-8
## register latest room's humidity&temperature to DynamoDB
import smbus
import time

# initialize am2320
AM2320_ADDR = 0x5c
i2c = smbus.SMBus( 1 )

# Main
while True:
    try:
        i2c.write_i2c_block_data( AM2320_ADDR ,0x00, [] )
    except:
        pass

    time.sleep(0.003)
    i2c.write_i2c_block_data( AM2320_ADDR, 0x03, [ 0x00, 0x04 ] )

    time.sleep(0.015)
    data = i2c.read_i2c_block_data( AM2320_ADDR, 0x00, 6 )
    # floatだと怒られるので、intに
    # humi = int(float( data[2] << 8 | data[3] ) / 10)
    # temp = int(float( data[4] << 8 | data[5] ) / 10)
    humi = float( data[2] << 8 | data[3] ) / 10
    temp = float( data[4] << 8 | data[5] ) / 10

    print("Temperature:", temp, "C Humidity:", humi, "%")
    time.sleep(10)

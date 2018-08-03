#!/usr/bin/env python3
#encoding=utf-8
## register latest room's humidity&temperature to DynamoDB
import smbus
import time
import decimal

import boto3
from boto3.session import Session

# initialize am2320
AM2320_ADDR = 0x5c
i2c = smbus.SMBus( 1 )

def create_table():
  table = dynamodb.create_table(
    TableName = 'temphumi',
    KeySchema =[
      {
        'AttributeName' : 'am2320',
        'KeyType' : 'HASH'
      }
    ],
    AttributeDefinitions = [
      {
        'AttributeName' : 'am2320',
        'AttributeType' : 'N'
      }
    ],
    ProvisionedThroughput = {
      'ReadCapacityUnits' : 1,
      'WriteCapacityUnits' : 1
    },
  )
  table.meta.client.get_waiter('table_exists').wait(TableName = 'temphumi')
  tablename = dynamodb.Table('temphumi')
  table = tablename.put_item(
    Item={
      'am2320': 1,
      'temp': { 'Value': 0},
      'humi': { 'Value': 0},
    }
  )

def update_data(temp,humi):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('temphumi')
    response = table.update_item( Key = {'am2320' : 1 }, AttributeUpdates={ 'temp': { 'Value': decimal.Decimal(str(temp)), 'Action': 'PUT' }, 'humi': { 'Value': decimal.Decimal(str(humi)), 'Action': 'PUT' } })

# Main
while True:
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    response = client.list_tables()
    if 'temphumi' in response['TableNames']:
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
        update_data(temp,humi)
        time.sleep(10)
    else:
        create_table()

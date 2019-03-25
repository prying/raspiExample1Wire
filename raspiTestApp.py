import os
import time
import requests

max31820_sensor = '/sys/bus/w1/devices/SOME_ADDRESS/w1_slave'
key = 'SOME_KEY'
sensor_read_time_interval = 60 # seconds

# Read temp of one wire device using r-pi driver


def get_temp():
    # Open w1_slave and store lines
    f = open(max31820_sensor, 'r')
    lines = f.readlines()
    f.close()

    # Find the temp in the second line
    temp_pos = lines[1].find('t=')
    if temp_pos != -1:
        string_buff = lines[1].strip()[temp_pos+2:]
        temp = float(string_buff)/1000.0
        return temp

# Sends data to API
def send_data(temp, key):
    response = requests.get("http://iottemperatureapi.azurewebsites.net/update?key="+key+"&temp="+str(temp))
    # Check if it was a valid response
    if (response.text.find('Invalid') != -1):
        print('Error: Failed to send data to API:' + response.text)
        return 0

    return 1

while(1):
    temp = get_temp()
    send_data(temp, key)
    time.sleep(sensor_read_time_interval)

print('temperature recorder stopping')









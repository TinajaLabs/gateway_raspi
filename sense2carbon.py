#!/usr/bin/env python
import serial, syslog, time, math
from xbee import xbee

from urlparse import urlparse
import json
import httplib
import urllib 



# SERIALPORT = "/dev/tts/0"    # the com/serial port the XBee is connected to
SERIALPORT = "/dev/ttyAMA0"    # the com/serial port the XBee is connected to
BAUDRATE = 9600      # the baud rate we talk to the xbee


import argparse
import socket
import time

# CARBON_SERVER = '192.168.5.3'
# CARBON_SERVER = '192.168.0.14'
# CARBON_SERVER = '192.168.0.28'
CARBON_SERVER = '192.168.0.109'
CARBON_PORT = 2003
# CARBON_PORT = 80


# open up the FTDI serial port to get data transmitted to xbee
ser = serial.Serial(SERIALPORT, BAUDRATE)
ser.open()
print "serial port opened...?"
syslog.syslog("serial port opened...")

print "ready...  and waiting for sensor data"

smartURIBase = "http://10.15.2.56:8000"
httpConnection = None




def send2Carbon(metric_path, value):

    if (value <=0):
        return

    cValue = clamp(value, 0, 1023)

    timestamp = int(time.time())
    message = '%s %s %d\n' % (metric_path, cValue, timestamp)
    # print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()





##############################################################
def smartInit():

    httpConnection = httplib.HTTPConnection("10.15.2.56:8000")


    myBaseObjJSON = {'resourceName': 'sensors','resourceClass': 'SmartObject'}

    sensorObsJSON = {'resourceName': 'temperature','resourceClass': 'ObservableProperty'}


    # dlService = {"resourceName": "xivelyObserver","resourceClass":  "xivelyPublisher",'apiBase': 'https://api.xively.com/v2/feeds','feedID': '10258','streamID': 'temp','apiKey': 'xxx','updateInterval': 100 }
    dlService = {"apiBase": "https://api.xively.com/v2/feeds", "apiKey": "xxx", "feedID": "10258", "streamID": "temp", "resourceName": "xivelyObserver", "updateInterval": 100, "resourceClass": "xivelyPublisher"}


    httpConnection.request('POST', "", json.dumps(myBaseObjJSON), {"Content-Type": "application/json"})

    httpConnection.getresponse()

    httpConnection.request('POST', "sensors", json.dumps(sensorObsJSON), {"Content-Type": "application/json"})

    httpConnection.getresponse()

    # print "json.dumps: " + json.dumps(dlService)

    httpConnection.request('POST', "sensors/temperature/Observers", json.dumps(dlService), {"Content-Type": "application/json"})

    print httpConnection.getresponse().read()
    # print "testing: " + test.reason

    # print "test.read: " + test.read()



##############################################################

def send2Smart(metric_path, value):

    httpConnection = httplib.HTTPConnection("10.15.2.56:8000")

    if (value <=0):
        return

    timestamp = int(time.time())
    message = '%s %s %d\n' % (metric_path, value, timestamp)


    # print 'sending message:\n%s' % message
    print 'sending message:\n%s' % value

    # uriObject = urlparse(smartURIBase + "/sensors/temperature")
    
    # httpConnection = httplib.HTTPConnection(uriObject.netloc)

    httpConnection.request('PUT', "/sensors/temperature", json.dumps(value), {"Content-Type": "application/json"})

    print httpConnection.getresponse().read()

    # httpConnection.getresponse()


##############################################################

def send2Smart_orig(metric_path, value):

    if (value <=0):
        return

    timestamp = int(time.time())
    message = '%s %s %d\n' % (metric_path, value, timestamp)


    # print 'sending message:\n%s' % message
    print 'sending message:\n%s' % value

    uriObject = urlparse(smartURIBase + "/sensors/temperature")
    
    httpConnection = httplib.HTTPConnection(uriObject.netloc)

    httpConnection.request('PUT', uriObject.path, json.dumps(value), {"Content-Type": "application/json"})

    httpConnection.getresponse()



##############################################################
def calctemp(xb):
    try:
        mVolts = xb.analog_samples[0][1]  # Report the millivolts from the TMP36
    except Exception, e:
        print "calctemp exception: "+str(e)
        syslog.syslog("TLSM.calctemp exception: "+str(e))
        return 0

    # tempC = mVolts * 0.1              # Convert millivolts to Celcius
    voltage = mVolts * 3.3 / 1024       # Convert millivolts to Celcius
    tempC = (voltage - .5) * 100        # Convert millivolts to Celcius

    tempF = math.floor(tempC * 9 / 5 + 32)        # Convert to Fehrenheit

    # Print formated tempurature readings
    # print tempC, "C \t", tempF, "F - ", mVolts, voltage
    return tempF

##############################################################
def smoothout(xb):
    return ""

##############################################################
def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n

# smartInit()

while True:
    # grab one packet from the xbee, or timeout
    # syslog.syslog("testReader.py - " + time.strftime("%Y %m %d, %H:%M"))
    # time.sleep(.1)

    try:
        packet = xbee.find_packet(ser)
    except Exception, f:
        print "    find_packet: ", f
        continue


    if not packet:
        # print "    no serial packet found... "+ time.strftime("%Y %m %d, %H:%M")
        # syslog.syslog("TLSM.mainloop exception: no serial packet found..." )
        continue


    if packet:
        # if we have a packet but it has problems
        try:
            xb = xbee(packet)
        except Exception, x:
            print "    packet exception: ", x
            continue

        # this section to test for bad xb object
        try:
            if xb.address_16 == 99:
                continue
        except Exception, e:
            print "    bad xb object: ", e
            continue

        try:

            # slow it down a bit
            time.sleep(0.5)

            if xb.address_16 == 13:
                print "013: ", xb.analog_samples[0][0], xb.analog_samples[0][1], xb.analog_samples[0][2], xb.analog_samples[0][3]
                send2Carbon("tinaja.13.0", xb.analog_samples[0][0])
                send2Carbon("tinaja.13.1",  calctemp(xb))
                send2Carbon("tinaja.13.2", xb.analog_samples[0][2])
                send2Carbon("tinaja.13.3", xb.analog_samples[0][3])

                # send2Smart("tinaja.13.0", xb.analog_samples[0][0])
                # send2Smart("tinaja.13.1",  calctemp(xb))
                # send2Smart("tinaja.13.2", xb.analog_samples[0][2])
                # send2Smart("tinaja.13.3", xb.analog_samples[0][3])
                continue

            if xb.address_16 == 29:
                print "029: ", xb.analog_samples[0][0], xb.analog_samples[0][1], xb.analog_samples[0][2], xb.analog_samples[0][3]
                send2Carbon("tinaja.29.0", xb.analog_samples[0][0])
                send2Carbon("tinaja.29.1",  calctemp(xb))
                send2Carbon("tinaja.29.2", xb.analog_samples[0][2])
                send2Carbon("tinaja.29.3", xb.analog_samples[0][3])
                continue

            if xb.address_16 == 23:
                print "023: ", xb.analog_samples[0][0], xb.analog_samples[0][1], xb.analog_samples[0][2], xb.analog_samples[0][3]
                send2Carbon("tinaja.23.0", xb.analog_samples[0][0])
                send2Carbon("tinaja.23.1", calctemp(xb))
                send2Carbon("tinaja.23.2", xb.analog_samples[0][2])
                send2Carbon("tinaja.23.3", xb.analog_samples[0][3])
                continue

            if xb.address_16 == 12:
                print "012: ", xb.analog_samples[0][0], xb.analog_samples[0][1], xb.analog_samples[0][2], xb.analog_samples[0][3]
                send2Carbon("tinaja.12.0", xb.analog_samples[0][0])
                send2Carbon("tinaja.12.1",  calctemp(xb))
                send2Carbon("tinaja.12.2", xb.analog_samples[0][2])
                send2Carbon("tinaja.12.3", xb.analog_samples[0][3])
                continue

        except Exception, e:
            print "xb exception: "+str(e)
            syslog.syslog("xb exception: "+str(e))


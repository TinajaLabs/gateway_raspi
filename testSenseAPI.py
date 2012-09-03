#!/usr/bin/env python
import serial, math
from xbee import xbee
import urllib2
import simplejson


SERIALPORT = "/dev/tts/0"    # the com/serial port the XBee is connected to
BAUDRATE = 9600      # the baud rate we talk to the xbee

# open up the FTDI serial port to get data transmitted to xbee
ser = serial.Serial(SERIALPORT, BAUDRATE)
ser.open()


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
    print tempC, "C \t", tempF, "F - ", mVolts, voltage
    return tempF



while True:
    # grab one packet from the xbee, or timeout
    packet = xbee.find_packet(ser)
    if packet:
        xb = xbee(packet)
	
	# print "       >>> "
        # print xb

	thisTemp = calctemp(xb)

        # define a Python data dictionary
        data = {'feed_id': '2271', 'value': thisTemp}
        data_json = simplejson.dumps(data)
        host = "http://api.sen.se/events/?sense_key=3aDtyWpZYcgXCYpDM5az_A"
        req = urllib2.Request(host, data_json, {'content-type': 'application/json'})
        response_stream = urllib2.urlopen(req)
        response = response_stream.read()

        print response


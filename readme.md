This is some python code that I use to manage a group of xbee based sensor boards from a Raspberry Pi with an attached Xbee radio.  The main program is allsensors.py.

You can see my rough notes and references at: 
http://tinajalabs.wordpress.com/2012/09/02/raspberry-pi-as-an-xbee-wireless-sensor-network-gateway/

To run it you'll need to create a default.cfg file (in the same directory) that looks like this:


	[apikeys]
	thingspeak_key: 
	cosm_key: 
	sense_key: 
	twitterusername: 
	twitterpassword: 
	tinaja_key: 
	[paths]
	locallogpath: /var/www/tinajalog
	tinajalogurl: 
	senselogurl: http://api.sen.se/events/?sense_key=
	thingspeaklogurl: api.thingspeak.com

Look at the import commands and you'll see it will require the following python modules:

* SUDS
* EEML
* pySerial
* simplejson


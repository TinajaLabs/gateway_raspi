import csv, sys

print sys.platform
print sys.copyright
print ">>>"
print sys.version
# print sys.path
# print sys.modules
print "--------------------------------------------"


class Sensors():
    sensors = []

    def __init__(self):
        self.sensors = []

    def __init__(self, f):
        if f:
            self.readconfig(f)

    def find(self, sensornum)
        for sensor in self.sensors:
            if sensor.sensornum = sensornum:
                return sensor

        sensor = Sensor(sensornum)
        self.sensors.append(sensor)
        return history

 
    def readconfig(self, f)
        configReader = csv.reader(open('sensorconfig.csv', 'rb'))
        for row in configReader:
            sensornum = row[0]
            sensor = self.find(sensornum)

            sensor.desc = row[1]
            sensor.xid = row[2]
            sensor.tlogkey = row[3]
            sensor.plogkey = row[4]
            sensor.pchmin = row[5]
            sensor.pchmax = row[6]


    def __str__(self):
        s = ""
        for sensor in self.sensors:
            s += sensor.__str__()
        return s



class Sensor():
    #id, desc, xid, tlogkey, plogkey, pchmin, pchmax
    sensorid = 0
    desc = ""
    xid = 0
    tlogkey = ""
    plogkey = ""
    pchmin = ""
    pchmax = ""

    def __str__(self):
        return "[ id#: %d, 5mintimer: %f, lasttime; %f, 5minwatthr: %f, daywatthr = %f]" % (self.sensornum, self.fiveminutetimer, self.lasttime, self.cumulative5mwatthr, self.dayswatthr)
        return "[ id#: %d, desc: %f, lasttime: %f, 5minwatthr: %f, daywatthr = %f]" % (self.sensornum, self.fiveminutetimer, self.lasttime, self.cumulative5mwatthr, self.dayswatthr)




import threading
import time
import requests
import os.path
import datetime
import csv
from gps import *
from os import path

class GPS_poller(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.latitude = None
        self.longitude = None
        self.speed = None
        self.climb = None
        self.time = None
        
    def get_current_value(self):
        return self.current_value
    
    
    # Method for retrieving latitude
    def get_latitude(self):
        return self.latitude
    
    # Method for retrieving longitude
    def get_longitude(self):
        return self.longitude
    
    # Method for retrieving speed
    def get_speed(self):
        return self.speed
    
    # Method for retrieving climb
    def get_climb(self):
        return self.climb
    
    # Method for retrieving time
    def get_time(self):
        return self.time
    
    # Method to run automatically. Try to set the self.___ to sessions.fix.____
    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
                self.latitude = self.session.fix.latitude
                self.longitude = self.session.fix.longitude
                self.speed = self.session.fix.speed
                self.climb = self.session.fix.climb
                self.time = self.session.fix.time
                time.sleep(0.5)
        except StopIteration:
            pass
        
# Main program
        
if __name__ == '__main__':
    
    # Create and initialize global variables/objects
    gpsp = GPS_poller()
    gpsp.start()
    latitude = None
    longitude = None
    speed = None
    timeStamp = None
    counter = 0
    date_object = datetime.date.today()
    
    # Define name of the file to write to and its header. test_dummy is used for checking if the header
    # of a file is correct
    file_name = "GPSDATA{}.csv".format(date_object)
    file_header = "Latitude,Longitude,Time,Speed"
    test_dummy = ['Latitude', 'Longitude', 'Time', 'Speed']
    
    # Check if the file with the specified name exists, if not create it, if it does, check the header
    # if header is wrong, overwrite the file with new header.
    # PERHAPS CHANGE THIS SO THAT THE HEADER IS SIMPLY ADDED TO THE TOP OF THE FILE ?
    if not path.exists(file_name):
        with open(file_name, "w") as f:
            f.write(file_header)
    else:    
        f = open(file_name, newline='')
        reader = csv.reader(f)
        header = next(reader)
        f.close()
        if not header == test_dummy:
            with open(file_name, "w") as f:
                f.write(file_header)
                f.write("Latitude,Longitude,Time,Speed")
                
    # Main loop. Retrieves the latitude, longitude, speed and time every iteration. Time is given by datetime
    # for accuracy. The GPS-time is not accurate enough (IT SEEMS).
    # Checks if the latitude and longitude are true coordinates or not, and if they are, form a string to append
    # to the csv-file. Counter for knowing the amount of coordinates retrieved. 
    
    # In commented section: requests from the server in which the longitude and latitude is specified and sent to
    # the server. 
    
    # TODO: modify the server so that it can store speed, time and perhaps more data. 
    # TODO: modify the requests to that all the relevant data is sent
    # TODO: add retrieving of accelerometer-data and Kalman filter to the position, speed and acceleration data. 
    while 1:
        latitude = gpsp.get_latitude()
        longitude = gpsp.get_longitude()
        speed = gpsp.get_speed()
        timestamp = datetime.datetime.now()
        text = "\n"+str(latitude)+","+str(longitude)+","+str(timestamp)+","+str(speed)
        if latitude != None and latitude > 0.0:
            counter += 1
            with open(file_name, "a") as f:
                f.write(text)
            print('Lat: ',latitude, 'Lon: ', longitude, ' Speed: ', speed, ' Time: ', timestamp, ' Coordinates sent: ',counter)
        time.sleep(1)
        
        
#r = requests.get('http://94.254.77.173/write_data.php?lon='+str(longitude)+'&lat='+str(latitude))
#if r.status_code == 200:
#    print('Success!')
#elif r.status_code == 404:
#    print('Not found.')
import threading
import requests
import time
import front
import datetime

class WebsiteChecker(threading.Thread):
    def __init__(self, website, interval, front, id):
        threading.Thread.__init__(self)
        self.website = website
        self.status = None
        self.interval = interval
        self.front = front
        self.id = id
        self.stop_event = threading.Event()
        self.skip_event = threading.Event()
        
    def check_website(self):
        try:
            response = requests.head(self.website, timeout=5)
            if response.status_code < 400:
                if self.status =="DOWN":
                    with open("LOG.txt", 'w') as file:
                        file.append("Website " + self.website + " is back up: " + datetime.datetime.now())
                self.status = "UP"
            else:
                if self.status =="UP":
                    with open("LOG.txt", 'w') as file:
                        file.append("Website " + self.website + " has gone down: " + datetime.datetime.now())
                self.status = "DOWN"
        except requests.exceptions.RequestException:
            self.status = "DOWN"

    def run(self):
        while not self.stop_event.is_set():
            self.check_website()
            self.skip_event.wait(self.interval)
                
    def getStatus(self):
        return self.status
    
    def stop(self):
        self.stop_event.set()
        self.skip_event.set()
        
    def skip(self):
        self.skip_event.set()
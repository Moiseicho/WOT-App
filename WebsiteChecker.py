import threading
import requests
import time
import front

class WebsiteChecker(threading.Thread):
    def __init__(self, website, interval, front, id):
        threading.Thread.__init__(self)
        self.website = website
        self.status = None
        self.interval = interval
        self.front = front
        self.id = id

    def check_website(self):
        try:
            response = requests.head(self.website, timeout=5)
            if response.status_code < 400:
                self.status = "UP"
            else:
                self.status = "DOWN"
        except requests.exceptions.RequestException:
            self.status = "DOWN"

    def run(self):
        while True:
            self.check_website()
            time.sleep(self.interval)
    
    def getStatus(self):
        return self.status
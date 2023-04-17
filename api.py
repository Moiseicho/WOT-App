from flask import Flask, jsonify, request
import time
import requests
import threading
import os

app = Flask(__name__)

class WebsiteChecker(threading.Thread):
    def __init__(self, website, interval, status_code):
        threading.Thread.__init__(self)
        self.website = website
        self.status = None
        self.interval = interval
        self.daemon = True
        self.status_code = status_code

    def check_website(self):
        try:
            resp = requests.head(self.website, timeout=5)
            if resp.status_code == self.status_code:
                self.status = 'UP'
            else:
                self.status = 'DOWN'
        except requests.exceptions.RequestException:
            self.status = 'DOWN'

    def run(self):
        print('Starting thread for website {}'.format(self.website))
        while True:
            self.check_website()
            time.sleep(self.interval)

websites = {}

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the website checker API'}), 200

@app.route('/websites', methods=['POST'])
def add_website():
    website = request.json.get('website')
    interval = request.json.get('interval', 10)
    status_code = request.json.get('status_code', 200)
    if website in websites:
        return jsonify({'error': 'Website already exists'}), 409
    thread = WebsiteChecker(website, interval, status_code)
    websites[len(websites)] = thread
    thread.start()
    return jsonify({'message': 'Website added successfully'}), 201

@app.route('/websites/<web_id>', methods=['DELETE'])
def remove_website(web_id):
    if int(web_id) not in websites:
        return jsonify({'error': 'Website not found'}), 404
    websites[int(web_id)].stop()
    del websites[int(web_id)]
    return jsonify({'message': 'Website removed successfully'}), 200

@app.route('/websites/<web_id>', methods=['GET'])
def get_website_status(web_id):
    if int(web_id) not in websites:
        return jsonify({'error': 'Website not found'}), 404
    return jsonify({'website': websites[int(web_id)].website, 'status': websites[int(web_id)].status}), 200

@app.route('/websites', methods=['GET'])
def get_all_websites():
    websites_list = []
    for web_id in websites:
        websites_list.append({'id': web_id, 'website': websites[web_id].website, 'status': websites[web_id].status})
    return jsonify({'websites': websites_list}), 200

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=port)
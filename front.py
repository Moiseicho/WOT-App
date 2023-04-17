import tkinter as tk
import webbrowser
import random
import datetime
import time
import requests

class App():
    # Define function to open web browser
    def open_url(self, event):
        index = self.listbox.curselection()[0]
        website = self.listbox.get(index).split(' Last update: ')[0]
        self.updateSingle(index)
        webbrowser.open_new_tab(website)

    def updateSingle(self, index):
        isDown = self.websites[website_id]['status'] == 'DOWN'
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.listbox.delete(index)
        self.listbox.insert(index, website + " Last update: " + current_time)
        self.listbox.itemconfigure(index, bg='#ed736d' if isDown else '#6ded73')

    def update(self):
        response = requests.get('http://localhost:5000/websites').json().get('websites')
        for website in response:
            self.websites[website['id']] = {'website': website['website'], 'status': website['status']}
        
        for index in range(len(self.websites)):
            self.updateSingle(index)

    def add_website(self):
        website = self.add_url_entry.get()
        status = self.status_var.get()
        response = requests.post('http://localhost:5000/websites', json={'website': website, 'status_code': int(status)}).json()
        self.update()
        
    def __init__(self):
        self.websites = {}

        response = requests.get('http://localhost:5000/websites').json().get('websites')
        for website in response:
            self.websites[website['id']] = {'website': website['website'], 'status': website['status']}
        
        # Create Tkinter window
        self.window = tk.Tk()
        self.window.title("List of Websites")
        self.window.configure(bg='#FFF5C7')

        # Create frame for adding new websites
        add_frame = tk.Frame(self.window)
        add_frame.pack(padx=10, pady=10)

        tk.Label(add_frame, text="Add Website URL: ").grid(row=0, column=0, padx=5, pady=5)
        self.add_url_entry = tk.Entry(add_frame)
        self.add_url_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Expected Status: ").grid(row=1, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("000")
        self.status_entry = tk.Entry(add_frame, textvariable=self.status_var)
        self.status_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(add_frame, text="Add", command=self.add_website)
        self.add_button.grid(row=2, column=1, padx=5, pady=5)

        # Create listbox widget
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(padx=10, pady=10, expand=True, fill=tk.X)

        height = len(self.websites)
        self.listbox.config(height=height)
        index = 0
        for website in self.websites:
            # Check if the website is online - KRUMAK and put it in a variable
            isDown = self.websites[website]['status'] == 'DOWN'
            index += 1
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            self.listbox.insert(tk.END, self.websites[website]['website'] + " Last update: " + current_time)
            self.listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')


        self.text = tk.Text(self.window)
        self.text.pack(padx=10, pady=10, expand=True, fill=tk.Y)

        with open('LOG.txt', 'r') as file:

            content = file.read()
            
            self.text.delete('0.1', tk.END)
            self.text.insert(tk.END, content)

        self.button = tk.Button(self.window, text="Update", command=self.update)
        self.button.pack()

        # Bind function to <<ListboxSelect>> event
        self.listbox.bind("<<ListboxSelect>>", self.open_url)
        # Run Tkinter event loop

        
        
    def run(self):
        self.window.mainloop()
        
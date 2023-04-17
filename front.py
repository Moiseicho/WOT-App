import tkinter as tk
import webbrowser
import random
import datetime
import WebsiteChecker
import time

class App():
    # Define function to open web browser
    def open_url(self, event):
        index = self.listbox.curselection()[0]
        website = self.listbox.get(index).split(' Last update: ')[0]
        self.updateSingle(index)
        webbrowser.open_new_tab(website)

    def updateSingle(self, index):
        
        for counter in range(self.listbox.size()):
            if counter == index:
                
                isDown = "DOWN" # Add the stuff here
                now = datetime.datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                website = self.listbox.get(0).split(' Last update: ')[0]
                self.listbox.delete(0)
                self.listbox.insert(tk.END, website + ' Last update: ' + current_time)
                self.listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')
            else:
                tempText = self.listbox.get(0)
                color = self.listbox.itemcget(0, 'bg')
                self.listbox.delete(0)
                self.listbox.insert(tk.END, tempText)
                self.listbox.itemconfigure(tk.END, bg=color)
                

    def update(self):
        for counter in range(self.listbox.size()):
            
            isDown = "DOWN" # Add stuff here
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            website = self.listbox.get(0).split(' Last update: ')[0]
            self.listbox.delete(0)
            self.listbox.insert(tk.END, website + ' Last update: ' + current_time)
            self.listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')
        with open('LOG.txt', 'r') as file:

            # Read the contents of the file
            content = file.read()
            
            self.text.delete('0.1', tk.END)
            self.text.insert(tk.END, content)
    def __init__(self):
        self.websites = {"https://www.google.com/",
                    "https://slay.one/",
                    "https://www.example.com/michael",
                    "https://www.example.com/sarah",
                    "https://www.example.com/david"}

        # Create Tkinter window
        self.window = tk.Tk()
        self.window.title("List of Websites")
        self.window.configure(bg='#FFF5C7')

        # Create listbox widget
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(padx=10, pady=10, expand=True, fill=tk.X)

        height = len(self.websites)
        self.listbox.config(height=height)
        index = 0
        for website in self.websites:
            # Check if the website is online - KRUMAK and put it in a variable
            isDown ="DOWN" # Add stuff here
            index += 1
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            self.listbox.insert(tk.END, website + " Last update: " + current_time)
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
        
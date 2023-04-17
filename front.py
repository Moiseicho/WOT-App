import tkinter as tk
import webbrowser
import random
import datetime


# Define function to open web browser
def open_url(event):
    index = listbox.curselection()[0]
    website = listbox.get(index)
    updateSinge(index)
    #webbrowser.open_new_tab(website)

def updateSinge(index):
    
    for counter in range(listbox.size()):
        if counter == index:
            # Check if the website is online - KRUMAK and put it in a variable
            isDown = random.choice([True, False])
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            website = listbox.get(0).split(' Last update: ')[0]
            listbox.delete(0)
            listbox.insert(tk.END, website + ' Last update: ' + current_time)
            listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')
        else:
            tempText = listbox.get(0)
            color = listbox.itemcget(0, 'bg')
            listbox.delete(0)
            listbox.insert(tk.END, tempText)
            listbox.itemconfigure(tk.END, bg=color)
            

def update():
    for counter in range(listbox.size()):
        # Check if the website is online - KRUMAK and put it in a variable
        isDown = random.choice([True, False])
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        website = listbox.get(0).split(' Last update: ')[0]
        listbox.delete(0)
        listbox.insert(tk.END, website + ' Last update: ' + current_time)
        listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')
    with open('LOG.txt', 'r') as file:

        # Read the contents of the file
        content = file.read()
        
        text.delete('0.1', tk.END)
        text.insert(tk.END, content)

websites = {"https://www.example.com/john",
            "https://www.example.com/jane",
            "https://www.example.com/michael",
            "https://www.example.com/sarah",
            "https://www.example.com/david"}

# Create Tkinter window
window = tk.Tk()
window.title("List of Websites")
window.configure(bg='#FFF5C7')

# Create listbox widget
listbox = tk.Listbox(window)
listbox.pack(padx=10, pady=10, expand=True, fill=tk.X)

height = len(websites)
listbox.config(height=height)


for website in websites:
    # Check if the website is online - KRUMAK and put it in a variable
    isDown = random.choice([True, False])
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    listbox.insert(tk.END, website + " Last update: " + current_time)
    listbox.itemconfigure(tk.END, bg='#ed736d' if isDown else '#6ded73')


text = tk.Text(window)
text.pack(padx=10, pady=10, expand=True, fill=tk.Y)

with open('LOG.txt', 'r') as file:

    # Read the contents of the file
    content = file.read()
    
    text.insert(tk.END, content)

button = tk.Button(window, text="Update", command=update)
button.pack()

# Bind function to <<ListboxSelect>> event
listbox.bind("<<ListboxSelect>>", open_url)
# Run Tkinter event loop
window.mainloop()
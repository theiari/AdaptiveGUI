import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image #EXTRA LIBRARY --> pip install pillow
import json

LARGEFONT = ("Verdana", 24)

class ServiceStatePage(tk.Frame):
    
    config_file = ''
    global background_image
    labels = [] # boxes corresonds to a collection of labels, each one inside a frame
    service_map = {}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.option_add("*Font","aerial")

        self.controller = controller

        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19))

        def disruptionHandler():
            highlighted_value = self.comboBox.get() #return the selected value
            temp : tk.Label
            temp = self.labels[int(highlighted_value) -1]
            temp.config(background= "red")

        self.grid_columnconfigure(0, weight=0)
        self.rightFrame = tk.Frame(self, width= 400, height= 100)
        
        buttonsFrame = tk.Frame(self.rightFrame)
        buttonsFrame.grid(column=0, row = 5, pady=30)

        self.rightFrame.pack(side = "right", padx= 50)
        
        self.backgroundFrame = tk.Frame(self, width= 1400)
        
        servicesLabel = ttk.Label(self.backgroundFrame , text= "Services" , font= LARGEFONT)
        servicesLabel.pack(side= "top")

        self.backgroundFrame.pack(side= "left", padx= 50)

        self.servicesLabel = ttk.Label(self.rightFrame, text= "Execution plan", font= LARGEFONT)
        self.servicesLabel.grid(row= 0, column= 0)

        self.listBox = tk.Listbox(self.rightFrame, width= 25, height= 15, font= ('arial',14))
        self.listBox.grid(column= 0, row= 1)

        self.comboBox = ttk.Combobox(self.rightFrame,width= 25, height= 15, font= ('arial',14), state= "readonly") #readonly avoid the user from entering values arbitarily
        self.comboBox.grid(column= 0, row= 2, pady=30)

        # Button to go back to the start page
        disruptionButton = ttk.Button(self.rightFrame, text="Send disruption", command=disruptionHandler, style= 'CustomButton.TButton', width= 20)
        disruptionButton.grid(row=3, column=0, padx=10, pady=10)

        homeButton = ttk.Button(buttonsFrame, text="Home", command=lambda: controller.show_mainPage(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)
        startButton = ttk.Button(buttonsFrame, text="Start", command= self.start, style= 'CustomButton.TButton') #no action
        startButton.grid(row=1, column=1, padx=10, pady=10)
        refreshButton = ttk.Button(self.rightFrame, text="refresh states", command='', style= 'CustomButton.TButton', width= 20) #debug button to reset background to green
        refreshButton .grid(row=4, column=0, padx=10, pady=10)

    
    def start(self):
        if any(box.cget("background") == "red" for box in self.labels):
            msgbox.showerror("Error", "Some processes are not working")
        else:
            msgbox.showinfo("All good", "Hurray!")


    def set_image_services(self):
        # Read the JSON file
        with open(self.config_file) as json_file:
            data = json.load(json_file)
    
        # JSON attributes loading
        services = data['services']
        self.image_path = f"utils/{data['image_path']}"
        self.folder = data['folder']
        
        self.matrix = [data['matrix'][key] for key in ['rows', 'columns']]

        print("this is the matrix: ")
        print(self.matrix)

        service_map = {}
        # Iterate over the services and extract relevant information
        for service in services:
            nome_file = service['name_file']
            x = service['x']
            y = service['y']
            label = service['label']

            #ALTERNATIVE SERVICE MAP KEY_VALUE PAIR
            service_map[label] = (x,y,nome_file)

        self.service_map = service_map
        
        positions = list(self.service_map.values())
        data = list(self.service_map.keys())

        self.background_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((1200,900)))
        self.background_image_label = tk.Label(self.backgroundFrame, image= self.background_image)
        self.background_image_label.pack()

        num_elements = self.matrix[0] * self.matrix[1]

        # Create frames for each cell
        frames = []
               
        covered_indexes = []
        j = 0
        
        for i in range(num_elements):  # Create required number of boxes based on matrix dimensions
            frame = tk.Frame(self.background_image_label, width=120, height=120, borderwidth=1, relief="raised", padx= 5 , pady= 35)
            frame.grid(row=i // self.matrix[1], column=i % self.matrix[1])  # Adjust the column value to change the number of columns
            frames.append(frame)
            label = tk.Label(frame,text= '')
            label.pack()
            self.labels.append(label)

        for position in positions:
            index = position[0] * self.matrix[1] + position[1]  # Calculate the corresponding index for the frame

            if index < len(frames):
                frame : tk.Frame  = frames[index]
                label : tk.Label = self.labels[index]
                label.config(text= data[j])  # right now it rewrite the text showing service label
                covered_indexes.append(index)  # Add the covered index to the list, just a debug stuff for now, probably useless soon
            else:
                frame = frames[index]
                label = tk.Label(frame, text=" ")
                
            label.pack() 
            j= j+1


    def refreshComboBox(self): #very ugly way to update items in the listbox
        data = list(self.service_map.keys())
        #self.listBox.delete(0, END)
        self.comboBox['values'] = data
        self.comboBox.current(0) #load the first file, instead of showin a blank selection
        #for file in data:
        #    self.listBox.insert(END,str(file))
import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image #EXTRA LIBRARY --> pip install pillow
import json
from local.aida_utils import AIDAUtils
import time
import subprocess
import asyncio
from constants import *
import signal


class ServiceStatePage(tk.Frame):
    
    config_file = ''
    labels = [] # boxes corresonds to a collection of labels, each one inside a frame
    service_map = {}
    service_map_rectangle = {}
    background_canvas = None


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        style = ttk.Style()
        style.configure('CustomButton.TButton', font=MEDIUMFONT)

        def disruptionHandler():
            highlighted_value = self.comboBox.get() #return the selected value
            self.change_rect_red(highlighted_value)

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

        self.serviceslistBox = tk.Listbox(self.rightFrame, width= 60, height= 20, font= XSMALLFONT)
        self.serviceslistBox.grid(column= 0, row= 1)

        self.comboBox = ttk.Combobox(self.rightFrame,width= 25, height= 15, font= SMALLFONT, state= "readonly") #readonly avoid the user from entering values arbitarily
        self.comboBox.grid(column= 0, row= 2, pady=30)

        disruptionButton = ttk.Button(self.rightFrame, text="Send disruption", command=disruptionHandler, style= 'CustomButton.TButton', width= 20)
        disruptionButton.grid(row=3, column=0, padx=10, pady=10)

        homeButton = ttk.Button(buttonsFrame, text="Home", command=lambda: controller.show_mainPage(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)

        self.startButton = ttk.Button(buttonsFrame, text="Start", command= self.start, style= 'CustomButton.TButton') #no action
        self.startButton.grid(row=1, column=1, padx=10, pady=10)
        
        self.nextButton = ttk.Button(buttonsFrame, text="Next", command=self.next , style= 'CustomButton.TButton', state="disabled") #debug button to reset background to green
        self.nextButton.grid(row=4, column=0, padx=10, pady=10)

        self.killButton = ttk.Button(buttonsFrame, text="Kill", command=self.kill, style= 'CustomButton.TButton', state="disabled") #debug button to reset background to green
        self.killButton.grid(row=4, column=1, padx=10, pady=10)

    
    def start(self):
        config_json = json.load(open(self.config_file))
        folder = config_json['folder']
        mode = config_json['mode']
        target_file = config_json['target_file']

        app_path = "../local/IndustrialAPI/app.py"
        self.p1 = subprocess.Popen([f"xterm -e python {app_path}"], shell=True, preexec_fn=os.setsid)

        time.sleep(1)

        launch_devices_path = "../local/IndustrialAPI/launch_devices.py"
        self.p2 = subprocess.Popen([f"xterm -e python {launch_devices_path} {folder} {mode}"], shell=True)

        time.sleep(3)

        target = os.path.abspath(f"{folder}/{target_file}")
        self.aida = AIDAUtils(target)

        asyncio.get_event_loop().run_until_complete(self.aida.compute_policy())

        self.startButton.config(state= "disabled")
        self.nextButton.config(state= "normal")
        self.killButton.config(state= "normal")


    async def _next(self):
        service, state, executed_action, finished = await self.aida.next_step()
        if state == "broken":
            self.change_rect_red(service)
        elif state != "broken" and state != "normal":
            self.change_rect_orange(service)
        self.serviceslistBox.insert(END, f"{service} : {executed_action} - {state}")
        if finished:
            msgbox.showinfo("Execution completed!", "Execution completed!")
            self.startButton.config(state= "normal")
            self.nextButton.config(state= "disabled")
            self.killButton.config(state= "disabled")
            self.kill()

    
    def next(self):
        asyncio.get_event_loop().run_until_complete(self._next())


    def kill(self):
        print("Stopping...")
        os.killpg(os.getpgid(self.p1.pid), signal.SIGTERM)
        #os.killpg(os.getpgid(self.p2.pid), signal.SIGTERM)
        self.startButton.config(state= "normal")
        self.nextButton.config(state= "disabled")
        self.killButton.config(state= "disabled")


    def refreshComboBox(self): #very ugly way to update items in the listbox
        data = list(self.service_map.keys())
        self.comboBox['values'] = data
        self.comboBox.current(0)


    def set_image_services(self):
        # Read the JSON file
        with open(self.config_file) as json_file:
            data = json.load(json_file)
    
        # JSON attributes loading
        services = data['services']
        self.image_path = f"utils/{data['image_path']}"
        self.folder = data['folder']
        
        self.matrix = [data['matrix'][key] for key in ['rows', 'columns']]

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
        
        data = list(self.service_map.keys())

        self.background_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((1200,900)))
        #self.background_image_label = tk.Label(self.backgroundFrame, image= self.background_image)
        self.background_canvas = tk.Canvas(self.backgroundFrame, width=1200, height=900)
        self.background_canvas.create_image(0,0, anchor=tk.NW, image=self.background_image)
        self.background_canvas.pack()
        
        step_x = 1200 / self.matrix[1]
        step_y = 900 / self.matrix[0]
        
        for service_label in self.service_map.keys():
            y = self.service_map[service_label][0]
            x = self.service_map[service_label][1]
            x1 = x * step_x
            if x1 == 0: x1 +=1
            y1 = y * step_y
            if y1 == 0: y1 +=1
            rectangle = self.background_canvas.create_rectangle(x1, y1, x1+step_x, y1+step_y, fill="green", stipple="gray50", outline="black")
            self.background_canvas.create_text(x1+step_x/2, y1+step_y/2, text=service_label, font=SERVICE_FONT)
            self.service_map_rectangle[service_label] = rectangle
      
    
    def change_rect_red(self, service_label):
        self.background_canvas.itemconfig(self.service_map_rectangle[service_label], fill="red", stipple="gray50", outline="black")
        

    def change_rect_orange(self, service_label):
        self.background_canvas.itemconfig(self.service_map_rectangle[service_label], fill="orange", stipple="gray50", outline="black")


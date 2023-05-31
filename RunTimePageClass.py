import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox as msgbox
import json
import glob

LARGEFONT = ("Verdana", 24)

class RunTimePage(tk.Frame):

    config_file = ''
    
    def __init__(self, parent, controller):    
        
        def execute():
            if (len(self.targetsListBox.get_children())):
                controller.show_testPage()
            else:
                msgbox.showerror("check your files", "Please, check the .tdl file and try again.")
                self.controller.show_mainPage()
        
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19)) 

        self.controller = controller

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        
        buttonFrame = tk.Frame(self)

        homeButton = ttk.Button(buttonFrame, text ="Home",
                            command = lambda : controller.show_mainPage(), style='CustomButton.TButton')
        homeButton.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        exectueButton = ttk.Button(buttonFrame, text= "EXECUTE", command= execute, style='CustomButton.TButton')
        exectueButton.grid(row= 0, column= 1, padx= 10, pady= 10)

        buttonFrame.grid(column=0, row= 5, pady= 50)
        
        servicesLabel = ttk.Label (self, text = "SERVICES:")
        servicesLabel.grid(row =1, column=0, pady= 50)

        targetsLabel = ttk.Label ( self, text= "TARGETS:")
        targetsLabel.grid(row = 3, column= 0, pady=10)

        self.servicesListBox = ttk.Treeview(self, height=12, columns=("Name", "Validity"), show='headings', padding= 5)
        self.servicesListBox.grid(row = 2, column= 0, padx= 15, pady= 2)
        
        self.targetsListBox = ttk.Treeview(self, height=2, columns=("Name", "Validity") , show='headings', padding= 5)
        self.targetsListBox.grid(row = 4, column= 0, padx= 15, pady=20)


    def set_files(self):
        if self.config_file == "":
            msgbox.showerror("File config", "You need to select a config file.")
            self.controller.show_mainPage()
            return

        with open(self.config_file) as json_file:
            data = json.load(json_file)

        folder_name = data["folder"]
        
        self.setColumnsNames(self.servicesListBox)
        self.setColumnsNames(self.targetsListBox)

        self.loadListBoxs(folder_name)


    def loadListBoxs(self, folder_name):
        service_list = [file for file in os.listdir(folder_name) if file.endswith(".sdl")] 
        target_list = [file for file in os.listdir(folder_name) if file.endswith(".tdl")]
        
        for file in service_list:
            self.servicesListBox.insert('', 'end', text="0", values=(str(file), 'ok!')) #for now, the validity is not implemented, it just shows ok for everyone
        for file in target_list:
            self.targetsListBox.insert('', 'end', text="0", values=( str(file), 'ok!'))# validity is not implemented yet


    def setColumnsNames(self, listBox): #This method create headings names, and change text size to be bigger
        style1 = ttk.Style()
        style1.configure("Treeview.Heading", font=(None, 22), ) #changing heading text size
        style1.configure("Treeview", font=(None, 16), rowheight = 20) #changing elements text size

        listBox.column( "#1", anchor= "center" , width = 400)
        listBox.heading("#1", text="Name")
        listBox.column( "#2", anchor= "center", width = 200)
        listBox.heading("#2", text="Validity")

    
    def check_files_config(self):
        if self.config_file == "":
            msgbox.showerror("File config", "You need to select a config file.")
            print("1")
            self.controller.show_mainPage()
            return

        with open(self.config_file) as json_file:
            data = json.load(json_file)

        folder_name = data["folder"]
        services = [service["name_file"] for service in data["services"]]

        files = glob.glob(f"{folder_name}/*.sdl") + glob.glob(f'{folder_name}/*.tdl')
        print(files)

        for f in files:
            service_name = f.split("/")[-1]
            if service_name not in services:
                # ERROR
                msgbox.showerror("check your files", "Please, check the files in folder and try again. They are not coherent with the config file.")
                print("1")
                self.controller.show_mainPage()
                break

from tkinter import ttk
import tkinter as tk
from ServiceStatePageClass import ServiceStatePage
from RunTimePageClass import RunTimePage
from InstancePlanningPageClass import InstancePlanningPage
from StochasticPolicyPage import StochasticPolicyPage
from StochasticConstraintsBasedPolicy import StochasticConstraintsBasedPolicy
from tkinter import filedialog
from tkinter import Text
from tkinter import END
import tkinter.messagebox as msgbox
import os
import tkinter.font as font
import json
import tkinter as tk
from constants import *


class tkinterApp(tk.Tk):
    
    #JSON stuff
    service_map = {} #services map of JSON file, is a map/dictionary <Key,Value> ==> <service.nome_file,[service.x, service.y, service.label], for all service in services. Pure projectual choice, I guess it could be approached differently...
    matrix = [] #is a vector with two elements [number_of_rows, number_of_columns]
    image_path= ''
    folder = '' #is the folder used to load all the .sdl and .tdl files, in runtimepage ( BEFORE entering in the ServiceStatePage)

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        self.geometry("1920x1080")
        container = tk.Frame(self)
        self.title("Adaptive Software")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #container.grid(side = "top", fill = "both", expand = True)
        container.grid(row=0, column=0, sticky= "nsew")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
        # iterating through a tuple consisting of the different page layouts
        for F in (StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage):
            frame = F(container, self)
            
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.show_frame(StartPage) #THIS CALL WILL LOAD THE FIRST PAGE, IT ACCEPTS THIS CLASSES : StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage)
        
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    

    #getter for JSON attributes
    def getFrame(self, cont):
        return self.frames[cont]
    

    def show_mainPage(self):
        frame = self.frames[StartPage]
        frame.tkraise()
    
    
    def show_testPage(self):
        frame = self.frames[ServiceStatePage] 
        frame.tkraise()
    

    def getMatrix(self):
        return self.matrix
    

    def getImage_path(self):
        return self.image_path
    

    def getFolder(self):
        return self.folder


    def getServicesMap(self):
        return self.service_map


    #This method check the selected radio button and call showframe function
    def checkRadio(self, temp, radioStatus ,controller):
        if radioStatus.get() == 2: #if RunTime RadioButton has been selected 
            self.show_frame(RunTimePage) #tell show_frame to load runTimePage
            global config_file
            config_file = filedialog.askopenfilename(
                title="Select the config file",
                initialdir="./config_files"
            )
            if not config_file:
                msgbox.showerror("Error", "Please select a file")
                self.show_frame(RunTimePage)
                return
            config_json = json.load(open(config_file))
            folder = config_json['folder']
            if not os.path.isdir(folder):
                msgbox.showerror("Error", "The folder specified in the config file does not exist")
                controller.show_mainPage()
                return
            
            temp = self.getFrame(RunTimePage)
            temp.config_file = str(config_file)
            #temp.check_files_config()
            temp.set_files()

            temp = self.getFrame(ServiceStatePage)
            temp.config_file = str(config_file)
            temp.set_image_services()
            temp.refreshComboBox()
        else:                      #DesignTime RadioButton has been selected
            self.show_frame(temp)
            global file
            folder = filedialog.askdirectory(
                title='Select the folder', #name of the tab
                initialdir="./", #initial shown directory
            )
            if not folder:
                msgbox.showerror("Error", "Please select a folder")
                return
            try:
                os.mkdir(folder)
            except:
                print()
            temp = self.getFrame(temp) #retrive the frame instance, otherwise it uses the generic class 
            temp.path = str(folder)
            temp.refreshListBox(controller)          


    def loadJson(self, mode):
        # Read the JSON file
        with open(f"config_files/config_layout_{mode}.json") as json_file:
            data = json.load(json_file)
    
        # JSON attributes loading
        services = data['services']
        self.image_path = f"utils/{data['image_path']}"
        self.folder = data['folder']
        
        self.matrix = [data['matrix'][key] for key in ['rows', 'columns']]

        print("this is the matrix: ")
        print(self.matrix)

        # Iterate over the services and extract relevant information
        for service in services:
            nome_file = service['nome_file']
            x=  service['x']
            y = service['y']
            label = service['label']

            #ALTERNATIVE SERVICE MAP KEY_VALUE PAIR
            self.service_map[label] = (x,y,nome_file)


# first window frame startpage  --START PAGE--
class StartPage(tk.Frame):
    def __init__(self, parent, controller : tkinterApp):
        
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.option_add("*Font","aerial") #change font size 
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=MEDIUMFONT) 
    
        # label of frame
        label = ttk.Label(self, text ="Adaptive 0.2", font = LARGEFONT)
        label.grid(row = 0, column =0, padx = 10, pady = 10)
  
        # button planning
        button1 = ttk.Button(self, text ="Instance planning",
            command = lambda : controller.checkRadio(InstancePlanningPage, selected_value, controller),
            style='CustomButton.TButton',
            width= 30
        )
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)
  
        # button stochastic policy
        button2 = ttk.Button(self, text ="Stochastic policy",
            command = lambda : controller.checkRadio(StochasticPolicyPage, selected_value, controller),
            style='CustomButton.TButton',
            width= 30
        )
        button2.grid(row = 2, column = 0, padx = 10, pady = 10)
  
        # button stochastic constraint-based policy
        button3 = ttk.Button(self, text ="Stochastic constraint-based policy",
            command = lambda : controller.checkRadio(StochasticConstraintsBasedPolicy, selected_value, controller),
            style='CustomButton.TButton',
            width= 30
        )
        button3.grid(row = 3, column = 0, padx = 10, pady = 10)

        selected_value = tk.IntVar()
        style.configure('TRadiobutton', font=MEDIUMFONT)
        designTime = ttk.Radiobutton(
            self,
            text='Design Time',
            value=1,
            variable=selected_value,
            style= 'TRadiobutton'
        )  
        designTime.grid(row = 4, column = 0, padx = 5)
        designTime.invoke() # highlights the first radio button, without it there would be the two buttons blank

        runTime = ttk.Radiobutton(
            self,
            text='Run Time',
            value=2, #Value 2 is related to runtime
            variable=selected_value,
            style= 'TRadiobutton'
        )
        runTime.grid(row = 5, column = 0, padx = 5)

        def setLabel(self, labelName):
            label.config(text= labelName)



#this one will be useful for the runtime section
def loadFile(): #select the file from os explorer and return its directory as string type, PROBABLY NOT USEFUL, BUT I KEEP IT HERE FOR NOW
    filetypes = (
        ('text files', '*.txt'), # this is just for debug, eventually will be deleted
        ('service description language', '*.sdl'),
        ('target description language', '*.tdl')
    )
    global file
    file = filedialog.askopenfilename(
        title='Select the file', #name of the tab
        initialdir=".", #initial shown directory
        filetypes= filetypes) #filters types of file can be selected
    return file


# Driver Code
app = tkinterApp() ##app corresponds to the object app, its attributes are: 
app.mainloop()
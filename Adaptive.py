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
import InstancePlanningPageClass
#import TestPage

LARGEFONT =("Verdana", 28)


class tkinterApp(tk.Tk):
    
    #This method check the selected radio button and call showframe function
    def checkRadio(self, temp , radioStatus):
        # if temp == Page1 and radioStatus.get()== 1:
        #    self.show_frame(Page1)
        # if temp == Page1 and radioStatus.get() == 2:
        #    self.show_frame(RunTimePage) 
        if radioStatus.get() == 2: #if RunTime RadioButton has been selected 
            self.show_frame(RunTimePage) #tell show_frame to load runTimePage
        else:                       #nothing fancy to see here
        
            self.show_frame(temp) 
            global file
            file = filedialog.askdirectory(
            title='Select the file', #name of the tab
            initialdir="C:/Users/anton/OneDrive/Documenti/Software Engineering/Fellowship/Adaptive", #initial shown directory
            )
            
            temp = self.getFrame(temp) #retrive the frame instance, otherwise it uses the generic class 
            print(temp.path)
            temp.path = str(file)
            print(temp.path)
            temp.refreshListBox()
            #temp.loadPath()
            #print ( "debug = "+ str(temp.path))
            

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
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage):
       
            
            frame = F(container, self)
            
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.show_frame(StartPage) #THIS CALL WILL LOAD THE FIRST PAGE, IT ACCEPTS THIS CLASSES : StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage)
        
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def getFrame(self, cont):
        return self.frames[cont]
    
    def show_mainPage(self):
        frame = self.frames[StartPage] 
        frame.tkraise()
    def show_testPage(self):
        frame = self.frames[ServiceStatePage] 
        frame.tkraise()
# first window frame startpage  --START PAGE--
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.option_add("*Font","aerial") #change font size 
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 18)) 
       
    
        # label of frame Layout 2
        label = ttk.Label(self, text ="Adaptive 0.2", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column =0, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Instance planning",
        command = lambda : controller.checkRadio(InstancePlanningPage,selected_value),
        style='CustomButton.TButton',
        width= 30
        )
        #print(str(button1.winfo_reqwidth()))
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Stochastic policy",
        command = lambda : controller.checkRadio(StochasticPolicyPage,selected_value),
        style='CustomButton.TButton',
        width= 30)
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 0, padx = 10, pady = 10)
  
        button3 = ttk.Button(self, text ="Stochastic constraint-based policy",
        command = lambda : controller.checkRadio(StochasticConstraintsBasedPolicy,selected_value),
        style='CustomButton.TButton',
        width= 30)

        button3.grid(row = 3, column = 0, padx = 10, pady = 10)

        selected_value = tk.IntVar()
        style.configure('TRadiobutton', font=('Arial', 21)) 
        designTime = ttk.Radiobutton(
            self,
            text='Design Time',
            value=1,
            variable=selected_value,
            style= 'TRadiobutton'
        )  
        designTime.grid(row = 4, column = 0, padx = 5)
        
        designTime.invoke() #highlights the first radio button, without it there would be the two buttons blank

        runTime = ttk.Radiobutton(
            self,
            text='Run Time',
            value=2, #Value 2 is related to runtime
            variable=selected_value,
            
        )
        runTime.grid(row = 5, column = 0, padx = 5)
    

        label1 = ttk.Label(self, textvariable = selected_value)
        
        #label1.grid(row = 6, column = 1) debug test, not mandatory so for now it's not placed in the frame

        button4 = ttk.Button(self, text ="paginaTest", # paginaTest is a class written in another file, used just for testing outer invocation (not working...)
        command = lambda : controller.show_frame(ServiceStatePage))
        #button4.grid(row=7, column = 1) #not placed for now, button4 is indeed debug stuff

        def setLabel(self, labelName):
            label.config(text= labelName)



#this one will be useful for the runtime section
def loadFile(): #select the file from os explorer and return its directory as string type, PROBABLY NOT USEFUL, BUT I KEEP IT HERE FOR NOW
    filetypes  = (
        ('text files', '*.txt'), # this is just for debug, eventually will be deleted
        ('service description language', '*.sdl'),
        ('target description language', '*.tdl')
    )
    global file
    file = filedialog.askopenfilename(
        title='Select the file', #name of the tab
        initialdir="C:/Users/anton/OneDrive/Documenti/Software Engineering/Fellowship/Adaptive", #initial shown directory
        filetypes= filetypes) #filters types of file can be selected
    return file


# Driver Code
app = tkinterApp() ##app corresponds to the object app, its attributes are: 
app.mainloop()
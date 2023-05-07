from tkinter import ttk
import tkinter as tk
from TestPageProva import TestPage
from tkinter import filedialog
from tkinter import Text
from tkinter import END
import tkinter.messagebox as msgbox
import os
#import TestPage

LARGEFONT =("Verdana", 24)
  
class tkinterApp(tk.Tk):

    #This method check the selected radio button and call showframe function
    def checkRadio(self, temp, radioStatus):
        # if temp == Page1 and radioStatus.get()== 1:
        #    self.show_frame(Page1)
        # if temp == Page1 and radioStatus.get() == 2:
        #    self.show_frame(RunTimePage) 
        if radioStatus.get() == 2: #if RunTime RadioButton has been selected 
            self.show_frame(RunTimePage) #tell show_frame to load runTimePage
        else:                       #nothing fancy to see here
            self.show_frame(temp) 

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self, height=400, width=1200) 
        self.title("Adaptive Software")
        #container.grid(side = "top", fill = "both", expand = True)
        container.grid(row=1, column=0)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, TestPage):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
    
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  

# first window frame startpage  --START PAGE--
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Adaptive 0.1", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        button1 = ttk.Button(self, text ="Instance planning",
        command = lambda : controller.checkRadio(InstancePlanningPage,selected_value))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Stochastic policy",
        command = lambda : controller.show_frame(StochasticPolicyPage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
        button3 = ttk.Button(self, text ="Stochastic constraint-based policy",
        command = lambda : controller.show_frame(StochasticConstraintsBasedPolicy))

        button3.grid(row = 3, column = 1, padx = 10, pady = 10)

        selected_value = tk.IntVar()

        designTime = ttk.Radiobutton(
            self,
            text='Design Time',
            value=1,
            variable=selected_value,
            
        )  
        designTime.grid(row = 4, column = 1, padx = 5)
        
        designTime.invoke() #highlights the first radio button, without it there would be the two buttons blank

        runTime = ttk.Radiobutton(
            self,
            text='Run Time',
            value=2, #Value 2 is related to runtime
            variable=selected_value,
        )
        runTime.grid(row = 5, column = 1, padx = 5)
    

        label1 = ttk.Label(self, textvariable = selected_value)
        
        #label1.grid(row = 6, column = 1) debug test, not mandatory so for now it's not placed in the frame

        button4 = ttk.Button(self, text ="paginaTest", # paginaTest is a class written in another file, used just for testing outer invocation (not working...)
        command = lambda : controller.show_frame(TestPage))
        #button4.grid(row=7, column = 1) #not placed for now, button4 is indeed debug stuff

        
            

  
# second window frame --INSTANCE PLANNING--
class InstancePlanningPage(tk.Frame):

    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        def reset():
            inputtxt.delete(1.0, END)
            loadedFileLabel.config(text = "here is the list of all loaded files: \n")
        
        def loadFile() :
             file_list = [file for file in os.listdir() if file.endswith(".txt")] #this is the list of all .txt file in this directory
             

             for file in file_list:
                tempText = loadedFileLabel.cget("text")
                loadedFileLabel.config( text= tempText +' '+str(file)+ '\n' )
                with open(file, "r") as file:
                    content = file.read()
                #inputtxt.insert(END, '\n BEGIN OF FILE: '+file.name +'\n') this can be both useful and annoying
                inputtxt.insert(END, content)
                inputtxt.insert(END, '\n\n')
             #if len(file_list) != 0:
                 #we need to change a label
       
        def preSave():
                info_window = tk.Toplevel()
                info_window.grab_set()
                info_window.title("Save the model")
                info_window.geometry("200x130")
                info_label = tk.Label(info_window, text="Please, select a name for the file")
                info_label.pack(pady=10)
                saveTextBox= tk.Text(info_window, height= 1, width= 12)
                saveTextBox.pack(pady=10)
                close_button = tk.Button(info_window, text="Save", command= lambda : saveFile(info_window, saveTextBox.get(0.0,END).strip() + ".txt") )
                close_button.pack(pady=10)
               

        def saveFile(info_window, filename):
            info_window.destroy()
            info_window.update()

            try:
           
                text_file = open(filename, "x") #the file will be saved as a .txt file, this will need to be changed depending on file extension type
                text_file.write(inputtxt.get(1.0, END)) #the file is saved in the current folder
                text_file.close()
                inputtxt.delete(0.0, END) #textbox is now blank
           #info_window = tk.Toplevel()
                info_window = msgbox.showinfo("Information", "file " +filename+" has been saved!")
            except FileExistsError:
                msgbox.showerror("Error", "A file with this name already exist!")
            


        
        
      
        

        # FRAME DECLARATION & GRID

        #frame placed in the right side of the window
        rightFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 100 , height= 100)
        rightFrame.grid(row = 1, column= 6)
        #frame placed in the top side of the window
        topFrame = tk.Frame(self, width = 200 , height= 30)
        topFrame.grid(row = 0, column= 0 )
        #frame placed in the centre of the window
        centerFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 200 , height= 200)
        centerFrame.grid(row = 1, column= 0 )
        #frame palced at the bottom of the window
        bottomFrame = tk.Frame(self, width = 200 , height= 200)
        bottomFrame.grid(row = 8, column= 0 )




        #LABEL & BUTTON DECLARATION & GRID 
 
        resetButton = ttk.Button(bottomFrame, text="RESET", command= reset ) #function to redet the whole design window, has not be implemented yet // TODO
        resetButton.grid(column=0, row=0, padx = 3, pady = 3)
 
 
        #button MODEL used to retrieve .tdl or .sdl files
        modelButton = ttk.Button(bottomFrame, text="MODEL", command= preSave) #function to load a file from local storage, for now just a single one
        modelButton.grid(column=1, row=0, padx = 3, pady = 3)
        
        label = ttk.Label(centerFrame, text ="Instance Planning Design Time", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        
        loadedFileLabel = ttk.Label(rightFrame, text='here is the list of all loaded files: \n')
        loadedFileLabel.grid(row = 1, column= 5, padx= 10)

        startPageButton = ttk.Button(bottomFrame, text ="Home",
                            command = lambda : controller.show_frame(StartPage))   
        startPageButton.grid(row = 0, column = 2, padx = 3, pady = 3)

        modelServiceButton = ttk.Button(topFrame, text = " Service Template ", command= loadFile)
        modelServiceButton.grid(row = 1, column = 0)

        modelTargetButton =  ttk.Button(topFrame, text = " Target Template ", command= loadFile)
        modelTargetButton.grid(row = 1, column = 1)


        inputtxt = tk.Text(centerFrame,
                height = 14,
                width = 60,
                )
        inputtxt.grid(row = 1 , column= 0 )
        global dynamicLabel 
        dynamicLabel = ttk.Label(rightFrame, text = "select some files" ) #this label shows the directory of the selected file
        dynamicLabel.grid(row = 2, column= 6)


   
# second window frame page1  --INSTANCE PLANNING RUNTIME TEST --
class RunTimePage(tk.Frame):
     
    def __init__(self, parent, controller):
        
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Instance planning RUNTIME", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)  
  
# second window frame page2  --STOCHASTIC POLICY--
class StochasticPolicyPage(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)

        def reset():
            inputtxt.delete(1.0, END)
            loadedFileLabel.config(text = "here is the list of all loaded files: \n")
        
        def loadFile() :
             file_list = [file for file in os.listdir() if file.endswith(".txt")] #this is the list of all .txt file in this directory
             

             for file in file_list:
                tempText = loadedFileLabel.cget("text")
                loadedFileLabel.config( text= tempText +' '+str(file)+ '\n' )
                with open(file, "r") as file:
                    content = file.read()
                #inputtxt.insert(END, '\n BEGIN OF FILE: '+file.name +'\n') this can be both useful and annoying
                inputtxt.insert(END, content)
                inputtxt.insert(END, '\n\n')
             #if len(file_list) != 0:
                 #we need to change a label
       
        def preSave():
                info_window = tk.Toplevel()
                info_window.grab_set()
                info_window.title("Save the model")
                info_window.geometry("200x130")
                info_label = tk.Label(info_window, text="Please, select a name for the file")
                info_label.pack(pady=10)
                saveTextBox= tk.Text(info_window, height= 1, width= 12)
                saveTextBox.pack(pady=10)
                close_button = tk.Button(info_window, text="Save", command= lambda : saveFile(info_window, saveTextBox.get(0.0,END).strip() + ".txt") )
                close_button.pack(pady=10)
               

        def saveFile(info_window, filename):
            info_window.destroy()
            info_window.update()

            try:
           
                text_file = open(filename, "x") #the file will be saved as a .txt file, this will need to be changed depending on file extension type
                text_file.write(inputtxt.get(1.0, END)) #the file is saved in the current folder
                text_file.close()
                inputtxt.delete(0.0, END) #textbox is now blank
           #info_window = tk.Toplevel()
                info_window = msgbox.showinfo("Information", "file " +filename+" has been saved!")
            except FileExistsError:
                msgbox.showerror("Error", "A file with this name already exist!")
            

        # FRAME DECLARATION & GRID

        #frame placed in the right side of the window
        rightFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 100 , height= 100)
        rightFrame.grid(row = 1, column= 6)
        #frame placed in the top side of the window
        topFrame = tk.Frame(self, width = 200 , height= 30)
        topFrame.grid(row = 0, column= 0 )
        #frame placed in the centre of the window
        centerFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 200 , height= 200)
        centerFrame.grid(row = 1, column= 0 )
        #frame palced at the bottom of the window
        bottomFrame = tk.Frame(self, width = 200 , height= 200)
        bottomFrame.grid(row = 8, column= 0 )

        inputtxt = tk.Text(centerFrame,
                height = 15,
                width = 60,
                )
        inputtxt.grid(row = 1 , column= 0 )


        #LABEL & BUTTON DECLARATION & GRID 
 
        resetButton = ttk.Button(bottomFrame, text="RESET", command= reset) #function to redet the whole design window, has not be implemented yet // TODO
        resetButton.grid(column=0, row=0, padx = 3, pady = 3)
    
        
 
        #button MODEL used to retrieve .tdl or .sdl files
        modelButton = ttk.Button(bottomFrame, text="MODEL", command= preSave) #function to load a file from local storage, for now just a single one
        modelButton.grid(column=1, row=0, padx = 3, pady = 3)
        
        label = ttk.Label(centerFrame, text ="Stochastic Policy Design Time", font = LARGEFONT)
        label.grid(row = 0, column = 0)


        
        loadedFileLabel = ttk.Label(rightFrame, text='here is the list of all loaded files: \n')
        loadedFileLabel.grid(row = 1, column= 5, padx= 10)


        startPageButton = ttk.Button(bottomFrame, text ="Home",
                            command = lambda : controller.show_frame(StartPage))   
        startPageButton.grid(row = 0, column = 2, padx = 3, pady = 3)

        modelServiceButton = ttk.Button(topFrame, text = " Service Template ", command= loadFile )# no action, WIP
        modelServiceButton.grid(row = 1, column = 0)

        modelTargetButton =  ttk.Button(topFrame, text = " Target Template ",command= loadFile)# no action, WIP
        modelTargetButton.grid(row = 1, column = 1)


       
        global dynamicLabel 
        dynamicLabel = ttk.Label(rightFrame, text = "select some files" ) #this label shows the directory of the selected file
        dynamicLabel.grid(row = 2, column= 6)

  
  # third window frame      --STOCHASTIC CONSTRAINTS-BASED POLICY--
class StochasticConstraintsBasedPolicy(tk.Frame):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        
        
        def reset():
            inputtxt.delete(1.0, END)
            loadedFileLabel.config(text = "here is the list of all loaded files: \n")
        
        def loadFile() :
             file_list = [file for file in os.listdir() if file.endswith(".txt")] #this is the list of all .txt file in this directory
             

             for file in file_list:
                tempText = loadedFileLabel.cget("text")
                loadedFileLabel.config( text= tempText +' '+str(file)+ '\n' )
                with open(file, "r") as file:
                    content = file.read()
                #inputtxt.insert(END, '\n BEGIN OF FILE: '+file.name +'\n') this can be both useful and annoying
                inputtxt.insert(END, content)
                inputtxt.insert(END, '\n\n')
             #if len(file_list) != 0:
                 #we need to change a label
       
        def preSave():
                info_window = tk.Toplevel()
                info_window.grab_set()
                info_window.title("Save the model")
                info_window.geometry("200x130")
                info_label = tk.Label(info_window, text="Please, select a name for the file")
                info_label.pack(pady=10)
                saveTextBox= tk.Text(info_window, height= 1, width= 12)
                saveTextBox.pack(pady=10)
                close_button = tk.Button(info_window, text="Save", command= lambda : saveFile(info_window, saveTextBox.get(0.0,END).strip() + ".txt") )
                close_button.pack(pady=10)
        
                
        
               

        def saveFile(info_window, filename):
            info_window.destroy()
            info_window.update()

            try:
           
                text_file = open(filename, "x") #the file will be saved as a .txt file, this will need to be changed depending on file extension type
                text_file.write(inputtxt.get(1.0, END)) #the file is saved in the current folder
                text_file.close()
                inputtxt.delete(0.0, END) #textbox is now blank
           #info_window = tk.Toplevel()
                info_window = msgbox.showinfo("Information", "file " +filename+" has been saved!")
            except FileExistsError:
                msgbox.showerror("Error", "A file with this name already exist!")
            
           #info_window.title("Information")
           #info_window.geometry("200x100")
           

        # FRAME DECLARATION & GRID

        #frame placed in the right side of the window
        rightFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 100 , height= 100)
        rightFrame.grid(row = 1, column= 6)
        #frame placed in the top side of the window
        topFrame = tk.Frame(self, width = 200 , height= 30)
        topFrame.grid(row = 0, column= 0 )
        #frame placed in the centre of the window
        centerFrame = tk.Frame(self,  highlightbackground= 'black', highlightthickness = 0.75, width = 200 , height= 200)
        centerFrame.grid(row = 1, column= 0 )
        #frame palced at the bottom of the window
        bottomFrame = tk.Frame(self, width = 200 , height= 200)
        bottomFrame.grid(row = 8, column= 0 )




        #LABEL & BUTTON DECLARATION & GRID 
 
        resetButton = ttk.Button(bottomFrame, text="RESET", command= reset ) #function to redet the whole design window, has not be implemented yet // TODO
        resetButton.grid(column=0, row=0, padx = 3, pady = 3)
 
        #model button should load the file
        #button MODEL used to retrieve .tdl or .sdl files
        modelButton = ttk.Button(bottomFrame, text="MODEL", command= preSave ) #function to load a file from local storage, for now just a single one
        modelButton.grid(column=1, row=0, padx = 3, pady = 3)

        modelButtonLoad= ttk.Button(bottomFrame, text="load", command= loadFile ) #not sure if this is essential, for now I'll just leave it here
        modelButtonLoad.grid(column=5, row=0, padx = 3, pady = 3)               #it does the same action as Service/Target Template, for now.

        label = ttk.Label(centerFrame, text ="Stochastic Constraints-based Policy Design Time", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        loadedFileLabel = ttk.Label(rightFrame, text='here is the list of all loaded files: \n')
        loadedFileLabel.grid(row = 1, column= 5, padx= 10)
        startPageButton = ttk.Button(bottomFrame, text ="Home",
                            command = lambda : controller.show_frame(StartPage))   
        startPageButton.grid(row = 0, column = 2, padx = 3, pady = 3)

        modelServiceButton = ttk.Button(topFrame, text = " Service Template ", command= loadFile)# no action, WIP
        modelServiceButton.grid(row = 1, column = 0)

        modelTargetButton =  ttk.Button(topFrame, text = " Target Template ", command= loadFile)# no action, WIP
        modelTargetButton.grid(row = 1, column = 1)


        inputtxt = tk.Text(centerFrame,
                height = 15,
                width = 60,
                )
        inputtxt.grid(row = 1 , column= 0 )
        global dynamicLabel 
        dynamicLabel = ttk.Label(rightFrame, text = "select some files" ) #this label shows the directory of the selected file
        #dynamicLabel.grid(row = 2, column= 6)


        


#this one will be useful for the runtime section
def loadFile(): #select the file from os explorer and return its directory as string type
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

    dynamicLabel.config(text= file )
  
    #showinfo(
       # title='Selected File',
      #  message= str(file)
     #   )

    return file


# Driver Code
app = tkinterApp() ##app corresponds to the object app, its attributes are: 
app.mainloop()
import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox as msgbox


LARGEFONT = ("Verdana", 24)



class RunTimePage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19)) 
        
        folder_name = controller.getFolder() #this variable has the name of the folder used to load all the sdl and tld files. The folder should be in the same main folder of these py files





        def loadListBoxs():
            service_list = [file for file in os.listdir(folder_name) if file.endswith(".sdl")] 
            target_list = [file for file in os.listdir(folder_name) if file.endswith(".tdl")]
            
            for file in service_list:
                servicesListBox.insert('', 'end', text="0", values=(str(file), 'ok!')) #for now, the validity is not implemented, it just shows ok for everyone
            for file in target_list:
                targetsListBox.insert('', 'end', text="0", values=( str(file), 'ok!'))# validity is not implemented yet
    
        def execute():
            if (len(targetsListBox.get_children())): #TODO
                controller.show_testPage()
               
            else:
                msgbox.showerror("check your files", "Please, check the .tdl file and try again.")
                
        def setColumnsNames(listBox): #This method create headings names, and change text size to be bigger
            style1 = ttk.Style()
            style1.configure("Treeview.Heading", font=(None, 22), ) #changing heading text size
            style1.configure("Treeview", font=(None, 16), rowheight = 20) #changing elements text size

            listBox.column( "#1", anchor= "center" , width = 400)
            listBox.heading("#1", text="Name")
            listBox.column( "#2", anchor= "center", width = 200)
            listBox.heading("#2", text="Validity")
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        
        label = ttk.Label(self, text ="the selected folder is: " + folder_name, font = LARGEFONT)
        label.grid(row = 0, padx = 10, pady = 20)
        buttonFrame = tk.Frame(self)
        
        #self.configure(width= 1920, height= 1080)
        servicesLabel = ttk.Label (self, text = "SERVICES:")
        targetsLabel = ttk.Label ( self, text= "TARGETS:")
        #frame.grid(row = 5, column= 0)
        # button to show frame 2 with text
        # layout2
        homeButton = ttk.Button(buttonFrame, text ="Home",
                            command = lambda : controller.show_mainPage(), style='CustomButton.TButton')

        exectueButton = ttk.Button(buttonFrame, text= "EXECUTE", command= execute, style='CustomButton.TButton')
        
        # putting the button in its place
        # by using grid
        homeButton.grid(row = 0, column = 0, padx = 10, pady = 10)  
        exectueButton.grid(row= 0, column= 1, padx= 10, pady= 10)
        buttonFrame.grid(column=0, row= 5, pady= 50)
        servicesListBox = ttk.Treeview(self, height=12, columns=("Name", "Validity"), show='headings', padding= 5)
        servicesListBox.grid(row = 2, column= 0, padx= 15, pady= 2)
        servicesLabel.grid(row =1, column=0, pady= 50)
        targetsListBox = ttk.Treeview(self, height=2, columns=("Name", "Validity") , show='headings', padding= 5)
        targetsListBox.grid(row = 4, column= 0, padx= 15, pady=20)
        targetsLabel.grid(row = 3, column= 0, pady=10)
        setColumnsNames(servicesListBox)
        setColumnsNames(targetsListBox)

        loadListBoxs()
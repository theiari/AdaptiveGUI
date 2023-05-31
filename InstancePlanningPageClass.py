import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from tkinter import filedialog

LARGEFONT = ("Verdana", 24)


class InstancePlanningPage(tk.Frame):
    
    path = ''
    listBox : tk.Listbox

    def refreshListBox(self, controller): #very ugly way to update items in the listbox
        print(self.path)
        if self.path == '':
            msgbox.showerror("error", "Please select a valid path!\n")
            controller.show_mainPage()
        else:
            file_list = [file for file in os.listdir(self.path) if file.endswith(".sdl") or file.endswith(".tdl")]
            self.listBox.delete(0, END)
            
            for file in file_list:
                self.listBox.insert(END,str(file))
    
    def emptyListBox(self):
        self.listBox.delete(0, END) #this ensures that the listbox will be empty every time the frame is loaded, before choosing the new directory

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19)) 

        sdl_list = [file for file in os.listdir("./templates") if file.endswith(".sdl")]
        tdl_list = [file for file in os.listdir("./templates") if file.endswith(".tdl")]

        def reset():
            inputtxt.delete(1.0, END)
            self.listBox.delete(0, END)
            #loadedFileLabel.config(text = "here is the list of all loaded files: \n")
        
        def refreshListBox(controller): #very ugly way to update items in the listbox
            #path = str('./' + str(loadFile())) #TODO right now it crashes and it loads at the very begin with no apparent reason
            file_list = [file for file in os.listdir(self.path) if file.endswith(".sdl") or file.endswith(".tdl")]
            self.listBox.delete(0, END)
            
            for file in file_list:
                self.listBox.insert(END,str(file))
       
        def delete_item(): #function called by button DELETE
            selected_index = self.listBox.curselection()
            selected_value = self.listBox.get(selected_index)
            file_path = os.path.join(self.path, selected_value)
            if selected_index:
                flag = msgbox.askyesno("Are you sure?", "do you want to permanently delete "+selected_value+" ?")
                print(flag)
                if os.path.isfile(file_path) and flag:
                   os.remove(str(file_path))
                   msgbox.showinfo("all gone"," File "+selected_value+ " has been deleted")
                   self.listBox.delete(selected_index)
                   reset()
                   refreshListBox(controller)
                

        def showFile(): #action of button LOAD
            inputtxt.delete(1.0, END) #first we clean the textbox
            selected_index = self.listBox.curselection()
            selected_value = self.listBox.get(selected_index)
            file_path = os.path.join(self.path, selected_value)
            with open(str(file_path), "r") as file:
                inputtxt.insert(1.0,str(file.read()))


        def loadSDLFiles():
            inputtxt.delete(1.0, END)
            for file in sdl_list:
                subfolder = "templates"
                file_path = os.path.join(subfolder, str(file))
                with open(str(file_path), "r") as file:
                    inputtxt.insert(END,str(file.read()+ '\n')) #A NEWLINE IS INSERTED FOR EVERY NEW LOADED FILE


        def loadTDLFiles():
            inputtxt.delete(1.0, END)
            for file in tdl_list:
                subfolder = "templates"
                file_path = os.path.join(subfolder, str(file))
                with open(str(file_path), "r") as file:
                    inputtxt.insert(END,str(file.read()+ '\n')) #A NEWLINE IS INSERTED FOR EVERY NEW LOADED FILE   


        def preSave():
                info_window = tk.Toplevel()
                info_window.grab_set()
                info_window.title("Save the model")
                info_window.geometry("600x120")
                info_label = tk.Label(info_window, text="Please, select a name for the file", font= ('arial',18) )
                info_label.grid(row=0, column=0)
                boolean = tk.IntVar()
                radioButtonSDL = ttk.Radiobutton(
                    info_window,
                    text='.sdl',
                    value=1, #TODO right now I can select both radiobuttons, while only one just have to do so
                    variable= boolean
                )  

                radioButtonTDL = ttk.Radiobutton(
                    info_window,
                    text='.tdl',
                    value=2,
                    variable= boolean
                )

                radioButtonSDL.grid(row=1, column= 1)                
                radioButtonTDL.grid(row=1, column=2)
                radioButtonSDL.invoke()

                saveTextBox= tk.Text(info_window, height= 1, width= 18)
                saveTextBox.grid(row=1, column=0)
 
                close_button = tk.Button(info_window, text="Save", command= lambda : saveFile(info_window, saveTextBox.get(0.0,END).strip(), boolean) )
                close_button.grid(row=1, column=3)


        def saveFile(info_window, filename, boolean):
            info_window.destroy()
            info_window.update()
            if (boolean.get() == 1):
                filename = filename + ".sdl".strip()
            else:
                filename = filename + ".tdl".strip()

            try:
                file_path = os.path.join(self.path, filename)
                text_file = open(file_path, "w") 
                text_file.write(inputtxt.get("1.0", "end-1c").strip()) #the file is saved in the current folder
                text_file.close()
                inputtxt.delete(1.0, END) #textbox is now blank
                msgbox.showinfo("Information", "file " +filename+" has been saved!")
                refreshListBox(controller)
            except Exception as e:
                msgbox.showerror("error", "an error occurred!"+str(e))    
           
            #refreshListBox(self.path)

        def goHome():
            reset()
            controller.show_mainPage()
            
        def wipeText():
            inputtxt.delete(1, END)

        # FRAME DECLARATION & GRID
        #frame placed in the top side of the window
        topFrame = tk.Frame(self, width = 200 , height= 30)
        topFrame.grid(row = 0, column= 0 )
        #frame placed in the centre of the window
        centerFrame = tk.Frame(self,  highlightbackground= 'black', width = 200 , height= 200)
        centerFrame.grid(row = 1, column= 0 )
        #frame placed in the right side of the window
        rightFrame = tk.Frame(self, width = 100 , height= 100, padx= 50, pady= 50)
        rightFrame.grid(row = 1, column= 1)
        #frame palced at the bottom of the window
        bottomFrame = tk.Frame(self, width = 200 , height= 200)
        bottomFrame.grid(row = 8, column= 0 )
        #frame used inside RightFrame
        buttonsFrame = tk.Frame(rightFrame)
        buttonsFrame.grid(row=2, column=0)

        #LABEL & BUTTON DECLARATION & GRID  
        resetButton = ttk.Button(bottomFrame, text="Cancel", command= wipeText, style= 'CustomButton.TButton') #function to redet the whole design window, has not be implemented yet // TODO
        resetButton.grid(column=0, row=0, padx = 3, pady = 3)
        #model button should load the file, button MODEL used to retrieve .tdl or .sdl files
        modelButton = ttk.Button(bottomFrame, text="SAVE", command= preSave, style= 'CustomButton.TButton') #function to load a file from local storage, for now just a single one
        modelButton.grid(column=1, row=0, padx = 3, pady = 3)

        deleteButton= ttk.Button(buttonsFrame, text="Delete file", command= delete_item , style= 'CustomButton.TButton') #not sure if this is essential, for now I'll just leave it here
        deleteButton.grid(column=0, row=0, padx = 8, pady = 3)               #it does the same action as Service/Target Template, for now.

        loadButton = ttk.Button(buttonsFrame, text="Load file", command= showFile ,style= 'CustomButton.TButton')
        loadButton.grid(column=1, row=0, padx = 8, pady = 3)
        
        label = ttk.Label(centerFrame, text ="Instance Planning Design Time", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        self.listBox = tk.Listbox(rightFrame, width= 30, height= 25, font= ('arial',14))
        self.listBox.grid(row= 0, column= 0)

        startPageButton = ttk.Button(bottomFrame, text ="Home", command = goHome , style= 'CustomButton.TButton')   
        startPageButton.grid(row = 0, column = 2, padx = 3, pady = 3)

        modelServiceButton = ttk.Button(topFrame, text = " Service Template ", command= loadSDLFiles, style= 'CustomButton.TButton')
        modelServiceButton.grid(row = 1, column = 0, pady= 5)

        modelTargetButton =  ttk.Button(topFrame, text = " Target Template ", command= loadTDLFiles, style= 'CustomButton.TButton')    
        modelTargetButton.grid(row = 1, column = 1, pady= 5)
        
        inputtxt = tk.Text(centerFrame,
            height = 38,
            width = 115,
        )
        inputtxt.grid(row= 1, column= 0)


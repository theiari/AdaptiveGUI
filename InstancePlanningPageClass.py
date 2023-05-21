import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox


LARGEFONT = ("Verdana", 24)
class InstancePlanningPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19)) 

        file_list = [file for file in os.listdir("./saved_models") if file.endswith(".sdl") or file.endswith(".tdl")]
        sdl_list = [file for file in os.listdir("./templates") if file.endswith(".sdl")]
        tdl_list = [file for file in os.listdir("./templates") if file.endswith(".tdl")]
        def reset():
            inputtxt.delete(1.0, END)
            #loadedFileLabel.config(text = "here is the list of all loaded files: \n")
        
        def refreshListBox(): #very ugly way to update items in the listbox
            file_list = [file for file in os.listdir("./saved_models") if file.endswith(".sdl") or file.endswith(".tdl")]
            listBox.delete(0, END)
            
            for file in file_list:
                listBox.insert(END,str(file))
       
        def delete_item(): #function called by button DELETE
            selected_index = listBox.curselection()
            selected_value = listBox.get(selected_index)
            subfolder = "saved_models"
            file_path = os.path.join(subfolder, selected_value)
            if selected_index:
                flag = msgbox.askyesno("Are you sure?", "do you want to permanently delete "+selected_value+" ?")
                print(flag)
                if os.path.isfile(file_path) and flag:
                   file_list.remove(selected_value)
                   os.remove(str(file_path))
                   msgbox.showinfo("all gone"," File "+selected_value+ "has been deleted")
                   listBox.delete(selected_index)
                   reset()
                   refreshListBox()
                

        def showFile(): #action of button LOAD
            inputtxt.delete(1.0, END) #first we clean the textbox
            selected_index = listBox.curselection()
            selected_value = listBox.get(selected_index)
            subfolder = "saved_models"
            file_path = os.path.join(subfolder, selected_value)
            with open(str(file_path), "r") as file:
                inputtxt.insert(1.0,str(file.read()))

        def loadSDLFiles():
            reset()
            for file in sdl_list:
                subfolder = "templates"
                file_path = os.path.join(subfolder, str(file))
                with open(str(file_path), "r") as file:
                        inputtxt.insert(END,str(file.read()+ '\n')) #A NEWLINE IS INSERTED FOR EVERY NEW LOADED FILE

        def loadTDLFiles():
            reset()
            for file in tdl_list:
                subfolder = "templates"
                file_path = os.path.join(subfolder, str(file))
                with open(str(file_path), "r") as file:
                        inputtxt.insert(END,str(file.read()+ '\n')) #A NEWLINE IS INSERTED FOR EVERY NEW LOADED FILE   

        def preSave():
                info_window = tk.Toplevel()
                info_window.grab_set()
                info_window.title("Save the model")
                info_window.geometry("1280x720")
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
                subfolder = "saved_models"
                file_path = os.path.join(subfolder, filename)
                text_file = open(file_path, "w") 
                text_file.write(inputtxt.get("1.0", "end-1c").strip()) #the file is saved in the current folder
                text_file.close()
                inputtxt.delete(1.0, END) #textbox is now blank
                msgbox.showinfo("Information", "file " +filename+" has been saved!")
            except Exception as e:
                msgbox.showerror("error", "an error occurred!"+str(e))    
           
            refreshListBox()

        def goHome():
            reset()
            controller.show_mainPage()
            

        # FRAME DECLARATION & GRID
        
        #frame placed in the top side of the window
        topFrame = tk.Frame(self, width = 200 , height= 30)
        topFrame.grid(row = 0, column= 0 )
        #frame placed in the centre of the window
        centerFrame = tk.Frame(self,  highlightbackground= 'black', width = 200 , height= 200, padx=10)
        centerFrame.grid(row = 1, column= 0 )
        #frame placed in the right side of the window
        rightFrame = tk.Frame(self, width = 100 , height= 100, padx=30)
        rightFrame.grid(row = 1, column= 6)
        #frame palced at the bottom of the window
        bottomFrame = tk.Frame(self, width = 200 , height= 200)
        bottomFrame.grid(row = 8, column= 0 )
        #frame used inside RightFrame
        buttonsFrame = tk.Frame(rightFrame)
        buttonsFrame.grid(row=2, column=0)


        #LABEL & BUTTON DECLARATION & GRID 
 
        resetButton = ttk.Button(bottomFrame, text="RESET", command= reset , style= 'CustomButton.TButton') #function to redet the whole design window, has not be implemented yet // TODO
        resetButton.grid(column=0, row=0, padx = 3, pady = 3)
 
        #model button should load the file
        #button MODEL used to retrieve .tdl or .sdl files
        modelButton = ttk.Button(bottomFrame, text="SAVE", command= preSave, style= 'CustomButton.TButton' ) #function to load a file from local storage, for now just a single one
        modelButton.grid(column=1, row=0, padx = 3, pady = 3)

        deleteButton= ttk.Button(buttonsFrame, text="delete", command= delete_item , style= 'CustomButton.TButton') #not sure if this is essential, for now I'll just leave it here
        deleteButton.grid(column=0, row=0, padx = 8, pady = 3)               #it does the same action as Service/Target Template, for now.

        loadButton = ttk.Button(buttonsFrame, text="load", command= showFile ,style= 'CustomButton.TButton')
        loadButton.grid(column=1, row=0, padx = 8, pady = 3)
        label = ttk.Label(centerFrame, text ="Instance Planning Design Time", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        listBox = tk.Listbox(rightFrame, width= 40, height= 25, font= ('arial',14))
        refreshListBox()
        listBox.grid(row= 1, column= 0)

        loadedFileLabel = ttk.Label(rightFrame, text='here is the list of all loaded files: \n')
        #loadedFileLabel.grid(row = 1, column= 5, padx= 10)
        startPageButton = ttk.Button(bottomFrame, text ="Home", command = goHome , style= 'CustomButton.TButton')   
        startPageButton.grid(row = 0, column = 2, padx = 3, pady = 3)

        modelServiceButton = ttk.Button(topFrame, text = " Service Template ", command= loadSDLFiles, style= 'CustomButton.TButton')
        modelServiceButton.grid(row = 1, column = 0, pady= 5)

        modelTargetButton =  ttk.Button(topFrame, text = " Target Template ", command= loadTDLFiles, style= 'CustomButton.TButton')    
        modelTargetButton.grid(row = 1, column = 1, pady= 5)


        inputtxt = tk.Text(centerFrame,
                height = 35,
                width = 110,
                
                )
        inputtxt.grid(row = 1 , column= 0 )
        global dynamicLabel 
        dynamicLabel = ttk.Label(rightFrame, text = "select some files" ) #this label shows the directory of the selected file
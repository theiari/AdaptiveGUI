import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
from tkinter import END
from tkinter import messagebox as msgbox
LARGEFONT = ("Verdana", 24)


class ServiceStatePage(tk.Frame):
    #global redLight, yellowLight, greenLight
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.option_add("*Font","aerial")
        #self.redLight = tk.PhotoImage(file="redLight.png").subsample(200,200) #the "self" part is essential to avoid garbage collection
        #self.yellowLight = PhotoImage(file="yellowLight.png")
        #self.greenLight = PhotoImage(file="greenLight.png")
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19))

        def disruptionHandler():
            highlighted_value = comboBox.get() #return the selected value
            temp : tk.Label
            temp = boxes[int(highlighted_value) -1]
            temp.config(background= "red")
            #self.after(5000, backToGreen(temp) )

        #def backToGreen(temp):
            #temp.config(background= "green")

        self.grid_columnconfigure(0, weight=0)
        rightFrame = tk.Frame(self, width= 400, height= 100)
        leftFrame = tk.Frame(self, width= 800, height= 100, padx= 350)
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] #random data 
        buttosFrame = tk.Frame(rightFrame)
        buttosFrame.grid(column=0, row = 5, pady=30)
        rightFrame.grid(column=1, row=1)
        leftFrame.grid(column=0, row = 1)
        self.servicesLabel = ttk.Label(self, text= "Services", font= LARGEFONT)
        self.servicesLabel.grid(row=0, column=0, padx=10, pady=10)
        processLabel = ttk.Label(self, text= "Processes" , font= LARGEFONT)
        processLabel.grid(row=0, column= 1, padx= 10, pady= 10)

        num_elements = len(data)


        def refreshListBox(): #very ugly way to update items in the listbox
            file_list = [file for file in os.listdir("./saved_models") if file.endswith(".sdl")]
            listBox.delete(0, END)
            comboBox['values'] = data
            comboBox.current(0) #load the first file, instead of showin a blank selection
            for file in file_list:
                listBox.insert(END,str(file))
            
        def start():
            if any(box.cget("background") == "red" for box in boxes):
             msgbox.showerror("Error", "Some processes are not working")
            else:
             msgbox.showinfo("All good", "Hurray!")

        def refreshStates():
           for label in boxes:
              label.config(background = "green")


        # Create frames for each cell
        frames = []
        boxes = []
        for i in range(num_elements):
            frame = tk.Frame(leftFrame, width=10, height=10, borderwidth=1, relief="solid")
            frame.grid(row=i // 3, column=i % 3)  # Adjust the column value to change the number of columns
            frames.append(frame)

        # Add text label to each frame
            #box = tk.Label(frame, width= 16, height= 8, image= self.redLight) NOT WORKING SO FAR
            box = tk.Label(frame, width= 16, height= 8,  text= str(data[i]), background= "green")
            boxes.append(box)
            #box.insert(str(data[i]))
            #box.pack(fill=tk.BOTH, expand=True)
            box.grid(row=0, column=0, sticky="nsew")

        listBox = tk.Listbox(rightFrame, width= 25, height= 15, font= ('arial',14))
       
        listBox.grid(column= 0, row= 0)

        comboBox = ttk.Combobox(rightFrame,width= 25, height= 15, font= ('arial',14), state= "readonly") #readonly avoid the user from entering values arbitarily
        comboBox.grid(column= 0, row= 1, pady=30)

        refreshListBox()
        # Button to go back to the start page
        disruptionButton = ttk.Button(rightFrame, text="Send disruption", command=disruptionHandler, style= 'CustomButton.TButton', width= 20)
        disruptionButton.grid(row=3, column=0, padx=10, pady=10)

        homeButton = ttk.Button(buttosFrame, text="Home", command=lambda: controller.show_mainPage(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)
        startButton = ttk.Button(buttosFrame, text="Start", command= start, style= 'CustomButton.TButton') #no action
        startButton.grid(row=1, column=1, padx=10, pady=10)
        refreshButton = ttk.Button(rightFrame, text="refresh states", command=refreshStates, style= 'CustomButton.TButton', width= 20) #debug button to reset background to green
        refreshButton .grid(row=4, column=0, padx=10, pady=10)
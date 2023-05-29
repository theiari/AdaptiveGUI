import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image #EXTRA LIBRARY --> pip install pillow

LARGEFONT = ("Verdana", 24)


class ServiceStatePage(tk.Frame):
    #global redLight, yellowLight, greenLight
    global background_image
    labels = [] # boxes corresonds to a collection of labels, each one inside a frame



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
            temp = self.labels[int(highlighted_value) -1]
            temp.config(background= "red")
            #self.after(5000, backToGreen(temp) )

        #def backToGreen(temp):
            #temp.config(background= "green")

        self.grid_columnconfigure(0, weight=0)
        rightFrame = tk.Frame(self, width= 400, height= 100)
        
        backgroundFrame = tk.Frame(self, width= 1400)
        leftFrame = tk.Frame(backgroundFrame, width= 1000)
        
        servicesMap = controller.getServicesMap()
        positions = list(servicesMap.values())
        data = list(servicesMap.keys())
        matrix = [0,0]
        matrix = controller.getMatrix()
        image_path = controller.getImage_path()
        #self.background_image = tk.PhotoImage(file= image_path).subsample(200,200) #the "self" part is essential to avoid garbage collection
        self.background_image = ImageTk.PhotoImage(Image.open(image_path).resize((1200,900)))
        background_image_label = tk.Label(backgroundFrame, image= self.background_image)
        


        #canvas = tk.Canvas(backgroundFrame, width=400, height=100)
        #canvas.pack()

        #img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGTH), Image.ANTIALIAS))
        #canvas.background = img  # Keep a reference in case this code is put in a function.
        #bg = canvas.create_image(0, 0, anchor=tk.NW, image= self.background_image)






        buttonsFrame = tk.Frame(rightFrame)


        processLabel = ttk.Label(backgroundFrame , text= "Processes" , font= LARGEFONT)
        processLabel.pack(side= "top")
        rightFrame.pack(side = "right", padx= 50)
        backgroundFrame.pack(side= "left", padx= 50)
        background_image_label.pack()
        leftFrame.pack()
        buttonsFrame.grid(column=0, row = 5, pady=30)
        self.servicesLabel = ttk.Label(rightFrame, text= "Service", font= LARGEFONT)
        self.servicesLabel.grid(row= 0, column= 0)
        

        num_elements = matrix[0] * matrix[1]


        def refreshListBox(): #very ugly way to update items in the listbox
            file_list = [file for file in os.listdir("./saved_models") if file.endswith(".sdl")]
            listBox.delete(0, END)
            comboBox['values'] = data
            comboBox.current(0) #load the first file, instead of showin a blank selection
            for file in file_list:
                listBox.insert(END,str(file))
            
        def start():
            if any(box.cget("background") == "red" for box in self.labels):
             msgbox.showerror("Error", "Some processes are not working")
            else:
             msgbox.showinfo("All good", "Hurray!")

        


        # Create frames for each cell
        frames = []
       
        
        covered_indexes = []
        j = 0
        
        for i in range(num_elements):  # Create required number of boxes based on matrix dimensions
            frame = tk.Frame(background_image_label, width=120, height=120, borderwidth=1, relief="raised", padx= 5 , pady= 35)
            frame.grid(row=i // matrix[1], column=i % matrix[1])  # Adjust the column value to change the number of columns
            frames.append(frame)
            label = tk.Label(frame,text= '')
            label.pack()
            self.labels.append(label)

        for position in positions:
            
            index = position[0] * matrix[1] + position[1]  # Calculate the corresponding index for the frame

            if index < len(frames):
                frame : tk.Frame  = frames[index]
                label : tk.Label = self.labels[index]
                label.config(text= data[j])  # right now it rewrite the text showing service label
                covered_indexes.append(index)  # Add the covered index to the list, just a debug stuff for now, probably useless soon
                
            else:
                frame = frames[index]
                label = tk.Label(frame, text=" ")
                

    
            
            label.pack()  # Adjust the label placement within the frame if necessary
            #print(covered_indexes)
            j= j+1
            

                
        # Add text label to each frame
            
            #try:
                #box = tk.Label(frame, width= 15, height= 6,  text= str(data[i]), background= "green", font = ('arial',10) ) #right now data[] has all the labels retrieved from JSON services
            #except IndexError as error:
                #box = tk.Label(frame, width= 15, height= 6,  text= ' ' , font = ('arial',10))  #in this way we create the table with all the expected frames
                
                
            
                #boxes.append(box)
            #box.insert(str(data[i]))
            #box.pack(fill=tk.BOTH, expand=True)
                #box.pack()
                
        
        

        listBox = tk.Listbox(rightFrame, width= 25, height= 15, font= ('arial',14))
       
        listBox.grid(column= 0, row= 1)

        comboBox = ttk.Combobox(rightFrame,width= 25, height= 15, font= ('arial',14), state= "readonly") #readonly avoid the user from entering values arbitarily
        comboBox.grid(column= 0, row= 2, pady=30)

        refreshListBox()
        # Button to go back to the start page
        disruptionButton = ttk.Button(rightFrame, text="Send disruption", command=disruptionHandler, style= 'CustomButton.TButton', width= 20)
        disruptionButton.grid(row=3, column=0, padx=10, pady=10)

        homeButton = ttk.Button(buttonsFrame, text="Home", command=lambda: controller.show_mainPage(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)
        startButton = ttk.Button(buttonsFrame, text="Start", command= start, style= 'CustomButton.TButton') #no action
        startButton.grid(row=1, column=1, padx=10, pady=10)
        refreshButton = ttk.Button(rightFrame, text="refresh states", command='', style= 'CustomButton.TButton', width= 20) #debug button to reset background to green
        refreshButton .grid(row=4, column=0, padx=10, pady=10)
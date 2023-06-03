import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image #EXTRA LIBRARY --> pip install pillow
import json
import cv2 #pip install opencv-python


LARGEFONT = ("Verdana", 24)

class ServiceStatePage(tk.Frame):
    
    config_file = ''
    global background_image
    labels = [] # boxes corresonds to a collection of labels, each one is placed inside a frame
    services_map = {} # this is a map/dict with key being service label and value being the tuple ( x, y, nome_file) all retrived from the json file
    data : list #this is the keyset of the map above
    resized_image : Image #this is the image that is resized to a fixed length of 1200 * 900 ( see row 93)
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.option_add("*Font","aerial")
        
        self.controller = controller
        self.data = []
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=('Arial', 19))
        
        #this right now does nothing
        def disruptionHandler():
            highlighted_value = self.comboBox.get() #return the selected value
            temp : tk.Label
            temp = self.labels[int(highlighted_value) -1]
            temp.config(background= "red")

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

        self.listBox = tk.Listbox(self.rightFrame, width= 25, height= 15, font= ('arial',14))
        self.listBox.grid(column= 0, row= 1)

        self.comboBox = ttk.Combobox(self.rightFrame,width= 25, height= 15, font= ('arial',14), state= "readonly") #readonly avoid the user from entering values arbitarily
        self.comboBox.grid(column= 0, row= 2, pady=30)

        # Button to go back to the start page
        disruptionButton = ttk.Button(self.rightFrame, text="Send disruption", command=disruptionHandler, style= 'CustomButton.TButton', width= 20)
        disruptionButton.grid(row=3, column=0, padx=10, pady=10)

        homeButton = ttk.Button(buttonsFrame, text="Home", command=lambda: controller.show_mainPage(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)
        startButton = ttk.Button(buttonsFrame, text="Start", command= self.start, style= 'CustomButton.TButton') #no action
        startButton.grid(row=1, column=1, padx=10, pady=10)
        refreshButton = ttk.Button(self.rightFrame, text="refresh states", command='', style= 'CustomButton.TButton', width= 20) #debug button to reset background to green
        refreshButton .grid(row=4, column=0, padx=10, pady=10)

        
    #ALL THE NEW STUFF SHOULD BE IN THIS CLASS BELOW
    
    def loadImage(self):

        
        self.image_to_read = 'factory_layout.jpg'    
        self.saved_image = 'factory_layout_colored.jpg' #right now cv2 also creates this image, which is scaled at the right resize, not sure if it is possible to make a render/saving of the whole image with the rectangles
        
        self.img = cv2.imread(self.image_to_read)
        self.resized_image = cv2.resize(self.img, (1200, 900))

        cv2.resize(self.img, (900, 500))


        self.overlay = self.img.copy()
        
        #cv2.rectangle(self.overlay, (500,50), (400,100), (0, 255, 0), -1)
#        self.opacity = 0.4
#cv2.addWeighted(self.overlay, self.opacity, self.img, 1 - self.opacity, 0, self.img)
        #cv2.imwrite( self.saved_image, self.resized_image)

        self.im = Image.open(self.saved_image)
        self.photo = ImageTk.PhotoImage(self.im)     

        self.canvas = tk.Canvas(self.backgroundFrame, width = 1200, height = 900)
       
        
        self.canvas.pack()
      

        self.canvas.create_image(0,0, anchor=tk.N+tk.W, image = self.photo)

        #ROWS AND COLUMNS ARE RETRIEVED FROM THE JSON 
        number_of_rows = self.matrix[0]
        number_of_columns = self.matrix[1]

       
        #sizes are fixed depending on the number of cell needed to be drawed
        cell_width = self.resized_image.shape[1] // number_of_columns # this is the width of every canvas
        cell_height = self.resized_image.shape[0] // number_of_rows # this is the height of every canvas

        #SOME CONTEXT CONCERNING X0..Y1:
        'x0,y0 are the coordinates of the corner in top-left of the canvas, while x1,y1 in the bottom-right'

        #  (x0,y0)
        #     *-----------------
        #     |                |
        #     |                |
        #     -----------------*
        #                   (x1,y1)


        'The loop i wrote will draw each canvas starting from the top left corner, then covers the image column by column.'
        'At the end of every column, it will restart from the left side, one row below from the first column'

        x0 = 2 #this is a small offset to let the border be visible, otherwise it'd be outside the image
        y0 = 2 #this is a small offset to let the border be visible, otherwise it'd be outside the image
        y1 = cell_height
        rectangles_positions = [] #this list contains the coordinates of every canvas created in the form -> [(x0, y0, x1, y1)]
        rectangles_positions_table = [] #similar to the previous one, but this list only collect the tuple [ (row, column) of each canvas]

        #row and column are just two counters that I used to track the position of every service among the table, could be useful not sure
        row = 1
        column = 1
        i = 0
        while (self.resized_image.shape[0] - y0 >= cell_height -2 ): #draw rectangles until the end of the first column, the -2 is again the offset, without it, the loop will not draw the last row
            
            x1 = x0 + cell_width

           
            #the flag is essential to draw a service rectangle or a blank one ( the empty grey)
            flag = False
            for key, value in self.services_map.items(): #again, since the map is <label, (x,y, nome_file)> this loop checks if there is a service with the actual coordinates of drawed cell
                    
                    if value[:2] == (column, row): #the :2 is due to the fact that we don't need the third element of the tuple, we just focus on the first two ( x,y)
                        self.canvas.create_rectangle(x0, y0, x1,y1, fill="green", stipple="gray50")
                        self.canvas.create_text((x0+x1) / 2, (y0 + y1) / 2, text= str(key[:10] + '\n' +key[10:]), font= ('arial', 14, 'bold')) # here I also split every label into 2 lines, to make room for the text
                        flag = True
            if not flag: # if there's no service with the actual coordinates, just draw an empty grey rectangle
                        self.canvas.create_rectangle(x0, y0, x1,y1, fill="grey", stipple="gray50") #rectangles should always be drawed BEFORE the text, otherwise the text will be below the rectangle 
                        self.canvas.create_text((x0+x1) / 2, (y0 + y1) / 2, text= ' empty', font= ('arial', 14, 'underline'))
                    
                    
                #self.canvas.create_text((x0+x1) / 2, (y0 + y1) / 2, text= self.data_fixed_size[i], font= ('arial', 14)) 
        
                
                #self.canvas.create_rectangle(x0, y0, x1,y1, fill="grey", stipple="gray50")
                #self.canvas.create_text((x0+x1) / 2, (y0 + y1) / 2, text= ' empty', font= ('arial', 14))
         
                
            x0 += cell_width
            rectangles_positions.append((x0, y0, x1, y1)) #two collections to keep track of rectangles positions
            rectangles_positions_table.append((row, column))# this is to track rectangles ' row and column positions
            column += 1
            i +=1
            if x1 >= self.resized_image.shape[1] : #this is the width, once finished a pass, we need to move at the beginning on a lower row
                y0 +=cell_height #this number( 2 )  should be the same as the offset
                x0=2
                x1=2
                y1 +=cell_height #this number( 2 )  should be the same as the offset
                row += 1
                column = 1

            


        #END OF NEW PART (I GUESS)
    
    def start(self):
        if any(box.cget("background") == "red" for box in self.labels):
            msgbox.showerror("Error", "Some processes are not working")
        else:
            msgbox.showinfo("All good", "Hurray!")


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

        self.services_map = service_map
        
        positions = list(self.services_map.values())
        self.data = list(self.services_map.keys())
        
        #this cycle allow the data to be at a fixed length
        
        
        self.loadImage()
        


    def refreshComboBox(self): #very ugly way to update items in the listbox
        #data = list(self.service_map.keys())
        #self.listBox.delete(0, END)
        self.comboBox['values'] = self.data
        self.comboBox.current(0) #load the first file, instead of showin a blank selection
        #for file in data:
        #    self.listBox.insert(END,str(file))
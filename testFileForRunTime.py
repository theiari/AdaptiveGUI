import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import PIL
import json
import tkcap

class DrawCanvas(tk.Frame):
   #JSON stuff
    service_map = {} #services map of JSON file, is a map/dictionary <Key,Value> ==> <service.nome_file,[service.x, service.y, service.label], for all service in services. Pure projectual choice, I guess it could be approached differently...
    matrix = [] #is a vector with two elements [number_of_rows, number_of_columns]
    image_path= ''
    folder = '' #is the folder used to load all the .sdl and .tdl files, in runtimepage ( BEFORE entering in the ServiceStatePage)


    def loadJson(self):
        # Read the JSON file
        with open(f"config_layout.json") as json_file:
            data = json.load(json_file)
    
        # JSON attributes loading
        services = data['services']
        self.image_path = f"utils/{data['image_path']}"
        self.folder = data['folder']
        
        self.matrix = [data['matrix'][key] for key in ['rows', 'columns']]

        

        # Iterate over the services and extract relevant information
        for service in services:
            nome_file = service['nome_file']
            x=  service['x']
            y = service['y']
            label = service['label']

            #ALTERNATIVE SERVICE MAP KEY_VALUE PAIR
            self.service_map[label] = (x,y,nome_file)




    def __init__(self, parent):
        '''
        Prepare the frame and call the GUI initialization method.
        '''
        tk.Frame.__init__(self, parent)
        self.parent : tk.Frame
        self.parent=parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type        
        """
        self.parent.title("OpenCV + Tkinter")       
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)

        self.image_to_read = 'factory_layout.jpg'    
        self.saved_image = 'factory_layout_colored.jpg'
        
        self.img = cv2.imread(self.image_to_read)
        self.resized_image = cv2.resize(self.img, (900, 500))
        cv2.resize(self.img, (900, 500))
        self.overlay = self.img.copy()
        
        cv2.rectangle(self.overlay, (500,50), (400,100), (0, 255, 0), -1)
        self.opacity = 0.4
        cv2.addWeighted(self.overlay, self.opacity, self.img, 1 - self.opacity, 0, self.img)
        cv2.imwrite( self.saved_image, self.resized_image)

        self.im = Image.open(self.saved_image)
        self.photo = ImageTk.PhotoImage(self.im)     

        self.canvas = tk.Canvas(self.parent, width = 900, height = 500)
       
        
        self.canvas.grid(row = 0, column = 0)
      

        self.canvas.create_image(0,0, anchor=tk.N+tk.W, image = self.photo)
        #self.canvas.create_text(  200, 210, text= "service 1", font = ('arial', 45, 'bold'), fill= 'red')

        self.loadJson()
        #This garbage should be automated in a for loop (soon, I still need to figure out how...)
        '''self.canvas.create_rectangle(100, 50, 150,100, fill="green", stipple="gray25")
        self.canvas.create_text(125, 75, text= "test")
        self.canvas.create_rectangle(150, 50, 200,100, fill="green", stipple="gray25")
        self.canvas.create_text(175, 75, text= "test")
        self.canvas.create_rectangle(200, 50, 250,100, fill="yellow", stipple="gray25")
        self.canvas.create_text(225, 75, text= "test")
        self.canvas.create_rectangle(250, 50, 300,100, fill="red", stipple="gray25")
        self.canvas.create_text(275, 75, text= "test")
        self.canvas.create_rectangle(300, 50, 350,100, fill="yellow", stipple="gray25")
        self.canvas.create_text(325, 75, text= "test")'''

        number_of_rows = self.matrix[0]
        number_of_columns = self.matrix[1]
        cell_width = self.resized_image.shape[1] // number_of_columns # this is the width of every canvas
        cell_height = self.resized_image.shape[0] // number_of_rows # this is the height of every canvas
        x0 = 2 #this is a small offset to let the border be visible, otherwise it'd be outside the image
        y0 = 2 #this is a small offset to let the border be visible, otherwise it'd be outside the image
        y1 = cell_height
        rectangles_positions = [] #this list contains the coordinates of every canvas created in the form -> [(x0, y0, x1, y1)]
        rectangles_positions_table = [] #similar to the previous one, but this list only collect the tuple [ (row, column) of each canvas]
        'x0,y0 are the coordinates of the corner in top-left of the canvas, while x1,y1 in the bottom-right'

        #  (x0,y0)
        #     *-----------------
        #     |                |
        #     |                |
        #     -----------------*
        #                   (x1,y1)


        'The loop will draw each canva starting from the top left corner, then covers the image row by row.'
        'At the end of every row, it will restart from the left side, one row below'
        row = 1
        column = 1
        while (self.resized_image.shape[0] - y0 > cell_height):
            
            x1 = x0 + cell_width
            self.canvas.create_rectangle(x0, y0, x1,y1, fill="green", stipple="gray25")
           
            self.canvas.create_text((x0+x1) / 2, (y0 + y1) / 2, text= "test", font= ('arial', 14))
            x0 += cell_width
            rectangles_positions.append((x0, y0, x1, y1))
            rectangles_positions_table.append((row, column))
            column += 1
            if x1 >= self.resized_image.shape[1]: #this is the width, once finished a pass, we need to move at the beginning on a lower row
                y0 +=cell_height - 2 #this number( 2 )  should be the same as the offset
                x0=2
                x1=2
                y1 +=cell_height - 2 #this number( 2 )  should be the same as the offset
                row += 1
                column = 1

        #self.parent.winfo_rootx
        cap = tkcap.CAP(self.parent)     # master is an instance of tkinter.Tk
        cap.capture('saved_image.jpg', overwrite= True , )       # Capture and Save the screenshot of the tkiner window
      
        
            
            
            
            
        
        
      


      



def main():
    root=tk.Tk()
    d=DrawCanvas(root)
    root.mainloop()

if __name__=="__main__":
    main()
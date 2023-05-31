import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import PIL



class Begueradj(tk.Frame):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Prepare the frame and call the GUI initialization method.
        '''
        tk.Frame.__init__(self, parent)
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


        #This garbage should be automated in a for loop (soon, I still need to figure out how...)
        self.canvas.create_rectangle(100, 50, 150,100, fill="green", stipple="gray25")
        self.canvas.create_text(125, 75, text= "test")
        self.canvas.create_rectangle(150, 50, 200,100, fill="green", stipple="gray25")
        self.canvas.create_text(175, 75, text= "test")
        self.canvas.create_rectangle(200, 50, 250,100, fill="yellow", stipple="gray25")
        self.canvas.create_text(225, 75, text= "test")
        self.canvas.create_rectangle(250, 50, 300,100, fill="red", stipple="gray25")
        self.canvas.create_text(275, 75, text= "test")
        self.canvas.create_rectangle(300, 50, 350,100, fill="yellow", stipple="gray25")
        self.canvas.create_text(325, 75, text= "test")

        
        
      



        # Define the number of rows and columns for the table
        num_rows = 3
        num_columns = 4

        # Calculate the width and height of each table cell
        cell_width = 900 // num_columns
        cell_height = 500 // num_rows

      



def main():
    root=tk.Tk()
    d=Begueradj(root)
    root.mainloop()

if __name__=="__main__":
    main()
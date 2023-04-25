import tkinter as tk
from tkinter import ttk
LARGEFONT =("Verdana", 24)


class TestPage(tk.Frame):
    
    def __init__(self, parent, controller):
        super(TestPage, self).__init__()
        ttk.Frame.__init__(parent) 
        
        self.label = ttk.Label(parent, text ="this is a test page", font = LARGEFONT)
        self.label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        self.button2 = ttk.Button(parent, text ="Startpage",
                            command = lambda : controller.show_frame(self))
     
        # putting the button in its place by
        # using grid
        self.button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 24)


class ServiceStatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text="This is a test page", font=LARGEFONT)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Button to go back to the start page
        self.button = ttk.Button(self, text="Start Page", command=lambda: controller.show_mainPage())
        self.button.grid(row=1, column=0, padx=10, pady=10)

  
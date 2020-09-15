from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image
from tkinter import filedialog
import os
import shutil
from convert import Convert, deleteAll

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.image_location = ttk.Frame(self.parent)
        self.image_location.pack()
        self.button_location = Frame(self.parent)
        self.button_location.pack()
        self.photo_count = 0
        self.row = 0
        self.col = 0
        self.current_path = os.path.dirname(os.path.realpath(__file__))

        self.canvas = Canvas(self.image_location)
        self.scrollbar = ttk.Scrollbar(self.image_location, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_location.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.button1 = Button(self.button_location, text = 'Open Image', width = 25, command = self.open_img)
        self.button1.grid(row = 0, column = 0)
        self.button2 = Button(self.button_location, text = 'Convert', width = 25, command = lambda: Convert(self.current_path))
        self.button2.grid(row = 0, column = 1)
        self.button3 = Button(self.button_location, text = 'Clear', width = 25, command = self.clearEverything)
        self.button3.grid(row = 0, column = 2)
        
    def clearEverything(self):
        self.row = 0
        self.col = 0
        self.photo_count = 0
        for entry in os.scandir(self.current_path+'/Images'):
            # Check if directory exists
            if entry.is_dir():
                continue
            ext = entry.name.split('.')[-1]
            if ext == 'py' or ext == 'md':      # Checking so that the python file or the markdown file is not effected 
                continue
            os.remove(self.current_path+'/Images/'+entry.name)
            img = Image.open(self.current_path+'/necessary/colour-info.PNG')
            img = img.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.panel = ttk.Label(self.scrollable_frame, image=img)
            self.panel.image = img
            self.panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
            self.col = self.col + 2
            print(f"{self.row} {self.col}")
            if self.col >= 6:
                self.col = 0
                self.row = self.row + 2
        self.row = 0
        self.col = 0
        self.photo_count = 0
    def openfn(self):
        filename = filedialog.askopenfilenames(title='open')
        return filename
    def open_img(self):
        for element in self.openfn():
            try:
                shutil.copy(element, self.current_path+'/Images/'+str(self.photo_count)+'.jpg')
                self.photo_count = self.photo_count + 1
                img = Image.open(element)
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                self.panel = ttk.Label(self.scrollable_frame, image=img)
                self.panel.image = img
                self.panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
                self.col = self.col + 2
                print(f"{self.row} {self.col}")
                if self.col >= 6:
                    self.col = 0
                    self.row = self.row + 2
            except:
                pass

if __name__ == "__main__":
    root = Tk()
    root.geometry("550x300+300+150")
    root.resizable(width=False, height=False)
    MainApplication(root).pack(side = 'top', fill="both", expand=True)
    root.mainloop()

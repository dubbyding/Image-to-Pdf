from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import shutil
import datetime

class MainApplication(Frame):
    '''
        Main GUI interface
    '''
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent    # Root
        self.image_location = ttk.Frame(self.parent)
        self.image_location.pack()
        self.button_location = Frame(self.parent)
        self.button_location.pack()
        self.status = Frame(self.parent)
        self.status.pack()
        self.photo_count = 0
        self.row = 0
        self.col = 0
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.var = StringVar()


        #For Canvas and scrollbar
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

        #For Buttons
        self.button1 = Button(self.button_location, text = 'Open Image', width = 19, command = self.open_img)
        self.button1.grid(row = 0, column = 0)
        self.button2 = Button(self.button_location, text = 'Convert', width = 19, command = self.Convert)
        self.button2.grid(row = 0, column = 1)
        self.button3 = Button(self.button_location, text = 'Clear', width = 19, command = self.clearEverything)
        self.button3.grid(row = 0, column = 2)
        self.current_status = Label(self.status, textvariable = self.var)
        self.var.set("Status: Waiting")
        self.current_status.pack()
        
    def clearEverything(self):
        """
            To Clear everything from the screen
        """
        
        self.var.set("Status: Waiting")
        self.row = 0
        self.col = 0
        self.photo_count = 0
        for entry in os.scandir(self.current_path+'/temp'):
            # Check if directory exists
            if entry.is_dir():
                continue
            ext = entry.name.split('.')[-1]
            if ext == 'py' or ext == 'md':      # Checking so that the python file or the markdown file is not effected 
                continue
            os.remove(self.current_path+'/temp/'+entry.name)
            img = Image.open(self.current_path+'/necessary/colour-info.PNG')
            img = img.resize((100, 100), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.panel = ttk.Label(self.scrollable_frame, image=img)
            self.panel.image = img
            self.panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
            self.col = self.col + 2
            if self.col >= 6:
                self.col = 0
                self.row = self.row + 2
        self.row = 0
        self.col = 0
        self.photo_count = 0
    def openfn(self):
        """
            To open a dialog box for choosing files
        """
        image = (('jpg Image','jpg'), ('jpeg Image', 'jpeg'), ('png Image', 'png'), ('bmp Image', 'bmp'), ('webp Image', 'webp'))
        filename = filedialog.askopenfilenames(title='open', filetypes = image)
        return filename
    def open_img(self):
        """
            To Open Image and then move it to temporary location
        """
        for element in self.openfn():
            if not os.path.isdir(self.current_path+'/temp'):
                os.makedirs(self.current_path+'/temp')
                f = open(self.current_path+"/temp/info.txt", "w")
                f.write("Put images on this folder.")
                f.close()
            try:
                shutil.copy(element, self.current_path+'/temp/'+str(self.photo_count)+'.jpg')
                self.photo_count = self.photo_count + 1
                img = Image.open(element)
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                self.panel = ttk.Label(self.scrollable_frame, image=img)
                self.panel.image = img
                self.panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
                self.col = self.col + 2
                if self.col >= 6:
                    self.col = 0
                    self.row = self.row + 2
                self.var.set("Status: Ready For Conversion")
            except:
                pass
    def Convert(self):
        """
            Convert into PDF and clear screen and delete temp value
        """
        dir_path = self.current_path
        initial = 0
        image_list = []

        # Checking if pdf folder exists and checks to name the file
        if not os.path.isdir(dir_path+'/pdf'):
            os.makedirs(dir_path+'/pdf')
        name = list(os.listdir(dir_path+'/pdf'))
        if name == []:
            name = '1'
        else:
            name = str(int(name[-1].split('.')[0: -1][0]) + 1)

        if any(os.scandir(dir_path+'/temp')):
            # Going through Images folder
            for entry in os.scandir(dir_path+'/temp'):
                # Check if directory exists
                if entry.is_dir():
                    continue
                ext = entry.name.split('.')[-1]
                if ext == 'py' or ext == 'md' or ext == 'txt':      # Checking so that the python file or the markdown file is not effected 
                    continue
                if initial == 0:
                    im1 = Image.open(dir_path+'/temp/'+entry.name, mode='r').convert('RGB')
                    initial = initial + 1
                else:
                    image_list.append(Image.open(dir_path+'/temp/'+entry.name, mode='r').convert('RGB'))

            try:
                if image_list == []:
                    im1.save(dir_path+'/pdf/'+name+'.pdf', mode='r')
                else:
                    im1.save(dir_path+'/pdf/'+name+'.pdf', mode='r',save_all = True, append_images = image_list)
            except:
                pass
        self.clearEverything()
        self.var.set("Status: Converted")


if __name__ == "__main__":
    root = Tk()
    root.geometry("440x320+300+150")
    root.resizable(width=False, height=False)
    application = MainApplication(root).pack(side = 'top', fill="both", expand=True)
    root.mainloop()

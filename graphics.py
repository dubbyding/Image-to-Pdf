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
        self.parent.iconphoto(False, PhotoImage(file="icon.png"))
        self.parent.protocol("WM_DELETE_WINDOW", self.closing_application)
        # For RGB color default
        self.r, self.g, self.b = [x>>8 for x in self.parent.winfo_rgb(self.parent['bg'])]

        self.image_location = ttk.Frame(self.parent)
        self.image_location.pack()
        self.button_location = Frame(self.parent)
        self.button_location.pack()
        self.file_location = Frame(self.parent)
        self.file_location.pack()
        self.file_name = Frame(self.parent)
        self.file_name.pack()
        self.status = Frame(self.parent)
        self.status.pack()
        self.photo_count = 0
        self.row = 0
        self.col = 0
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_file_path = StringVar()
        self.current_saving_location = os.path.join(self.current_path,"pdf")
        self.var = StringVar()
        self.name = '1'

        #For Canvas and scrollbar
        self.canvas = Canvas(self.image_location)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
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
        self.input1label = Label(self.file_location, textvariable=self.current_file_path, width=49, anchor='w')
        self.current_file_path.set(os.path.join(self.current_path,"pdf"))
        self.input1label.grid(row=0, column=1)
        self.input1 = Button(self.file_location, text = "Choose Path", command=self.select_directory)
        self.input1.grid(row=0, column=2)
        self.text_box_info = Label(self.file_name, text="File Name (no need to add extension) :-")
        self.text_box_info.grid(row=0, column=0)
        self.text_box = Entry(self.file_name, justify="left", textvariable=self.name, width=35)
        self.text_box.insert(END, self.name)
        self.text_box.grid(row=0, column=3)
        self.current_status = Label(self.status, textvariable = self.var)
        self.var.set("Status: Waiting")
        self.current_status.pack()

        
        

    def select_directory(self):
        self.current_saving_location = filedialog.askdirectory()
        self.current_file_path.set(self.current_saving_location)
        # print(self.current_file_path)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*int(event.delta/120), "units")
    def clearEverything(self):
        """
            To Clear everything from the screen
        """
        self.var.set("Status: Waiting")
        self.row = 0
        self.col = 0
        self.photo_count = 0
        try:
            for entry in os.scandir(self.current_path+'/temp'):
                # Check if directory exists
                if entry.is_dir():
                    continue
                ext = entry.name.split('.')[-1]
                if ext == 'py' or ext == 'md':      # Checking so that the python file or the markdown file is not effected 
                    continue
                os.remove(self.current_path+'/temp/'+entry.name)
                img = Image.new('RGB', (100,100), color = (self.r, self.g, self.b))     #Create new image to replace existing image
                img = ImageTk.PhotoImage(img)
                panel = ttk.Label(self.scrollable_frame, image=img)
                panel.image = img
                panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
                self.col = self.col + 2
                if self.col >= 6:
                    self.col = 0
                    self.row = self.row + 2
            self.row = 0
            self.col = 0
            self.photo_count = 0
        except FileNotFoundError:
            pass
    
    def closing_application(self):
        self.clearEverything()
        self.parent.destroy()

    def openfn(self):
        """
            To open a dialog box for choosing files
        """
        image = (('jpg Image','jpg'), ('jpeg Image', 'jpeg'), ('png Image', 'png'), ('bmp Image', 'bmp'), ('webp Image', 'webp'))
        filename = filedialog.askopenfilenames(title='open', filetypes = image)
        # print(filename)
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
                imgFan = ImageTk.PhotoImage(img)
                panel = ttk.Label(self.scrollable_frame, image=imgFan)
                panel.image = imgFan
                panel.grid(row=self.row, column = self.col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
                panel.bind("<Button-1>", self.on_click)
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
        
        if any(os.scandir(dir_path+'/temp')):
            images_list = []
            ext_list = []
            # Going through Images folder
            for entry in os.scandir(dir_path+'/temp'):
                if entry.is_dir():
                    continue
                images_list.append(int(entry.name.split('.')[0]))
                ext_list.append(entry.name.split('.')[-1])
            images_list.sort()
            for index, entry in enumerate(images_list):
                ext = ext_list[index]
                file_name = str(entry) + "." + ext
                # Check if directory exists
                if ext == 'py' or ext == 'md' or ext == 'txt':      # Checking so that the python file or the markdown file is not effected 
                    continue
                if initial == 0:
                    # print("initial")
                    im1 = Image.open(dir_path+'/temp/' + file_name, mode='r').convert('RGB')
                    initial = initial + 1
                else:
                    image_list.append(Image.open(dir_path+'/temp/' + file_name, mode='r').convert('RGB'))
            # print(image_list)
            self.name = self.text_box.get().replace(" ","_")
            try:
                file_name_location = os.path.join(self.current_saving_location,self.name+'.pdf')
                count = 1
                while os.path.exists(file_name_location):
                    self.name = self.name+"({})".format(count)
                    count += 1
                    file_name_location = os.path.join(self.current_saving_location,self.name+'.pdf')
                if image_list == []:
                    im1.save(file_name_location, mode='r')
                else:
                    im1.save(file_name_location, mode='r',save_all = True, append_images = image_list)
            except Exception as e:
                print(e)
                pass
            
            self.clearEverything()
            self.var.set("Status: Converted")
        else:
            self.clearEverything()
            self.var.set("Warning: Nothing Selected")
    def on_click(self,event):
        new_row = event.widget.grid_info()["row"]
        new_col = event.widget.grid_info()["column"]
        counter = int((3 * (new_row/2)) + (new_col/2))
        rotateImg = Image.open("temp/"+str(counter)+".jpg").transpose(Image.ROTATE_90)
        rotateImg.save("temp/"+str(counter)+".jpg")
        rotateImg = rotateImg.resize((100, 100), Image.ANTIALIAS)
        imgFan = ImageTk.PhotoImage(rotateImg)
        panel = ttk.Label(self.scrollable_frame, image=imgFan)
        panel.image = imgFan
        panel.grid(row=new_row, column = new_col, columnspan = 2, rowspan = 2, padx = 10, pady = 3)
        panel.bind("<Button-1>", self.on_click)


if __name__ == "__main__":
    root = Tk()
    root.geometry("440x360")
    root.resizable(width=False, height=False)
    root.title("Image To PDF")
    application = MainApplication(root).pack(side = 'top', fill="both", expand=True)
    root.mainloop()
from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from PIL import ImageTk, Image

class Window(Frame):
    outfile = '.jpg'
    loaded = None
    lbl = None
    def __init__(self, window=None):
        Frame.__init__(self, window)              
        self.window = window
        self.init_window()

    def init_window(self):
        self.window.title("Image Editor")
        self.pack(fill=BOTH, expand=1)
        menu = Menu(self.window)
        file = Menu(menu)
        file.add_command(label='Open', command=self.client_open)
        file.add_command(label='Close', command=self.client_close)
        menu.add_cascade(label='File', menu=file)
        resize = Menu(menu)
        resize.add_command(label='25%', command= lambda: self.client_resize(0.25)))
        self.window.config(menu=menu)

    def client_open(self):
        file = filedialog.askopenfilename(filetypes = (("Image files",".jpg .png .jpeg .bmp .gif"),("all files","*.*")))
        
        self.loaded = Image.open(file)
        render = ImageTk.PhotoImage(self.loaded)
        self.lbl = Label(self, image=render)
        self.lbl.image = render
        self.lbl.pack(expand=1)

    def client_close(self):
        self.loaded.close()
        self.lbl.forget()

    def client_resize(self, scaleFactor):


    def reload(self):

        
    def save(self):



    def client_exit(self):
        exit()

root = Tk()
root.geometry('1080x854')
app = Window(root)

root.mainloop()
from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from PIL import ImageTk, Image

class Window(Tk):
    
    def __init__(self):
        super(Window,self).__init__()
        self.init_window()
        self.loaded = None

    def init_window(self):
        self.title("Image Editor")
        self.createMenu()
        self.createCanvas()

    def createCanvas(self):
        self.canvas = Canvas(self, width=200, height=100)
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0)
        self.canvas.bind('<Motion>', self.callback)
        self.canvas.pack(fill=BOTH, expand=YES)

    def createMenu(self):
        menubar = Menu(self)
        self.config(menu = menubar)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='Open', command=self.client_open)
        file_menu.add_command(label='Close', command=self.client_close)
        file_menu.add_command(label='Save', command=self.client_save)
        file_menu.add_command(label='reset', command=self.client_reset)
        menubar.add_cascade(label='File', menu=file_menu)
        resize_menu = Menu(menubar)
        resize_menu.add_command(label='25%', command=(lambda: self.client_resize(0.25)))
        resize_menu.add_command(label='50%', command=(lambda: self.client_resize(0.50)))
        resize_menu.add_command(label='75%', command=(lambda: self.client_resize(0.75)))
        resize_menu.add_command(label='150%', command=(lambda: self.client_resize(1.5)))
        resize_menu.add_command(label='200%', command=(lambda: self.client_resize(2)))
        menubar.add_cascade(label='Resize', menu=resize_menu)
        
    def client_open(self):
        if (self.loaded):
            print("Please close open file before opening a new file")
            return
        try:
            self.infile = filedialog.askopenfilename(title = "Select file", filetypes = (("Image files",".jpg .png .jpeg .bmp .gif"),("all files","*.*")))
            self.loaded = Image.open(self.infile)
        except:
            print("An exception occurred, try opening the file again")
            return
        stringList = self.infile.split('/')
        self.outfile = 'cropped-' + stringList[len(stringList)-1]
        self.canvas.image = ImageTk.PhotoImage(self.loaded)
        self.img = self.canvas.create_image(0,0, image = self.canvas.image, anchor = NW)

    def client_close(self):
        if (self.loaded):
            self.loaded.close()
            self.loaded = None
            self.canvas.delete(self.img)
        else:
            print("Close: No image open")

    def client_resize(self, scaleFactor):
        width, height = self.loaded.size
        self.loaded.resize((int(width*scaleFactor),int(height*scaleFactor)), Image.ANTIALIAS)
        self.reload()

    def reload(self):
        self.canvas.image = ImageTk.PhotoImage(self.loaded)
        self.img = self.canvas.itemconfig(self.img, image=self.canvas.image)
        
    def client_save(self):
        if (self.loaded):
            filePath = filedialog.asksaveasfilename(initialfile=self.outfile, title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            if (f is None):
                return
            self.loaded.save(filePath)
        else:
            print("Save: No image open")

    def client_reset(self):
        self.loaded.close()
        self.loaded = Image.open(self.infile)
        self.reload()

    def callback(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.rect, x - 10, y - 10, x + 10, y + 10)

root = Window()

root.mainloop()
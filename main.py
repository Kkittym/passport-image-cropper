from tkinter import *
from tkinter import Menu
from tkinter import filedialog
from PIL import ImageTk, Image

class Window(Tk):
    
    def __init__(self):
        super(Window,self).__init__()
        self.openImage = None #PIL image - edited
        self.canvas = None
        self.fileMenu = None
        self.img = None #TK rendered image on canvas
        self.dimensions = (351, 450)
        self.init_window()

    def init_window(self):
        self.title("Image Editor")
        self.createMenu()
        self.createCanvas()

    def createCanvas(self):
        self.canvas = Canvas(self, width=200, height=100)
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0)
        self.canvas.bind('<Motion>', self.rollOver)
        self.canvas.bind('<MouseWheel>', self.zoom)
        self.canvas.bind('<Button-1>', self.cut)
        self.canvas.pack(fill=BOTH, expand=YES)

    def createMenu(self):
        menubar = Menu(self)
        self.config(menu = menubar)
        self.fileMenu = Menu(menubar, tearoff=0)
        self.fileMenu.add_command(label='Open', command=self.client_open)
        self.fileMenu.add_command(label='Close', command=self.client_close, state=DISABLED)
        self.fileMenu.add_command(label='Save', command=self.client_save, state=DISABLED)
        self.fileMenu.add_command(label='reset', command=self.client_reset, state=DISABLED)
        menubar.add_cascade(label='File', menu=self.fileMenu)
        resizeMenu = Menu(menubar, tearoff=0)
        resizeMenu.add_command(label='25%', command=(lambda: self.client_resize(0.25)))
        resizeMenu.add_command(label='50%', command=(lambda: self.client_resize(0.50)))
        resizeMenu.add_command(label='75%', command=(lambda: self.client_resize(0.75)))
        resizeMenu.add_command(label='150%', command=(lambda: self.client_resize(1.5)))
        resizeMenu.add_command(label='200%', command=(lambda: self.client_resize(2)))
        menubar.add_cascade(label='Resize', menu=resizeMenu)
        
    def client_open(self):
        if (self.openImage):
            print("Please close open file before opening a new file")
            return
        try:
            self.infile = filedialog.askopenfilename(title = "Select file", filetypes = (("Image files",".jpg .png .jpeg .bmp .gif"),("all files","*.*")))
            self.openImage = Image.open(self.infile)
        except:
            print("An exception occurred, try opening the file again")
            return
        stringList = self.infile.split('/')
        self.outfile = 'cropped-' + stringList[len(stringList)-1]
        self.reload()
        self.fileMenu.entryconfig(0, state=DISABLED)
        self.fileMenu.entryconfig(1, state=NORMAL)
        self.fileMenu.entryconfig(2, state=NORMAL)
        self.fileMenu.entryconfig(3, state=NORMAL)
        

    def client_close(self):
        if (self.openImage):
            self.openImage.close()
            self.openImage = None
            self.canvas.delete(self.img)
            self.fileMenu.entryconfig(0, state=NORMAL)
            self.fileMenu.entryconfig(1, state=DISABLED)
            self.fileMenu.entryconfig(2, state=DISABLED)
            self.fileMenu.entryconfig(3, state=DISABLED)
        else:
            print("Close: No image open")

    def client_resize(self, scaleFactor):
        width, height = self.openImage.size
        self.openImage = self.openImage.resize((int(width*scaleFactor),int(height*scaleFactor)), Image.ANTIALIAS)
        self.reload()

    def reload(self):
        self.canvas.delete(self.img)
        self.canvas.image = ImageTk.PhotoImage(self.openImage)
        self.img = self.canvas.create_image(0,0, image=self.canvas.image, anchor=NW)
        
    def client_save(self):
        if (self.openImage):
            filePath = filedialog.asksaveasfilename(initialfile=self.outfile, title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            if (f is None):
                return
            self.openImage.save(filePath)
        else:
            print("Save: No image open")

    def client_reset(self):
        self.openImage.close()
        self.openImage = Image.open(self.infile)
        self.reload()

    def rollOver(self, event):
        x, y = event.x, event.y
        (dimx, dimy) = self.dimensions
        self.canvas.coords(self.rect, x-(dimx/2), y-(dimy/2), x+(dimx/2), y+(dimy/2))

    def zoom(self, event):
        x, y, delta = event.x, event.y, event.delta
        value = 10 if (delta > 0) else -10
        value = 0 if (delta == 0) else value
        (dimx, dimy) = self.dimensions
        self.dimensions = (dimx+value, dimy+value)
        (dimx, dimy) = self.dimensions
        self.canvas.coords(self.rect, x-(dimx/2), y-(dimy/2), x+(dimx/2), y+(dimy/2))

    def cut(self, event):
        x, y = event.x, event.y
        (dimx, dimy) = self.dimensions
        box = (x-dimx, y-dimy, x+dimx, y+dimy)
        self.openImage = self.openImage.crop(box)
        self.reload()

root = Window()

root.mainloop()
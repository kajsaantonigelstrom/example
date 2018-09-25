#import Tkinter
#Tkinter._test()

from Tkinter import *
import ttk
from PIL import Image, ImageTk
class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        # create a toplevel menu
        menubar = Menu(root)
        self.master.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Save")
        fileMenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menubar)
        editMenu.add_command(label="Copy")
        editMenu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=editMenu)

        toolbar = Frame(root, bd=1, relief=RAISED)

        self.img = Image.open("exit.png")
        eimg = ImageTk.PhotoImage(self.img)  

        exitButton = Button(toolbar, image=eimg, relief=FLAT,
            command=self.quit)
        exitButton.image = eimg
        exitButton.pack(side=LEFT, padx=2, pady=2)
       
        toolbar.pack(side=TOP, fill=X)
        root.config(menu=menubar)
        self.pack()

        
        self.QUIT = Button(root)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack()

        self.hi_there = Button(root)
        self.hi_there["text"] = 'button with long text',
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack()

        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="text input   ")
        w.pack(side=LEFT)
        self.entrythingy = Entry(f1, width=30)
        self.entrythingy.pack()

        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="multiline input   ")
        w.pack(side=LEFT)
        self.entrythingy = Text(f1, height=4, width=30)
        self.entrythingy.pack()


        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="list   ")
        w.pack(side=LEFT)
        listbox = Listbox(f1, height=4)
        listbox.pack(side=LEFT)
        listbox.insert(END, "alt1")
        for item in ["alt2", "alt3", "alt4", "alt5"]:
            listbox.insert(END, item)
    
        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="combobox   ")
        w.pack(side=LEFT)
        cb = ttk.Combobox(f1, values=("alt1", "alt2", "alt3", "alt4", "alt5"))
        cb.pack(side = RIGHT)

        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="radio   ")
        w.pack(side=LEFT)

        v = IntVar()
        r1 = Radiobutton(f1, text="One", variable=v, value=1)
        r1.pack(side=LEFT);
        r2 = Radiobutton(f1, text="Two", variable=v, value=2)
        r2.pack(side=LEFT);

        f1 = Frame(root)
        f1.pack()
        ttk.Checkbutton(f1).pack(side=LEFT);
        w = Label(f1, text="  toggle")
        w.pack(side=LEFT)

        #w = Scale(root, from_=0, to=100)
        #w.pack()

        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="slider   ")
        w.pack(side=LEFT)
        w = Scale(f1, from_=0, to=200, orient=HORIZONTAL)
        w.pack()

        f1 = Frame(root)
        f1.pack()
        w = Label(f1, text="progress   ")
        w.pack(side=LEFT)
        w = ttk.Progressbar(f1, orient=HORIZONTAL,length=100,  mode='indeterminate')
        w.pack()
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
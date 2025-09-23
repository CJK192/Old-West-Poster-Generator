#Import Needed Libraries
#You guys can import whatever new stuff you want up here
from PIL import Image
from PIL import ImageOps
from tkinter import Tk
from tkinter import filedialog as fd
from tkinter import ttk

root = Tk()
root.title("app")
root.geometry("300x300")

directory = ""

def open_text_file():
    global directory
    directory = fd.askopenfilename()
    print(directory)

def color_correct(dir):
    
    if(dir == ""):
        return 0
    else:
        img = Image.open(dir).convert("L")
        img = ImageOps.colorize(img, black="#24221C", white="#D3B05F")
        img.show()
       
    
       

enter_button = ttk.Button(root, text="Select Image", command=open_text_file)
enter_button.pack()

flip_button = ttk.Button(root, text="Color Correct", command= lambda: color_correct(directory))
flip_button.pack()


root.mainloop()
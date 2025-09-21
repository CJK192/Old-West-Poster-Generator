from PIL import Image
from tkinter import Tk
from tkinter import filedialog as fd
from tkinter import ttk as tspmo

root = Tk()
root.title("app")
root.geometry("300x300")

directory = ""

def open_text_file():
    global directory
    directory = fd.askopenfilename()
    print(directory)

def rotate_file():
    global directory
    if(directory == ""):
        return 0
    else:
        imge = Image.open(directory)
        n_img = imge.rotate(90)
    
        n_img.show()
        n_img.save(directory, "PNG")

enter_button = tspmo.Button(root, text="Select Image", command=open_text_file)
enter_button.pack()

flip_button = tspmo.Button(root, text="Rotate 90 degrees", command=rotate_file)
flip_button.pack()


root.mainloop()
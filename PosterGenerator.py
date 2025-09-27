#Import Needed Libraries
import os
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
from tkinter import Tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import Label
from tkinter import Entry

root = Tk()
root.title("Old West Poster Generator")
root.geometry("400x400")

directory = ""
grain = Image.open("FinalFilmGrain.png").resize((800,800))

def text_maker(img):  
    text = entry.get().strip()
    #test
    print(f"Adding text to image: '{text}'")
    
    if text:
        # draws text
        draw = ImageDraw.Draw(img)
        
        #coordinates
        x = 100  
        y = 700  
        
        
        # Draw white text on top
        draw.text((x, y), text, fill="white")
        
        print("Text successfully added to image!")

def open_text_file():
    global directory
    directory = fd.askopenfilename()
    print(f"Selected image: {directory}")

def color_correct(dir):
    global grain
    if(dir == ""):
        print("Please select an image first!")
        return 0
    else:
        # Open and process the image
        img = Image.open(dir).convert("L").resize((800,800))
        img.paste(grain, (0,0), mask=grain)
        img = ImageOps.colorize(img, black="#24221C", white="#D3B05F")
        
        
        text_maker(img)
        
        # Show the final image
        img.show()

# Create and pack the frame
frame = ttk.Frame(root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

# Put ALL widgets inside the frame
Label(frame, text="Enter poster text:").pack(pady=5)
entry = Entry(frame, width=20, font=("Arial", 12))
entry.pack(pady=10)
entry.insert(0, "WANTED")

enter_button = ttk.Button(frame, text="Select Image", command=open_text_file)
enter_button.pack(pady=10)

flip_button = ttk.Button(frame, text="Generate Poster", command=lambda: color_correct(directory))
flip_button.pack(pady=10)

root.mainloop()
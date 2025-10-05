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

WIDTH = 720
HEIGHT = 1280
FONT_SIZE_1 = 200.0


directory = ""
font_1 = ImageFont.truetype("WildWest.otf", FONT_SIZE_1)
grain = Image.open("FinalFilmGrain.png").resize((800,800))
Template = Image.open("BlankPosterTemplate.png").convert("L").resize((WIDTH, HEIGHT))
TemplateWAmounts = Image.open("PosterWAmounts.png").convert("L").resize((WIDTH, HEIGHT))

def text_maker(img):  
    global font_1
    text = entry.get().strip()
    #test
    print(f"Adding text to image: '{text}'")
    
    if text:
        # draws text
        # :)
        draw = ImageDraw.Draw(img)
        
        

        if(len(text) > 6):
            print("Stopped About where ou think")
            font_1 = ImageFont.truetype("WildWest.otf", FONT_SIZE_1 - 8 * (len(text) - 6))
        else:
            font_1 = ImageFont.truetype("WildWest.otf", FONT_SIZE_1)

        
        text_len = draw.textlength(text, font=font_1)
        
        # Draw white text on top
        print("Stopped here lmao")
        draw.text((int(WIDTH / 2 - (text_len / 2)), int(((HEIGHT / 4)) * 3)), text, fill="black", font=font_1)
        
       # Ay respectfully imma comment this out 
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
        badimg = Image.open(dir)
        img = ImageOps.exif_transpose(badimg).convert("L").resize((int(WIDTH / 2), int(HEIGHT * (5/12))))
        img.paste(grain, (0,0), mask=grain)
        img = ImageOps.colorize(img, black="#24221C", white="#D3B05F")
        temp = ImageOps.colorize(Template, black="#24221C", white="#D3B05F")

        #Bro it centers it ik it looks wierd but chill it lets us change the size of the poster
        temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (5/12)) / 2))))
        text_maker(temp)
        temp.show()
        
        
        
        # Show the final image
        

# Create and pack the frame
frame = ttk.Frame(root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

# Put ALL widgets inside the frame
Label(frame, text="Enter Name:").pack(pady=5)
entry = Entry(frame, width=20, font=("Arial", 12))
entry.pack(pady=10)
entry.insert(0, "")

enter_button = ttk.Button(frame, text="Select Image", command=open_text_file)
enter_button.pack(pady=10)

flip_button = ttk.Button(frame, text="Generate Poster", command=lambda: color_correct(directory))
flip_button.pack(pady=10)

root.mainloop()
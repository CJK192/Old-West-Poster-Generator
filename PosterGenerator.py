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

directory = ""
grain = Image.open("FinalFilmGrain.png").resize((800,800))
Template = Image.open("BlankPosterTemplate.png").convert("L").resize((WIDTH, HEIGHT))

#Draws text onto img at (ypos/100) the way down the image with customizable margins, font-size, font, and color
#IMPORTANT: ypos is like a slider from 0-100, 100 being at the bottom, 0 being at the top. NOT A MEASURE OF PIXELS!!

def draw_text(text, img, ypos, margin=80, font_size=200.0, font="WildWest.otf", font_color="black"):  

    global WIDTH

    draw = ImageDraw.Draw(img)
    text_len = draw.textlength(text, font=ImageFont.truetype(font, font_size))

    if(text_len > WIDTH - margin * 2):
        new_font_size = font_size
        while(text_len > WIDTH - margin * 2):
            new_font_size -= 1
            text_len = draw.textlength(text, font=ImageFont.truetype(font, new_font_size))
        draw.text((int(WIDTH / 2 - (text_len / 2)), int(((HEIGHT / 100)) * ypos)), text, fill=font_color, font=ImageFont.truetype(font, new_font_size))
    else:
         draw.text((int(WIDTH / 2 - (text_len / 2)), int(((HEIGHT / 100)) * ypos)), text, fill=font_color, font=ImageFont.truetype(font, font_size))
    
   


def open_text_file():
    global directory
    directory = fd.askopenfilename()

def color_correct(dir):
    global grain

    if(dir == ""):
        print("Please select an image first!")
        return 0
    else:
        # Open and process the image
        badimg = Image.open(dir)
        img = ImageOps.exif_transpose(badimg).convert("L").resize((int(WIDTH / 2), int(HEIGHT * (9/24))))
        img.paste(grain, (0,0), mask=grain)
        img = ImageOps.colorize(img, black="#24221C", white="#D3B05F")
        temp = ImageOps.colorize(Template, black="#24221C", white="#D3B05F")

        #Bro it centers it ik it looks wierd but chill it lets us change the size of the poster
        temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))
        draw_text(name_entry.get().strip(), temp, 70)
        draw_text(location_entry.get().strip(), temp, 83, font_size=100.0)
        draw_text(f"${bounty_entry.get().strip()}", temp, 90)
        
        temp.show()
        
        
        
        # Show the final image
        

# Create and pack the frame
frame = ttk.Frame(root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

# Put ALL widgets inside the frame
Label(frame, text="Choose a template:").pack(pady=5)
template_options = ["template1", "template2", "template3", "template4", "template5"]
dropdown = ttk.Combobox(frame, values=template_options)
dropdown.current(0)  # Set default value
dropdown.pack(pady=10)
selected_template = dropdown.get()

Label(frame, text="Enter Name:").pack(pady=3)
name_entry = Entry(frame, width=20, font=("Arial", 12))
name_entry.pack(pady=5)
name_entry.insert(0, "")

Label(frame, text="Enter Location:").pack(pady=3)
location_entry = Entry(frame, width=20, font=("Arial", 12))
location_entry.pack(pady=5)
location_entry.insert(0, "")

Label(frame, text="Enter Bounty in Dollars (You don't need the $ sign):").pack(pady=3)
bounty_entry = Entry(frame, width=20, font=("Arial", 12))
bounty_entry.pack(pady=5)
bounty_entry.insert(0, "")

enter_button = ttk.Button(frame, text="Select Image", command=open_text_file)
enter_button.pack(pady=10)

flip_button = ttk.Button(frame, text="Generate Poster", command=lambda: color_correct(directory))
flip_button.pack(pady=10)

root.mainloop()
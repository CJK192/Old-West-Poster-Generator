#Import Needed Libraries/Modules
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

#Initialize Tkinter window and give a name and dimensions

root = Tk()
root.title("Old West Poster Generator")
root.geometry("400x400")

#Contants for Width and Height of poster

WIDTH = 720
HEIGHT = 1280

#Initialize directory of portrait. Will be selected by user later in the program

directory = ""

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
    
   
#Formats img correctly, can change dimensions, black and white point, add grain and even change the directory of grain
#All parameters except img optional (They come with default values)

def filter_image(img, width=int(WIDTH / 2), height=int(HEIGHT * (9/24)), white_point="#D3B05F", black_point="#24221C", grain=False, grain_directory="FinalFilmGrain.png"):
    bad_format = Image.open(img)
    good_format = ImageOps.exif_transpose(bad_format).convert("L").resize((width, height))
    if(grain):
        good_format.paste(Image.open(grain_directory).resize((width, height)), (0,0), mask=Image.open(grain_directory).resize((width, height)))
    good_format = ImageOps.colorize(good_format, black=black_point, white=white_point)
    return good_format

#sets global directory variable (for portrait image) to file path of user's choice

def open_text_file():
    global directory
    directory = fd.askopenfilename()


#Allows for template selection with optimization
#Template is the directory (string) of the template, portait is the directory (string) of the pic you wanna use

def create_poster(template, portrait):
    global grain

    match template:
        case "":  
            print("Please select an image first!")
            return 0
        case "Template_1":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("BlankPosterTemplate.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case "Template_2":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("1.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case "Template_3":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("2.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case "Template_4":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("3.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case "Template_5":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("4.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case "Template_6":
    
            img = filter_image(portrait, grain=True)
            temp = filter_image("5.png", width=WIDTH, height=HEIGHT)

            temp.paste(img, (int((WIDTH / 2) - ((WIDTH / 2) / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2))))

            draw_text(name_entry.get().strip(), temp, 70)
            draw_text(location_entry.get().strip(), temp, 80, font_size=100.0)
            draw_text(f"${bounty_entry.get().strip()}", temp, 88)
            
            temp.show()

        case _:

            print("Please select a valid template!")
        

# Create and pack the frame
frame = ttk.Frame(root)
frame.pack(pady=20, padx=20, fill='both', expand=True)

#Template dropdown to select template
Label(frame, text="Choose a template:").pack(pady=5)
template_options = ["Template_1", "Template_2", "Template_3", "Template_4", "Template_5"]
dropdown = ttk.Combobox(frame, values=template_options)
dropdown.current(0)  # Set default value
dropdown.pack(pady=10)

#Entry for name
Label(frame, text="Enter Name:").pack(pady=3)
name_entry = Entry(frame, width=20, font=("Arial", 12))
name_entry.pack(pady=5)
name_entry.insert(0, "")

#Entry for location
Label(frame, text="Enter Location:").pack(pady=3)
location_entry = Entry(frame, width=20, font=("Arial", 12))
location_entry.pack(pady=5)
location_entry.insert(0, "")

#Entry for bounty
Label(frame, text="Enter Bounty in Dollars (You don't need the $ sign):").pack(pady=3)
bounty_entry = Entry(frame, width=20, font=("Arial", 12))
bounty_entry.pack(pady=5)
bounty_entry.insert(0, "")

#Button for selecting directory for portrait image
select_button = ttk.Button(frame, text="Select Image", command=open_text_file)
select_button.pack(pady=10)

#Button to finnally assemble and open poster in a new window
create_button = ttk.Button(frame, text="Generate Poster", command=lambda: create_poster(dropdown.get(), directory))
create_button.pack(pady=10)


root.mainloop()
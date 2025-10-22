
import os
import cv2
from deepface import DeepFace
from tkinter import filedialog as fd
from ttkthemes import ThemedTk
from tkinter import Tk, Label, Entry, Button, PhotoImage, StringVar, ttk, OptionMenu
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageTk

#pip3 install pillow-heif
from pillow_heif import register_heif_opener

from google import genai
from io import BytesIO

# Configure the client with your API key
client = genai.Client(api_key="AIzaSyBCzw3NGQhjfNlydeCyW0N-9Itx1F9ZxtY")

#This needs to be run to get HEIF file support
register_heif_opener()

#Initialize Tkinter window and give a name and dimensions
root = ThemedTk()
root.title("Old West Poster Generator")
root.geometry("500x550")


root.set_theme("default")
root.configure(bg='#2B1B17') 


# Load background image
background_image = Image.open("background.jpg")
background_image = background_image.resize((500, 550), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_photo

#Contants for Width and Height of poster
WIDTH = 720
HEIGHT = 1000


#Initialize directory of portrait. Will be selected by user later in the program
directory = ""

#Draws text onto img at (ypos/1280) the way down the image with customizable margins, font-size, font, and color

def draw_text(text, img, ypos, margin=80, font_size=145.0, font="WildWest.otf", font_color="black"): 

   global WIDTH

   draw = ImageDraw.Draw(img)
  
   text_len = draw.textlength(text=text, font=ImageFont.truetype(font, font_size))
   text_height = ImageFont.truetype(font, font_size).getbbox(text=text)[3] - ImageFont.truetype(font, font_size).getbbox(text=text)[1]

   if(text_len > WIDTH - margin * 2):
       new_font_size = font_size
       while(text_len > WIDTH - margin * 2):
           new_font_size -= 1
           text_len = draw.textlength(text, font=ImageFont.truetype(font, new_font_size))


       text_height = ImageFont.truetype(font, new_font_size).getbbox(text=text)[3] - ImageFont.truetype(font, new_font_size).getbbox(text=text)[1]
       draw.text((int(WIDTH / 2 - (text_len / 2)), int((ypos/1280) * HEIGHT) - (text_height / 2)), text, fill=font_color, font=ImageFont.truetype(font, new_font_size))
   else:
        draw.text((int(WIDTH / 2 - (text_len / 2)), int((ypos/1280) * HEIGHT) - (text_height / 2)), text, fill=font_color, font=ImageFont.truetype(font, font_size))
  
def edit_image(image):
    prompt = prompt_entry.get()
    if prompt == "":
        return image
    image = Image.open(image)
    response = client.models.generate_content(
        model = "gemini-2.5-flash-image",
        contents=[prompt, image],
    )
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            edited_image = Image.open(BytesIO(part.inline_data.data))
            edited_image.save("edited_image.png")
            return "edited_image.png"

#Formats img correctly, can change dimensions, black and white point, add grain and even change the directory of grain
#All parameters except img optional (They come with default values)

def filter_image(img, width=int(WIDTH * (2/3)), height=int(HEIGHT * (11/24)), white_point="#D3B05F", black_point="#24221C", grain=False, grain_directory="FinalFilmGrain.png"):
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

def crop_face(face, x=0, y=0):

    heic_image = Image.open(face)
    heic_image.save("temp_converted_image.png", format="PNG")

    detected_faces = DeepFace.extract_faces(img_path="temp_converted_image.png", enforce_detection=False)

    for face_info in detected_faces:
        facial_area = face_info['facial_area']
        face_x = facial_area['x']
        face_y = facial_area['y']
        face_w = facial_area['w']
        face_h = facial_area['h']

    cropped_face = Image.open(face).crop((face_x - x, face_y - y, face_x + face_w + x, face_y + face_h + y))
    cropped_face.save("temp_cropped_face.png", format="PNG")
    return "temp_cropped_face.png"

#This needs to be initialized here to be changed in the create poster function

select_button = ttk.Button(root, text="Select Image", command=open_text_file)

#Allows for template selection with optimization
#Template is the directory (string) of the template, portait is the directory (string) of the pic you wanna use


def create_poster(template, portrait):

    global grain

    if(portrait == ""):
        select_button.config(text="Please select an image!")
    else:
       
        
        
        match template:
            case "": 
                print("Please select an image first!")
                return 0
            case "Template_1":
        
                img = filter_image(crop_face(edit_image(portrait), 67, 67), grain=True)
                temp = filter_image("BlankPosterTemplate.png", width=WIDTH, height=HEIGHT)

                temp.paste(img, (int((WIDTH / 2) - (img.width / 2)), int((HEIGHT / 2) - ((HEIGHT  * (11/24)) / 2)) - 7))

                draw_text(name_entry.get().strip(), temp, 1003)
                draw_text(location_entry.get().strip(), temp, 1113, font_size=98.0)
                draw_text(f"${bounty_entry.get().strip()}", temp, 1220, font_size=115)
                temp.save("GeneratedPoster.png")

                

                
                temp.show()


            case "Template_2":
        
                img = filter_image(crop_face(edit_image(portrait), 67, 67), grain=True, height=int(HEIGHT * (11/24)) - 20)
                temp = filter_image("1.png", width=WIDTH, height=HEIGHT)


                temp.paste(img, (int((WIDTH / 2) - (img.width / 2)), int((HEIGHT / 2) + 62 - ((HEIGHT  * (9/24)) / 2))))


                draw_text(name_entry.get().strip(), temp, 1100, font_size=100, font_color="#CEC9BE", margin=110)
                draw_text(location_entry.get().strip(), temp, 1190, font_size=100.0, font_color="#CEC9BE", margin=110)
                draw_text(f"REWARD: ${bounty_entry.get().strip()}", temp, 413, font_size=90, margin=95)
                
                temp.show()


            case "Template_3":
        
                img = filter_image(crop_face(edit_image(portrait),  67, 67), grain=True, width=int(WIDTH * (2/3)) - 70, height=int(HEIGHT * (11/24)) - 90)
                temp = filter_image("2.png", width=WIDTH, height=HEIGHT)


                temp.paste(img, (int((WIDTH / 2) - (img.width / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2)) - 20))


                draw_text(name_entry.get().strip(), temp, 925, font_size=100, margin=145)
                draw_text(location_entry.get().strip(), temp, 1050, font_size=90.0, font_color="#CEC9BE", margin=145)
                draw_text(f"${bounty_entry.get().strip()} REWARD", temp, 1190, font_size=115, margin=85)
                
                temp.show()


            case "Template_4":
        
                img = filter_image(crop_face(edit_image(portrait), 67, 67), grain=True, width=int(WIDTH * (2/3)) - 20, height=int(HEIGHT * (11/24)) - 35)
                temp = filter_image("3.png", width=WIDTH, height=HEIGHT)


                temp.paste(img, (int((WIDTH / 2) - (img.width / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2)) + 30))


                draw_text(name_entry.get().strip(), temp, 1125 , margin=110, font_size=105)
                draw_text(location_entry.get().strip(), temp, 1025, font_size=90.0, margin=130)
                draw_text(f"REWARD: ${bounty_entry.get().strip()}", temp, 365, font_size=115, margin=130)
                
                temp.show()


            case "Template_5":
        
                img = filter_image(crop_face(edit_image(portrait), 67, 67), grain=True, width=int(WIDTH * (2/3)) - 55, height=int(HEIGHT * (11/24)) - 70)
                temp = filter_image("4.png", width=WIDTH, height=HEIGHT)


                temp.paste(img, (int((WIDTH / 2) - (img.width / 2)), int((HEIGHT / 2) - ((HEIGHT  * (9/24)) / 2)) + 50))


                draw_text(name_entry.get().strip(), temp, 397, font_size=120, margin= 140)
                draw_text(location_entry.get().strip(), temp, 1024, font_size=90.0, font_color="#CEC9BE", margin= 140)
                draw_text(f"${bounty_entry.get().strip()}", temp, 1180, font_size=105, margin= 105)
                
                temp.show()
            case _:


                print("Please select a valid template!")


# Use system default colors 
label_bg = 'SystemButtonFace'  

#Template dropdown to select template

template_options = ["Template_1", "Template_2", "Template_3", "Template_4", "Template_5"]
var = StringVar(value=template_options[0])
images = {t: PhotoImage (file="BlankPosterTemplate.png" if t == "Template_1" else
                        "1.png" if t == "Template_2" else
                        "2.png" if t == "Template_3" else
                        "3.png" if t == "Template_4" else
                        "4.png").subsample(12,12) for t in template_options}


def change_image(*_):
  img = images[var.get()]
  image_label.config(image=img)
  image_label.image = img


Label(root, text="Choose a template:", bg=label_bg, fg="black", font=('Arial', 14)).pack(pady=10)
dropdown = OptionMenu(root, var, *template_options, command=change_image)
dropdown.pack()
image_label = ttk.Label(root)
image_label.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

change_image()

#stores selected value
selected_value = var.get() 


#Entry for name
Label(root, text="Enter Name:", bg=label_bg, fg='black', font=('Arial', 14)).place(relx=0.5, rely=0.22, anchor='center')
name_entry = Entry(root, width=20, font=("Arial", 12))
name_entry.place(relx=0.5, rely=0.27, anchor='center')
name_entry.insert(0, "")

#Entry for location
Label(root, text="Enter Location:", bg=label_bg, fg='black', font=('Arial', 14)).place(relx=0.5, rely=0.34, anchor='center')
location_entry = Entry(root, width=20, font=("Arial", 12))
location_entry.place(relx=0.5, rely=0.39, anchor='center')
location_entry.insert(0, "")


#Entry for bounty
Label(root, text="Enter Bounty in Dollars:", bg=label_bg, fg='black', font=('Arial', 14)).place(relx=0.5, rely=0.46, anchor='center')
bounty_entry = Entry(root, width=20, font=("Arial", 12))
bounty_entry.place(relx=0.5, rely=0.51, anchor='center')
bounty_entry.insert(0, "")

Label(root, text="Enter Prompt", bg=label_bg, fg='black', font=('Arial', 14)).place(relx=0.5, rely=0.75, anchor='center')
prompt_entry = Entry(root, width=20, font=("Arial", 12))
prompt_entry.place(relx=0.5, rely=0.8, anchor='center')
prompt_entry.insert(0, "")

#Button for selecting directory for portrait image
select_button.place(relx=0.5, rely=0.70, anchor='center')


#Button to finnally assemble and open poster in a new window
create_button = ttk.Button(root, text="Generate Poster", command=lambda: create_poster(var.get(), directory))
create_button.place(relx=0.5, rely=0.85, anchor='center')


root.mainloop()


import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QWidget
import os
from audio_folder_picker import FolderPickerDialog
from image_picker import ImagePickerDialog
from style_selector_image_title import ImageTitleFormatter
from bottom_bar_formatter import BottomBarFormatter
from alert_window import show_alert
from image_selector import ImageSelector
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from embed_artwork import embed_artwork

BOTTOM_BAR_HEIGHT = 143
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 800

def get_data():
    app = QApplication([])
    data = {
        "audio_folder": None,
        "image_path": None,
        "title": {
        "color": None,
        "position": None,
        "font_family": None,
        "font_size": None,
        "word_spacing": None,
        "casing": None,
        },
        "bottom_bar": {
            "color": None,
            "font_family": None,
            "font_size": None,
            "word_spacing": None,
            "casing": None,
        },
        "darkness": None,
        "aspect_ratio": None,
    }
    # Create the folder picker dialog and get the selected folder
    audio_folder_picker = FolderPickerDialog()
    if audio_folder_picker.exec_() == QDialog.Accepted:
        audio_folder = audio_folder_picker.get_selected_folder()
        if os.path.exists(audio_folder) and os.path.isdir(audio_folder):
            if len([name for name in os.listdir(audio_folder) if name.endswith((".mp3", ".m4a"))]) > 0:
                data["audio_folder"] = audio_folder
            else:
                show_alert("No audio files found in the selected folder")
                sys.exit()
        else:
            show_alert("Invalid folder path")
            sys.exit()
    else:
        # show_alert("No folder selected")
        sys.exit()
    
    # Create the image picker dialog and get the selected image
    image_picker = ImagePickerDialog()
    if image_picker.exec_() == QDialog.Accepted:
        image_path = image_picker.get_selected_image()
        if os.path.exists(image_path) and os.path.isfile(image_path) and image_path.endswith(("png", "jpg", "jpeg")):
            data["image_path"] = image_path
        else:
            show_alert("Invalid image path")
            sys.exit()
    else:
        # show_alert("No image selected")
        sys.exit()

    # Create the font style selector, text location selector, color picker, and image preview for slected crop method defined in image_preview.py and image darkener defined in darken_preview.py all these in a single window
    image_title_formatter = ImageTitleFormatter()
    image_title_formatter.show()
    
    if image_title_formatter.exec_() == QDialog.Accepted:
        title_data = image_title_formatter.get_all_data()
        data["title"] = title_data
    else:
        sys.exit()
    
    # Create the bottom bar formatter
    bottom_bar_formatter = BottomBarFormatter()
    bottom_bar_formatter.show()
    if bottom_bar_formatter.exec_() == QDialog.Accepted:
        bottom_bar_data = bottom_bar_formatter.get_all_data()
        data["bottom_bar"] = bottom_bar_data
    else:
        sys.exit()

    # Create the darkner and image preview
    image_selector = ImageSelector(data["image_path"])
    image_selector.show()
    if image_selector.exec_() == QDialog.Accepted:
        image_selector_data = image_selector.get_all_data()
        data["darkness"] = image_selector_data["darkness_level"]
        data["aspect_ratio"] = image_selector_data["aspect_ratio_option"]
    else:
        sys.exit()


    return data

def smart_center_crop(image, new_size):
    '''
        new_size is a tuple (width, height)
    '''
    width, height = image.size
    new_width, new_height = new_size

    scale_w = new_width / width
    scale_h = new_height / height
    final_scale = max(scale_w, scale_h)
    new_image = image.resize((int(width * final_scale), int(height * final_scale)))
    extra_x = (width*final_scale - new_width) / 2
    extra_y = (height*final_scale - new_height) / 2
    new_image = new_image.crop((extra_x, extra_y, extra_x + new_width, extra_y + new_height))
    return new_image

def extract_date(string):
    '''
        This method extracts the date from the string
        The allowed formats are as follows: 
            - MM-DD-YYYY
            - YYYY-MM-DD
            - MM_DD_YYYY
            - YYYY_MM_DD
    '''
    import re
    file_extention = string.split(".")[-1]
    string = string.strip().replace(f".{file_extention}", "")
    pattern = r'(\d{2,4})[-_/](\d{2})[-_/](\d{2,4})'
    match = re.search(pattern, string)
    # Extract the date and split the text before and after the date
    if match:
        date_str = match.group(0)  # The entire matched date string
        parts = string.split(date_str, 1)  # Split at the first occurrence of date
        before_text = parts[0].strip().strip("-").strip(" ") if parts[0] else ""
        after_text = parts[1].strip().strip("-").strip(" ") if len(parts) > 1 else ""
        text_parts = [before_text, f"\"{after_text}\"" if after_text else ""]
        if len(match.group(1)) == 4: # if the first is 4 digits, then it is the year, then it is in this format YYYY-MM-DD
            return match.group(3), match.group(2), match.group(1), text_parts # return the day, month, year, and the text parts
        elif len(match.group(1)) == 2: # if the first is 2 digits, then it is the month, then it is in this format MM-DD-YYYY
            return match.group(2), match.group(1), match.group(3), text_parts # return the day, month, year, and the text parts
        else:
            return None, None, None, ["", ""]   

def apply_image_modifications(data):

    '''
        This method applies the image modifications to the image
        The modifications are as follows:
            - Darken the image
            - Crop the image
            - Add the bottom bar
        This is the base image over which different titles will be written
    '''

    with Image.open(data["image_path"]) as image:

        # darken the image
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(data["darkness"])

        # crop the image
        crop_method = data["aspect_ratio"]
        if crop_method == "crop": # not actually crop
            image = smart_center_crop(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        elif crop_method == "stretch":
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        elif crop_method == "do_nothing":
            scale_factor = min(IMAGE_WIDTH/image.width, IMAGE_HEIGHT/image.height)
            if scale_factor < 1:
                image = image.resize((int(image.width*scale_factor), int(image.height*scale_factor)))
            canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
            canvas.paste(image, (int(IMAGE_WIDTH/2-image.width/2), int(IMAGE_HEIGHT/2-image.height/2 - BOTTOM_BAR_HEIGHT/2)))
            image = canvas
        # Add the bottom bar
        draw = ImageDraw.Draw(image)
        color = data["bottom_bar"]["color"]
        if color == "random":
            color = genRandomColor()
        draw.rectangle((0, IMAGE_HEIGHT-BOTTOM_BAR_HEIGHT, IMAGE_WIDTH, IMAGE_HEIGHT), fill=color)
        image.save("output.png")
        # data["image_path"] = "output.png"
        return "output.png", color

def get_px_size(text, font_family, font_size):
    '''
        This method returns the size of the font in pixels
    '''
    font = ImageFont.truetype(font_family, font_size)
    box = font.getbbox(text)
    height = box[3] + box[1]  # we are adding because there is margin at top and bottom and margin is equal to the top value
    width = box[2] + box[0] 
    return width, height

def genRandomColor():
    '''
        This method generates a random color
    '''
    color=  "#" + ''.join([random.choice('0123456789abcdef') for _ in range(6)])
    print(color)
    return color

def write_on_bottom_bar(data, date : tuple, file_name : str):
    '''
        This method writes the date on the image and saves it with a new name
    '''
    path, color = apply_image_modifications(data)
    with Image.open(path) as image:
        draw = ImageDraw.Draw(image)
        DD, MM, YYYY, [heading, subheading] = date
        date_str=f"{MM}-{DD}-{YYYY}"
        date_width, date_height = get_px_size(date_str, data["bottom_bar"]["font_family"], data["bottom_bar"]["font_size"])

        ## Printing the date on the bottom bar
        bottom_text_color = "black"
        # Check if the background color is dark, then use white text
        bg_color = color
        # Convert hex to RGB if it's a hex color
        if bg_color.startswith("#"):
            r = int(bg_color[1:3], 16)
            g = int(bg_color[3:5], 16)
            b = int(bg_color[5:7], 16)
            # Calculate perceived brightness (common formula)
            brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            if brightness < 0.5:  # If background is dark
                bottom_text_color = "white"
        font = ImageFont.truetype(data["bottom_bar"]["font_family"], data["bottom_bar"]["font_size"])
        draw.text((IMAGE_WIDTH/2-date_width/2, IMAGE_HEIGHT-BOTTOM_BAR_HEIGHT+(BOTTOM_BAR_HEIGHT/2-date_height/2)), date_str, fill=bottom_text_color, font=font)
        image.save(f"{os.path.join(data['audio_folder'], file_name)}")
        return f"{os.path.join(data['audio_folder'], file_name)}"

def wrap_text(text, font_family, font_size, max_width):
    '''
        This method wraps the text to the correct width
    '''
    max_width = max_width*0.9
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if get_px_size(current_line + " " + word, font_family, font_size)[0] <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
        current_line = current_line.strip()
        print(current_line, get_px_size(current_line, font_family, font_size)[0])
    if current_line:
        lines.append(current_line)
    return lines

def draw_text_on_image(position, text, data, image):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(data["title"]["font_family"], data["title"]["font_size"])
    draw.text(position, text, fill=data["title"]["color"], font=font)
    return image, (position[0], position[1] + get_px_size(text, data["title"]["font_family"], data["title"]["font_size"])[1])

def place_text_on_image(data, heading_lines, subheading_lines, image_path):
    '''
        "top-left",
        "top-center",
        "top-right",
        "middle-left",
        "middle-center",
        "middle-right",
        "bottom-left",
        "bottom-center",
        "bottom-right"
        returns the position of the text in the image
        returns a tuple of the x and y coordinates
        (x, y)
    '''

    total_height = 0    
    for line in heading_lines:
        total_height += get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[1]
    for line in subheading_lines:
        total_height += get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[1]

    with Image.open(image_path) as image:
        if data["title"]["position"]["position_name"] == "top-left":
            x,y = 0,0
            for line in heading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "top-center":
            y=0
            for line in heading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "top-right":
            y=0
            for line in heading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "middle-left":
            x = 0
            y = (IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height)/2
            for line in heading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "middle-center":
            y = (IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height)/2
            for line in heading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "middle-right":
            y = (IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height)/2
            for line in heading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "bottom-left":
            x,y = 0, IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height
            for line in heading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "bottom-center":
            y = IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height
            for line in heading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = (IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0])/2
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        elif data["title"]["position"]["position_name"] == "bottom-right":
            y = IMAGE_HEIGHT - BOTTOM_BAR_HEIGHT - total_height
            for line in heading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
            for line in subheading_lines:
                x = IMAGE_WIDTH - get_px_size(line, data["title"]["font_family"], data["title"]["font_size"])[0]
                image, (x,y) = draw_text_on_image((x,y), line, data, image)
        image.save(image_path)
        
def get_casing_text(text, casing):
    if casing == "Normal":
        return text
    elif casing == "UPPERCASE":
        return text.upper()
    elif casing == "lowercase":
        return text.lower()
    elif casing == "Capitalize":
        data = text.split(" ")
        for i in range(len(data)):
            data[i] = data[i].capitalize()
        return " ".join(data)
    else:
        return text

if __name__ == "__main__":
    data = get_data()
    print(data)
    # data = {
    #     'audio_folder': '/Users/vardan/Code/fiverr/Xjhon/audio-imager/dummy_data',
    #     'image_path': '/Users/vardan/Code/fiverr/Xjhon/audio-imager/program-files/test.jpg', 
    #     'title': {
    #         'color': '#ffffff', 
    #         'font_family': 'Arial', 
    #         'font_size': 50, 
    #         'word_spacing': 1.0, 
    #         'casing': 'Normal',    
    #         'position': {
    #             'type': 'preset', 
    #             'preset_id': 1, 
    #             'position_name': 'top-left', 
    #             'row': 0, 
    #             'col': 0
    #         }
    #         }, 
    #     'bottom_bar': {
    #         'color': '#ff8000', 
    #         'font_family': '/Users/vardan/Library/Fonts/JetBrainsMono-Regular.ttf', 
    #         'font_size': 67, 
    #         'word_spacing': 1.0, 
    #         'casing': 'Normal'
    #     }, 
    #     'darkness': 0.25, 
    #     'aspect_ratio': 'do_nothing'
    # }
    audio_files = [file for file in os.listdir(data["audio_folder"]) if file.endswith((".mp3", ".m4a"))]
    for file in audio_files:
        file_extention = file.split(".")[-1]
        DD, MM, YYYY, [heading, subheading] = extract_date(file)
        # data = apply_image_modifications(data)
        file_path = write_on_bottom_bar(data, (DD, MM, YYYY, [heading, subheading]), f"{file.replace(file_extention,'png')}")

        heading = get_casing_text(heading, data["title"]["casing"])
        subheading = get_casing_text(subheading, data["title"]["casing"])

        heading_lines = wrap_text(heading, data["title"]["font_family"], data["title"]["font_size"], IMAGE_WIDTH)
        subheading_lines = wrap_text(subheading, data["title"]["font_family"], data["title"]["font_size"], IMAGE_WIDTH)
        place_text_on_image(data, heading_lines, subheading_lines, file_path)
        embed_artwork(data["audio_folder"])
       

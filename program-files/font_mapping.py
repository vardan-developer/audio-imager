import matplotlib.font_manager
from PIL import ImageFont
import os

def get_fonts_mapping():
    fonts_mapping = {}
    paths_to_check = [os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"), os.path.expanduser("~/Library/Fonts"), os.path.expanduser("C:/WINDOWS/FONTS")] if os.name == "nt" else [os.path.expanduser("~/Library/Fonts")]
    
    font_paths = [path for path in matplotlib.font_manager.findSystemFonts(fontpaths=paths_to_check) if "Emoji" not in path and "18030" not in path]

    for font_path in font_paths:
        try:
            font = ImageFont.FreeTypeFont(font_path)
            name, weight = font.getname()
            fonts_mapping[(name, weight)] = font_path
        except Exception as e:
            print(f'Error: could not load font {font_path}')
    return fonts_mapping





if __name__ == "__main__":
    import json
    fonts_mapping = get_fonts_mapping()
    new_fonts_mapping = {}
    for key, value in fonts_mapping.items():
        new_key = key[0]
        if new_key not in new_fonts_mapping:
            new_fonts_mapping[new_key] = []
        new_fonts_mapping[new_key].append([value, key[1]])
    with open("fonts_mapping.json", "w") as f:
        json.dump(new_fonts_mapping, f, indent=4)
    print(new_fonts_mapping)
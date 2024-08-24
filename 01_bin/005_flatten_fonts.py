from fontTools.ttLib import TTFont
import os
import glob
import shutil

font_input_dir = r"C:\Users\ezraameri\Downloads\nerd-fonts-3.2.1\nerd-fonts-3.2.1\patched-fonts"
font_out_dir = r"C:\Users\ezraameri\Downloads\flat"

os.makedirs(font_out_dir, exist_ok=True)
for font_group in os.listdir(font_input_dir):
    font_group_dir = font_input_dir + "\\" + font_group
    all_fonts = glob.glob(font_group_dir + "\\**\\*.ttf", recursive=True)
    for font_path in all_fonts:
        shutil.copy2(font_path, font_out_dir)
    print("done", font_group)
print("all done")

# then copy to the c:\windows\fonts directory

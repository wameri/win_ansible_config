import os
import ctypes
import ctypes as ct
from ctypes import wintypes as w

from PIL import Image
from PIL import ImageDraw
import shutil
from PIL import ImageFont
import yaml

from argparse import ArgumentParser as AP

def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    return parser.parse_args()

class Main:
    def __init__(self):
        self.args = parse_args()
        self.config = yaml.load(open(self.args.config, 'r'), Loader=yaml.FullLoader)
        self.image_dir = self.config["win_background_configs"]["image_dir"]
        self.output_dir = self.config["win_background_configs"]["output_dir"]
        self.font_name = os.getenv('LOCALAPPDATA') +  r"\Microsoft\Windows\Fonts\\" + self.config["win_background_configs"]['font_name']
        self.font_size = self.config["win_background_configs"]['font_size']
        self.image_fraction = self.config["win_background_configs"]['image_fraction']

        os.makedirs(self.output_dir, exist_ok=True)
        self.create_backgrounds()

    def create_backgrounds(self):
        for background in self.config["win_backgrounds"]:
            caption = background['name']
            input_image = os.path.join(os.path.abspath(self.image_dir), background['image'])
            output_image = self.create_background(input_image, caption)
            background['output_image'] = output_image

    def create_background(self, input_image, caption):
        output_path = os.path.join(os.path.abspath(self.config['win_background_configs']['output_dir']), caption.replace(" ", "") +".jpg")

        if os.path.exists(output_path):
            os.remove(output_path)
        img = Image.open(input_image)
        I1 = ImageDraw.Draw(img)

        myFont = ImageFont.truetype(self.font_name, self.font_size)
        while myFont.getbbox(caption)[2] < self.image_fraction * img.size[0]:
            self.font_size += 1
            myFont = ImageFont.truetype(self.font_name, self.font_size)

        bbox = myFont.getbbox(caption)
        text_len = bbox[2]
        text_width = bbox[3]
        x = max(0, img.size[0] / 2 - text_len / 2)
        y = max(0, img.size[1] / 5 - text_width / 2)
        shadow = 10

        I1.text((x, y + shadow), caption, font=myFont, fill=(219, 215, 185))
        I1.text((x + shadow, y), caption, font=myFont, fill=(54, 54, 71))

        img.save(output_path)
        return output_path

    def get_current_wallpaper(self):
        self.SPI_GETDESKWALLPAPER = 0x0073
        self.dll = ct.WinDLL("user32")
        self.dll.SystemParametersInfoW.argtypes = w.UINT, w.UINT, w.LPVOID, w.UINT
        self.dll.SystemParametersInfoW.restype = w.BOOL

        path = ct.create_unicode_buffer(260)
        result = self.dll.SystemParametersInfoW(self.SPI_GETDESKWALLPAPER, ct.sizeof(path), path, 0)
        print(f'current walpaper path {result}, {path.value}')
        return path.value

    def set_backgrounds(self):
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDWININICHANGE = 0x02

        for background in self.config["win_backgrounds"]:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, background["output_image"], SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)  # 0

application = Main()

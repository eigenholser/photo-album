from __future__ import print_function
import argparse
import logging
import os
from PIL import (Image, ImageDraw, ImageFont, ImageEnhance)
import sys


logger = logging.getLogger(__name__)


class Caption(object):
    """
    Read the source file. Create a caption with semi-transparent backcground
    for contrast. Paste the caption over the source image. Flatten and save.
    This offers the illusion of transparency in the RGB image that does not
    support transparency.
    """
    def __init__(self, config, source, target, caption_text):
        self.source = source
        self.target = target
        self.caption_text = caption_text

        if not os.path.exists(self.source):
            raise FileNotFoundError("Gallery file {} does not exist.".format(
                self.source))

        self.font = config.get('album', 'caption_font_filename')
        if not os.path.exists(self.font):
            raise FileNotFoundError("Font file {} does not exist.".format(
                self.font))

        self.create_caption()

    def create_caption(self):
        """
        Create the caption, convert the image to JPEG and save.
        """
        # Initialize some symbolic color names.
        black = (0, 0, 0)
        white = (255, 255, 255)
        transparent = (0, 0, 0, 0)

        # Create an RGBA image object from the source file.
        src_img = Image.open(self.source).convert('RGB')
        gallery_img = self.normalize_image(src_img)
        gallery_width, gallery_height = gallery_img.size

        # Caption height is 5% of total image height.
        caption_bg_color = (0, 0, 0, 100)   # Semi-transparent caption background
        caption_bg_height = int(gallery_height / 20)
        caption_font_size = int(caption_bg_height * 0.5)
        caption_font = ImageFont.truetype(self.font, caption_font_size)

        # New RGBA image object for the caption.
        wm = Image.new('RGBA',(gallery_width, caption_bg_height), caption_bg_color)
        draw = ImageDraw.Draw(wm)
        caption_color = "white"
        caption_width, caption_height = draw.textsize(
            self.caption_text, caption_font)
        draw.text(
            ((gallery_width-caption_width)/2, (caption_bg_height-caption_height)/2),
                self.caption_text, caption_color, caption_font)

        # Paste the caption on the lower end of the source image object.
        en = ImageEnhance.Brightness(wm)
        opacity=0.50    # TODO: Clumsy
        mask = en.enhance(1-opacity)
        gallery_img.paste(wm, (0, gallery_height-caption_bg_height), mask)

        # Flatten alpha channel and save.
        gallery_img.convert("RGB").save(self.target)

    def normalize_image(self, src_img):
        """
        Normalize the source image to a square by copying the source into a
        new image with white background.
        """
        white = (255, 255, 255)
        src_width, src_height = src_img.size

        # Image not square so lets place a square white background behind it.
        if (src_width != src_height):
            bg_width = src_width
            bg_height = src_height

            # Adjust for portrait/landscape orientation.
            if (src_width < src_height):
                fg_width = int((src_width/src_height)*src_width)
                fg_height = src_width
                x_offset = int(bg_width/2 - fg_width/2)
                box = (x_offset, 0, x_offset+fg_width, fg_height)
                gallery_width, gallery_height = src_width, src_width

            if (src_width > src_height):
                fg_width = src_height
                fg_height = int((src_height/src_width)*src_height)
                y_offset = int(bg_height/2 - fg_height/2)
                box = (0, y_offset, fg_width, y_offset+fg_height)
                gallery_width, gallery_height = src_height, src_height

            width, height = (gallery_width, gallery_width)
            bg_img = Image.new('RGB', (width, height), white)
            fg_img = src_img.resize((fg_width, fg_height,))
            bg_img.paste(fg_img, box)
            gallery_img = bg_img.convert('RGBA')
        else:
            gallery_img = src_img.convert('RGBA')

        return gallery_img

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
        index_img = Image.open(self.source).convert('RGBA')
        width, height = index_img.size

        # Caption height is 5% of total image height.
        caption_bg_color = (0, 0, 0, 100)   # Semi-transparent caption background
        caption_bg_height = int(height / 20)
        caption_font_size = int(caption_bg_height * 0.5)
        caption_font = ImageFont.truetype(self.font, caption_font_size)

        # New RGBA image object for the caption.
        wm = Image.new('RGBA',(width, caption_bg_height), caption_bg_color)
        draw = ImageDraw.Draw(wm)
        caption_color = "white"
        caption_width, caption_height = draw.textsize(
            self.caption_text, caption_font)
        draw.text(
            ((width-caption_width)/2, (caption_bg_height-caption_height)/2),
                self.caption_text, caption_color, caption_font)

        # Paste the caption on the lower end of the source image object.
        en = ImageEnhance.Brightness(wm)
        opacity=0.50    # TODO: Clumsy
        mask = en.enhance(1-opacity)
        index_img.paste(wm, (0, height-caption_bg_height), mask)

        # Flatten alpha channel and save.
        index_img.convert("RGB").save(self.target)


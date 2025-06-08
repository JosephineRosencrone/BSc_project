import cv2
import numpy as np
from rendering_app.scripts.import_config import PreprocessedSettings


class Filter_With_Config:
    def __init__(self, settings: list[PreprocessedSettings]):
        self.settings = settings

    def apply_to_image(self, img):
        blue, green, red = cv2.split(img)
        red = self.blur_color_channel(red, 0)
        green = self.blur_color_channel(green, 1)
        blue = self.blur_color_channel(blue, 2)
        return cv2.merge([blue, green, red])

    def blur_color_channel(self, channel, channel_id):
        s = self.settings[channel_id]

        if s.iterations == 0:
            return channel

        output = channel

        if s.iterations == 1:
            output = self.apply_filter(output, s)
        else:
            for _ in range(s.iterations):
                output = self.apply_filter(output, s)

        if s.sharpen:
            output = cv2.addWeighted(channel, 1.5, output, -0.5, 0)
            output = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)

        return output

    def apply_filter(self, img, s:PreprocessedSettings):
        if s.type == "boxBlur":
            return cv2.blur(img, s.kernel)
        elif s.type == "gauss":
            return cv2.GaussianBlur(img, s.kernel, s.sigma, s.sigma2)
        else:
            raise ValueError(f"Unknown filter type: {s.type}")

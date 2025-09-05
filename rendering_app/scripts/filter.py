import cv2
import numpy as np
from rendering_app.scripts.import_config import PreprocessedSettings


class Filter_With_Config:
    def __init__(self, settings: list[PreprocessedSettings]):
        self.settings = settings

    def apply_to_image(self, img, nonFilteredRadius=0):
        # Split video into color channels
        blue, green, red = cv2.split(img)
        
        # Apply filter to each channel
        red_filt = self.filter_color_channel(red, 0)
        green_filt = self.filter_color_channel(green, 1)
        blue_filt = self.filter_color_channel(blue, 2)
        
        if nonFilteredRadius > 0:
            # Create circular mask for exclusion
            center_y, center_x = img.shape[0] // 2, img.shape[1] // 2
            Y,X = np.ogrid[:img.shape[0], :img.shape[1]]
            dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            mask = dist_from_center <= nonFilteredRadius  # Circle with radius = nonFilteredRadius
            mask = mask.astype(np.uint8) # Create mask for each channel

            # Merge filtered and unfiltered circle using mask
            red_filt = np.where(mask, red, red_filt)
            green_filt = np.where(mask, green, green_filt)
            blue_filt = np.where(mask, blue, blue_filt)
        else:
            red, green, blue = red_filt, green_filt, blue_filt
            
        # Merge filtered colour channels back
        img_filt = cv2.merge([blue_filt, green_filt, red_filt])
            
        return img_filt


    def filter_color_channel(self, channel, channel_id):
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

import cv2
import numpy as np
from rendering_app.scripts.import_config import PreprocessedSettings


class Filter_With_Config:
    def __init__(self, settings: list[PreprocessedSettings]):
        self.settings = settings

    def apply_to_image(self, img, nonFilteredRadius=0):
        # Split and apply filter to each colour channel
        blue, green, red = cv2.split(img)
        
        red_filt = self.filter_color_channel(red, 0)
        green_filt = self.filter_color_channel(green, 1)
        blue_filt = self.filter_color_channel(blue, 2)
        
        if nonFilteredRadius > 0:
            # Circular mask
            center_y, center_x = img.shape[0] // 2, img.shape[1] // 2
            Y,X = np.ogrid[:img.shape[0], :img.shape[1]]
            dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            mask = dist_from_center <= nonFilteredRadius  # radius = nonFilteredRadius
            mask = mask.astype(np.uint8) # a mask for each channel

            # Merge original and filtered
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

        if s.sharpen:
            """
            # Unsharp Masking
            alpha = 2.0
            for _ in range(s.iterations):
                blurred = self.apply_filter(channel, s) 
            output = cv2.addWeighted(channel, 1 + alpha, blurred, -alpha, 0)
            """
            # Laplcian sharpening
            lap = cv2.Laplacian(channel, cv2.CV_16S, ksize=3)
            lap = cv2.convertScaleAbs(lap)
            output = cv2.addWeighted(channel, 1, lap, 1, 0)
            """
            # Sharpening convolution kernel
            k = s.kernel[0]
            if k % 2 == 0:
                k += 1
            kernel = -np.ones((k,k), dtype=np.float32)
            kernel[k//2, k//2] = (k * k)
            kernel /= kernel.sum()
            output = cv2.filter2D(channel, -1, kernel)
            """
            return output

        output = channel
        for _ in range(s.iterations):
            output = self.apply_filter(output, s)
    
        return output


    def apply_filter(self, img, s:PreprocessedSettings):
        if s.type == "boxBlur":
            return cv2.blur(img, s.kernel)
        elif s.type == "gauss":
            return cv2.GaussianBlur(img, s.kernel, s.sigma, s.sigma2)
        else:
            raise ValueError(f"Unknown filter type: {s.type}")

import cv2
import numpy as np
# import win32gui

from rendering_app.scripts.import_config import FilterSettings

class Filter_With_Config:
    def __init__(self, filter_settings: FilterSettings):
        self.filter_settings = filter_settings

    def apply_to_image(self, img, nonBlurRadius=0):
        # Split color channels
        if img.shape[-1] == 4:
            blue, green, red, alpha = cv2.split(img)  # BGRA channels in OpenCV
            has_alpha = True
        else:
            blue, green, red = cv2.split(img)  # BGR channels
            has_alpha = False

        # Blur the color channel
        red = self.blur_color_channel(red, 0, nonBlurRadius)
        green = self.blur_color_channel(green, 1, nonBlurRadius)
        blue = self.blur_color_channel(blue, 2, nonBlurRadius)

        # Create a new image with the blurred color channels
        if has_alpha:
            img_blur = cv2.merge([blue, green, red, alpha])  # Preserve BGR order
        else:
            img_blur = cv2.merge([blue, green, red])

        return img_blur

    def blur_color_channel(self, color_channel_data, color_channel_id, radius):
        color_channel_blur = color_channel_data

        
        # If timesFiltersApllied is 0, return the original image
        if self.filter_settings.settings[color_channel_id].timeFiltersApllied == 0:
            return color_channel_data
        

        # Find filter type
        filter_type = self.filter_settings.settings[color_channel_id].filterType
        
        # Get kernel size
        kernel_size = self.filter_settings.settings[color_channel_id].kernelSize
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size) # Convert to tuple
        if kernel_size[0] <= 0 or kernel_size[1] <= 0:  
            raise ValueError("Kernel size must be greater than 0 in both dimensions")
        if filter_type == "gauss":
            kernel_size = tuple((ks if ks % 2 == 1 else ks + 1) for ks in kernel_size)

        # Apply the filter multiple times if specified by the timeFiltersApllied value
        for _ in range(self.filter_settings.settings[color_channel_id].timeFiltersApllied):
            if filter_type == "boxBlur":
                blur = cv2.blur(color_channel_blur, kernel_size, borderType=cv2.BORDER_REFLECT_101)
                color_channel_blur = blur
            
            elif filter_type == "gauss":
                blur = cv2.GaussianBlur(
                    color_channel_blur,
                    kernel_size,
                    self.filter_settings.settings[color_channel_id].sigma,
                    self.filter_settings.settings[color_channel_id].sigma2,
                    borderType=cv2.BORDER_REFLECT_101
                    )
                color_channel_blur = blur
            
            else :
                raise ValueError(f"Unknown filter type: {filter_type}")
        

        # If the filter should sharpen and not blur the image, it is done here
        if self.filter_settings.settings[
            color_channel_id
        ].blurOrSharpenCheckbox:
            color_channel_blur = cv2.addWeighted(
                color_channel_data, 1.5, color_channel_blur, -0.5, 0
            )
            color_channel_blur = cv2.normalize(
                color_channel_blur, None, 0, 255, cv2.NORM_MINMAX
            )

        return color_channel_blur



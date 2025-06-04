from tkinter import Tk, filedialog
import cv2
import numpy as np

from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.import_config import FilterSettings
from rendering_app.scripts.process import process_video
from rendering_app.scripts.display import display_video
from rendering_app.scripts.output import save_output_video


class Video_render:
    def __init__(self, name):
        self.name = name

        root = Tk()
        root.withdraw()
        
        # INPUT FILES
        self.video_path = filedialog.askopenfilename(title="Select video file")
        if not self.video_path:  # User canceled file selection
            print("No video file selected. Exiting...")
            return

        file_path = filedialog.askopenfilename(title="Select config file")
        if not file_path:  # User canceled config selection
            print("No config file selected. Exiting...")
            return
        
        root.destroy()
        
        # Load filter settings from config file
        filter_settings = FilterSettings.import_config(file_path)
        self.filter = Filter_With_Config(filter_settings=filter_settings)

    def run(self):
        # LOAD AND PROCESS VIDEO
        output_path, resolution, fps = process_video(
            self.video_path,
            "temp_output.mp4",
            self.filter.apply_to_image
        )
        if output_path is None:
            print("Processing failed.")
            return
        
        
        # DISPLAY VIDEO
        display_output = input("Display rendered video? (y/n): ").strip().lower()
        if display_output == "y":
            display_video(output_path, resolution, fps)
        else:
            print("Video not displayed.")


        # SAVE VIDEO
        save_output = input("Save filtered video? (y/n): ").strip().lower()
        if save_output == "y":
            save_output_video(output_path, self.video_path)
        else:
            print("Video not saved.")
            

from tkinter import Tk, filedialog
import cv2
import numpy as np

from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.import_config import FilterSettings
from rendering_app.scripts.vid_process import process_video
from rendering_app.scripts.display import display_video
from rendering_app.scripts.output import save_output_video
from rendering_app.scripts.realtime import realtime


class Video_render:
    def __init__(self, name):
        self.name = name
        self.valid = False

        root = Tk()
        root.withdraw()
        
        # INPUT FILES
        self.video_path = filedialog.askopenfilename(title="Select video file")
        if not self.video_path:  # User cancels file selection
            print("No video file selected. Exiting...")
            return

        file_path = filedialog.askopenfilename(title="Select config file")
        if not file_path:  # User cancels config selection
            print("No config file selected. Exiting...")
            return
        root.destroy()
        
        # Load filter settings from config file
        filter_settings = FilterSettings.import_config(file_path)
        self.filter = Filter_With_Config(settings=filter_settings.preprocess_settings)
        
        # NON FILTERED CENTER
        try:
            self.nonFilteredRadius = int(input("Enter pixel radius for non-filtered center region (0 to disable): "))
        except ValueError:
            self.nonFilteredRadius = 0
        
        self.valid = True
        
    def filter_area(self, img):
        return self.filter.apply_to_image(img, nonFilteredRadius=self.nonFilteredRadius)


    def run(self):
        if not self.valid:
            return
        
        # PROCESS VIDEO
        # Realtime playback
        play_realtime = input("Play video in real-time? (y/n): ").strip().lower()
        if play_realtime == "y":
            output_path, resolution, fps = realtime(
                self.video_path,
                "temp_output.mp4",
                self.filter_area)
        else:
            # Full processing
            output_path, resolution, fps = process_video(
                self.video_path,
                "temp_output.mp4",
                self.filter_area
            )
            if output_path is None:
                print("Processing failed.")
                return
            
            # Display video
            display_output = input("Display rendered video? (y/n): ").strip().lower()
            if display_output == "y":
                display_video(self.video_path, output_path, resolution, fps)
            else:
                print("Video not displayed.")


        # SAVE VIDEO
        save_output = input("Save filtered video? (y/n): ").strip().lower()
        if save_output == "y":
            save_output_video(output_path, self.video_path)
        else:
            print("Video not saved.")
            

import time
from tkinter import Tk, filedialog
import cv2
import numpy as np
# from matplotlib import pyplot as plt


from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.import_config import FilterSettings


class Video_render:
    def __init__(self, name):
        # Define application settings
        self.name = name

        # Import video file
        Tk().withdraw()
        self.video_path = filedialog.askopenfilename(title="Select video file")
        if not self.video_path:  # User canceled file selection
            print("No video file selected. Exiting...")
            return

        # Import config file and setup filter
        file_path = filedialog.askopenfilename(title="Select config file")
        if not file_path:  # User canceled config selection
            print("No config file selected. Exiting...")
            return
        
        filter_settings = FilterSettings.import_config(file_path)
        self.filter = Filter_With_Config(filter_settings=filter_settings)

    def run(self):
        # Open video
        cap = cv2.VideoCapture(self.video_path)
        
        # Error handling
        if not cap.isOpened(): # Video file not found
            print("Error: Could not open video.")
            return

         # Video properties
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Frame width: {frame_width}, Frame height: {frame_height}, FPS: {fps}")


        processed_frames = []
        print("Processing video...")
        
        # Process video frame by frame
        while cap.isOpened():
            # Read through each video frame, stop when video ends
            ret, frame = cap.read()
            if not ret:
                break

            # Apply filter to frame
            frame_filtered = self.filter.apply_to_image(frame)
            processed_frames.append(frame_filtered)

        cap.release()
        print("Processing complete! Now displaying the filtered video...")
        
        windowName = "Filtered video"
        cv2.namedWindow(windowName)
        cv2.resizeWindow(windowName, 640, 480)
        
        # Display processed video
        for frame in processed_frames:
            cv2.imshow(windowName, frame)
            wait_time = int(1000 / fps) # Playback speed
            
            # Quit program if 'q' is pressed
            if cv2.waitKey(wait_time) & 0xFF == ord("q"):
                print("Playback stopped.")
                break
        
        cv2.destroyAllWindows()
    
        # Save video
        save_output = input("Save filtered video? (y/n): ").strip().lower()
        if save_output == "y":
            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")]
            )
            if output_path:
                print("Saving video...")
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
                
                for frame in processed_frames:
                    out.write(frame)
            out.release()
            print(f"Video saved at {output_path}")
        else:
            save_output = "n"
            print("Video not saved.")
            

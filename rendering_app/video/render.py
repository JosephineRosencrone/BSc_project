import time
from tkinter import Tk, filedialog
import cv2
import numpy as np
from moviepy import VideoFileClip,ImageSequenceClip  # Import MoviePy


from rendering_app.scripts.filter import Filter_With_Config
from rendering_app.scripts.import_config import FilterSettings


class Video_render:
    def __init__(self, name):
        self.name = name

        root = Tk()
        root.withdraw()
        
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
        # LOAD VIDEO
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened(): # Video file not found
            print("Error: Could not open video.")
            return

        # Video properties
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video width: {frame_width}, Video height: {frame_height}, FPS: {fps}")

        # PROCESS VIDEO
        output_video = None
        print("Processing video...")
        
        try: 
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                try:
                    frame_filtered = self.filter.apply_to_image(frame)
                except Exception as e:
                    print(f"Error applying filter: {e}")
                    continue

                # Initialize video writer only once (first frame)
                if output_video is None:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
                    output_video = cv2.VideoWriter("temp_output.mp4", fourcc, fps, (frame_width, frame_height))

                output_video.write(frame_filtered)  # Write directly to file

        finally:
            cap.release()
        if output_video:
            output_video.release()

        print("Processing complete!")
        
        # DISPLAY VIDEO
        cap = cv2.VideoCapture("temp_output.mp4")
        windowName = "Filtered video"
        cv2.namedWindow(windowName)
        
        # Scale video dimensions for display
        scale_w = 1280 / frame_width
        scale_h = 720 / frame_height
        scale = min(scale_w, scale_h)
        display_width = int(frame_width * scale)
        display_height = int(frame_height * scale)

        print("Now displaying the processed video. Press 'q' to quit.")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # Stop when the video ends

            display_frame = cv2.resize(frame, (display_width, display_height))
            cv2.imshow(windowName, display_frame)

            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):  # Wait for 'q' key to quit
                print("Playback stopped.")
                break

        cap.release()  # Release the video file
        cv2.destroyAllWindows()  # Close all OpenCV windows
    
        # SAVE VIDEO
        save_output = input("Save filtered video? (y/n): ").strip().lower()
        if save_output == "y":
            output_path = filedialog.asksaveasfilename(
                defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")]
            )
            if output_path:
                print("Saving video...")

                # Load the processed video and original audio
                processed_clip = VideoFileClip("temp_output.mp4")
                original_clip = VideoFileClip(self.video_path)

                # Set the audio of the processed video to the original audio
                final_clip = processed_clip.with_audio(original_clip.audio)
                final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                print(f"Video saved at {output_path}")
        else:
            print("Video not saved.")
            

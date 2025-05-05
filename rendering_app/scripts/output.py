from tkinter import filedialog
from moviepy import VideoFileClip

def save_output_video(temp_video_path, original_video_path):
    output_path = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4")],
        title="Save filtered video as..."
    )
    
    if not output_path:
        print("No path selected. Video not saved.")
        return

    print("Saving video...")

    try:
        # Load the processed and original videos
        processed_clip = VideoFileClip(temp_video_path)
        original_clip = VideoFileClip(original_video_path)

        # Combine audio from the original video
        final_clip = processed_clip.with_audio(original_clip.audio)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Video saved at {output_path}")
    except Exception as e:
        print(f"Error saving video: {e}")

import cv2
import time
import numpy as np

def display_video(original_path, filtered_path, original_size, fps):
    cap_og = cv2.VideoCapture(original_path, cv2.CAP_FFMPEG)
    cap_filt = cv2.VideoCapture(filtered_path, cv2.CAP_FFMPEG)
    if not cap_og.isOpened() or not cap_filt.isOpened():
        print("Error: Could not open video for display.")
        return

    # Calculate display size
    display_width = 950
    scale = display_width / original_size[0]
    display_height = int(original_size[1] * scale)

    frame_duration = 1 / fps

    print("Displaying the filtered video. Press 'q' to quit.")

    while True:
        start_time = time.time()

        ret1, frame1 = cap_og.read()
        ret2, frame2 = cap_filt.read()
        if not ret1 or not ret2:
            break

        original_frame = cv2.resize(frame1, (display_width, display_height), interpolation=cv2.INTER_AREA)
        filtered_frame = cv2.resize(frame2, (display_width, display_height), interpolation=cv2.INTER_AREA)
        
        # Concatenate them side by side
        combined_frame = np.hstack((original_frame, filtered_frame))
        
        cv2.imshow("Original | Filtered", combined_frame)

        elapsed = time.time() - start_time
        wait_time_ms = max(1, int(round((frame_duration - elapsed) * 1000)))

        if cv2.waitKey(wait_time_ms) & 0xFF == ord("q"):
            print("Playback stopped.")
            break

    cap_og.release()
    cap_filt.release()
    cv2.destroyAllWindows()

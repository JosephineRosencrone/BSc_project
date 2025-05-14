import cv2
import time
import numpy as np

def display_video(video_path, original_size, fps, window_name="Rendered video"):
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print("Error: Could not open video for display.")
        return

    cv2.namedWindow(window_name)

    # Calculate display size
    target_size = np.array([1280, 720])
    scale = np.min(target_size / np.array(original_size))
    display_size = (np.array(original_size) * scale).astype(int)
    display_width, display_height = display_size

    frame_duration = 1 / fps

    print("Now displaying the processed video. Press 'q' to quit.")

    while cap.isOpened():
        frame_start = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        display_frame = cv2.resize(frame, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
        cv2.imshow(window_name, display_frame)

        elapsed = time.time() - frame_start
        wait_time_ms = max(1, int(round((frame_duration - elapsed) * 1000)))

        if cv2.waitKey(wait_time_ms) & 0xFF == ord("q"):
            print("Playback stopped.")
            break

    cap.release()
    cv2.destroyAllWindows()

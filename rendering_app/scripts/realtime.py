import cv2
import numpy as np
import time

def realtime(video_path, filter_func):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps
    original_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    print("Starting real-time playback. Press 'q' to quit.")
    while cap.isOpened():
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        try:
            filtered_frame = filter_func(frame)
        except Exception as e:
            print(f"Error applying filter: {e}")
            continue

        # Calculate display size
        display_width = 750
        scale = display_width / original_size[0]
        display_height = int(original_size[1] * scale)

        original_resized = cv2.resize(frame, (display_width, display_height), interpolation=cv2.INTER_AREA)
        filtered_resized = cv2.resize(filtered_frame, (display_width, display_height), interpolation=cv2.INTER_AREA)

        # Concatenate them side by side
        combined_frame = np.hstack((original_resized, filtered_resized))

        cv2.imshow("Original | Filtered", combined_frame)

        elapsed = time.time() - start_time
        wait_time = max(1, int((frame_duration - elapsed) * 1000))

        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

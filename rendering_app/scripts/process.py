import cv2
import time

def process_video(input_path, output_path, filter_func):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None, None, None

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    total_seconds = int(frame_count / fps)
    minutes, seconds = divmod(total_seconds, 60)
    print(f"Video resolution: {frame_width}x{frame_height}, "
          f"Video length: {minutes:02d}:{seconds:02d} (mm:ss), FPS: {fps}")

    print("Processing video...")
    start_time = time.time()
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            try:
                filtered_frame = filter_func(frame)
            except Exception as e:
                print(f"Error applying filter: {e}")
                continue

            writer.write(filtered_frame)

    finally:
        cap.release()
        if writer:
            writer.release()

    print(f"Processing complete! Video rendered in {time.time() - start_time:.2f} seconds")

    return output_path, (frame_width, frame_height), fps

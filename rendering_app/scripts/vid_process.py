import cv2
import time
import os
import multiprocessing as mp

from rendering_app.scripts.cap_multiprocess import read_frames, process_frames, write_frames

# Confugration for multiprocessing
num_workers = 4  # os.cpu_count() - 2
max_queue = 3

def process_video(input_path, output_path, filter_func):
    # Get video properties using a temporary VideoCapture instance
    temp_cap = cv2.VideoCapture(input_path)
    if not temp_cap.isOpened():
        print("Error: Could not open video.")
        return None, None, None

    frame_width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = temp_cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(temp_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    temp_cap.release()

    minutes, seconds = divmod( int(total_frames/fps), 60)
    print(f"Video properties: {frame_width}x{frame_height}, {minutes:02d}:{seconds:02d}," 
          f"{fps:.2f} FPS, {total_frames} frames.")
    
    # Create multiprocessing queues for frame input and processed output
    frame_queue = mp.Queue(maxsize=max_queue)
    result_queue = mp.Queue()

    # Create processes for reading, processing, and writing
    reader_proc = mp.Process(target=read_frames, args=(input_path, frame_queue, num_workers))
    worker_procs = [mp.Process(target=process_frames, args=(frame_queue, result_queue, filter_func)) for _ in range(num_workers)]
    writer_proc = mp.Process(target=write_frames, args=(output_path, result_queue, total_frames, frame_width, frame_height, fps))

    # Start timing and all processes
    start_time = time.time()
    reader_proc.start()
    for p in worker_procs:
        p.start()
    writer_proc.start()

    # Wait for all processes to complete
    reader_proc.join()
    for p in worker_procs:
        p.join()
    writer_proc.join()

    print(f"Processing complete in {time.time() - start_time:.2f} seconds")

    return output_path, (frame_width, frame_height), fps
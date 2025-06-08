import cv2
import os
import ctypes

def get_cpu_id():
    return ctypes.windll.kernel32.GetCurrentProcessorNumber()


# Read video frames
def read_frames(input_path, frame_queue, num_workers):
    cap = cv2.VideoCapture(input_path)
    index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_queue.put((index, frame))
        index += 1
    cap.release()
    # Send stop signals
    for _ in range(num_workers):
        frame_queue.put(None)
        
# Process frames
def process_frames(frame_queue, result_queue, filter_func):
    print(f"Worker PID: {os.getpid()} running on CPU: {get_cpu_id()}")
    
    while True:
        item = frame_queue.get()
        if item is None:
            result_queue.put(None)
            break
        index, frame = item
        try:
            processed = filter_func(frame)
            result_queue.put((index, processed))
        except Exception as e:
            print(f"Error processing frame {index}: {e}")

# Write processed frames to output
def write_frames(output_path, result_queue, total_frames, frame_width, frame_height, fps):
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    received = {}
    expected_index = 0
    end_signals_received = 0

    while expected_index < total_frames:
        item = result_queue.get()
        if item is None:
            end_signals_received += 1
            continue
        index, frame = item
        received[index] = frame

        while expected_index in received:
            writer.write(received.pop(expected_index))
            expected_index += 1

    writer.release()

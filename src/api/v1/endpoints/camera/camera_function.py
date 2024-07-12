import cv2
import os
import time
import asyncio
from src.api.v1.endpoints.camera.object_tracking import *

def capture_webcam(ip_camera_url, flag = False):
    if flag:
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    else:
        cap = initialize_video_capture(ip_camera_url)
        model = initialize_model()
        class_names = load_class_names()
        
        tracker = DeepSort(max_age=20, n_init=3)
        
        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(class_names), 3))
        
        class_counters = defaultdict(int)
        track_class_mapping = {}
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            tracks = process_frame(frame, model, tracker, class_names, colors)
            frame = draw_tracks(frame, tracks, class_names, colors, class_counters, track_class_mapping)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            
async def capture_and_save(ip_camera_url, folder_path):
    cap = cv2.VideoCapture(0)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Lưu frame ảnh vào thư mục đã chỉ định
        frame_name = f"frame_{frame_count}.jpg"
        frame_path = os.path.join(folder_path, frame_name)
        cv2.imwrite(frame_path, frame)

        frame_count += 1

        if frame_count == 10 : 
            frame_count =0

        # Đợi 1 giây trước khi ghi frame tiếp theo
        await asyncio.sleep(0.25)
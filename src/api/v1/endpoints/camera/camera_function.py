import cv2
import os
import time
import asyncio

def capture_webcam(ip_camera_url):

    cap = cv2.VideoCapture(ip_camera_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
async def capture_and_save(ip_camera_url, folder_path):
    cap = cv2.VideoCapture(ip_camera_url)
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
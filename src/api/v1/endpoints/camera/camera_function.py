import cv2
import os
import time
import asyncio
from src.api.v1.endpoints.camera.object_tracking import *

def capture_webcam(ip_camera_url,model,tracker,folder_path ,flag = False):
    if flag:
        cap = cv2.VideoCapture(ip_camera_url)
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
        # model = initialize_model()
        class_names = load_class_names()
        
        # tracker = DeepSort(max_age=20, n_init=3)
        
        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(class_names), 3))
        
        class_counters = defaultdict(int)
        track_class_mapping = {}
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            tracks = process_frame(frame, model, tracker, class_names, colors)
            frame_name = f"frame_{frame_count}.jpg"
            frame_path = os.path.join(folder_path, frame_name)
            cv2.imwrite(frame_path, frame)
            # print(f"Saved frame {frame_count}")
            frame_count+=1
            if frame_count == 10 : 
                frame_count =0
            frame = draw_tracks(frame, tracks, class_names, colors, class_counters, track_class_mapping)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
# async def capture_webcam(frame_queue):
#     while True:
#         frame = await frame_queue.get()
#         if frame is None:
#             break

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
async def detect(ip_camera_url, model,tracker, folder_path, frame_queue):
    cap = initialize_video_capture(ip_camera_url)
    class_names = load_class_names()
    colors = np.random.randint(0, 255, size=(len(class_names), 3))
    frame_count = 0
    class_counters = defaultdict(int)
    track_class_mapping = {}
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        tracks = process_frame(frame, model, tracker, class_names, colors)
        
        frame_name = f"frame_{frame_count}.jpg"
        frame_path = os.path.join(folder_path, frame_name)
        cv2.imwrite(frame_path, frame)
        # print(f"Saved frame {frame_count}")
        frame_count += 1
        frame = draw_tracks(frame, tracks, class_names, colors, class_counters, track_class_mapping)
        if frame_count == 10:
            frame_count = 0
        try:
            await frame_queue.put(frame)
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass

    cap.release()
    await frame_queue.put(None)  # Signal that detection is done
async def capture_and_save(ip_camera_url,folder_path):
    try : 
        cap = initialize_video_capture(ip_camera_url)
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
            await asyncio.sleep(0.2)
    except Exception as e:
        print(f"Error: {str(e)}")
        await asyncio.sleep(5)
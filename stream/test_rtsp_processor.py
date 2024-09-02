import sys
sys.path.append('/workspace')

import sys
import os
import time
import lib.stream_processor as sp
import cv2
import numpy as np
import threading

# 설정된 출력 디렉토리
OUTPUT_DIR = "/workspace/output"

def create_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_frame(image_data, channel_id, timestamp):
    # 채널 ID와 타임스탬프를 사용하여 파일명 생성
    timestamp_str = time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp))
    file_name = f"channel_{channel_id}_{timestamp_str}_{int(time.time() * 1000) % 1000}.jpg"  # 밀리초 단위로 파일명 생성
    file_path = os.path.join(OUTPUT_DIR, file_name)

    # 이미지 데이터를 NumPy 배열로 변환
    image_array = np.frombuffer(image_data, dtype=np.uint8)
    image_array = image_array.reshape((IMG_HEIGHT, IMG_WIDTH, 3))  # 이미지 크기와 채널에 맞게 조정
    cv2.imwrite(file_path, image_array)

def process_frames(rtsp_urls, width, height, fps):
    # RTSP 스트림 설정
    sp.set_stream_config(rtsp_urls, width, height, fps)
    sp.start_stream_processing()
    create_output_directory()

    def frame_saver():
        while True:
            frame = sp.get_next_frame()
            if frame is None:
                time.sleep(0.01)  # 잠시 대기
                continue

            # FrameData 구조체를 파싱하여 정보 추출
            image_data = frame[0]  # 이미지 데이터
            channel_id = frame[1]  # 채널 ID
            timestamp = frame[2]   # 타임스탬프

            # 저장된 이미지와 메타데이터를 기반으로 이미지 저장
            save_frame(image_data, channel_id, timestamp)
            print(f"Saved frame from channel {channel_id} at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}")

    # 스레드 생성 및 시작
    threads = []
    for _ in range(fps):  # fps 값에 따라 여러 스레드를 생성
        t = threading.Thread(target=frame_saver)
        t.start()
        threads.append(t)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Processing interrupted by user.")
    finally:
        sp.stop_stream_processing()

if __name__ == "__main__":
    # 사용자 설정에 따라 width, height, fps 값을 지정합니다.
    RTSP_URLS = [
        "rtsp://127.0.0.1:8554/stream",
        "rtsp://127.0.0.1:8562/stream"
    ]
    IMG_WIDTH = 1280
    IMG_HEIGHT = 720
    FPS = 2  # C++ 코드에서 설정한 1초당 저장할 프레임 수
    process_frames(RTSP_URLS, IMG_WIDTH, IMG_HEIGHT, FPS)

# Detect scene boundaries and extract mid-scene frames with PySceneDetect
import cv2
import pandas as pd
from pathlib import Path
from scenedetect import open_video, SceneManager, ContentDetector

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
OUTPUT = Path(__file__).parent / "outputs" / "scenes"
OUTPUT.mkdir(parents=True, exist_ok=True)

video = open_video(str(VIDEO))
scene_manager = SceneManager()
scene_manager.add_detector(ContentDetector(threshold=27.0))
scene_manager.detect_scenes(video)
scene_list = scene_manager.get_scene_list()

rows = []
for i, (start, end) in enumerate(scene_list, 1):
    rows.append({"scene": i, "start_time": start.get_timecode(), "end_time": end.get_timecode(),
                 "duration_sec": round((end - start).get_seconds(), 2)})
df = pd.DataFrame(rows)
df.to_csv(OUTPUT / "scene_list.csv", index=False)

cap = cv2.VideoCapture(str(VIDEO))
fps = cap.get(cv2.CAP_PROP_FPS)
for i, (start, end) in enumerate(scene_list, 1):
    mid_frame = int((start.get_seconds() + end.get_seconds()) / 2 * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(str(OUTPUT / f"scene_{i:03d}.jpg"), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
cap.release()

print(f"Found {len(scene_list)} scenes, frames saved to {OUTPUT}")

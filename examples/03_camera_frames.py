"""03 - Get camera frames from the robot.

read_camera_data() returns one JPEG image as bytes (or None if no new frame is ready yet).
That is all you need: save it, decode it with Pillow or OpenCV, run your own detector on it.

    python examples/03_camera_frames.py              # grab frames for 5 s, save the last one to frame.jpg
    python examples/03_camera_frames.py --view       # live window (needs: pip install opencv-python)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import argparse
import time
from robot import connect

ap = argparse.ArgumentParser()
ap.add_argument("--seconds", type=float, default=5)
ap.add_argument("--view", action="store_true", help="show a live window instead of just saving")
args = ap.parse_args()

got = connect()
got.open_camera()                       # call once before reading frames

last, count, start = None, 0, time.time()
while time.time() - start < args.seconds:
    jpeg = got.read_camera_data()       # bytes, or None
    if not jpeg:
        continue
    last, count = jpeg, count + 1
    if args.view:
        import cv2, numpy as np
        image = cv2.imdecode(np.frombuffer(jpeg, np.uint8), cv2.IMREAD_COLOR)   # a normal OpenCV image
        cv2.imshow("robot camera (press q)", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

print(f"{count} frames in {time.time() - start:.1f}s")
if last:
    open("frame.jpg", "wb").write(last)
    print("saved the last frame to frame.jpg")

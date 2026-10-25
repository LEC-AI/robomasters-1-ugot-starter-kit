"""04 - Find AprilTags and QR codes with the robot's own vision.

You must load a vision model first, then read its results. Release it when done.

    python examples/04_tags_and_qr.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import time
from robot import connect

got = connect()
got.load_models(["apriltag_qrcode"])
try:
    for _ in range(40):                                      # about 10 seconds
        # each tag: [id, center_x, center_y, height, width, area, distance5, distance7, distance10, x, y, z, bearing_h, bearing_v]
        for t in got.get_apriltag_total_info() or []:
            tag_id, distance_10cm_tag, bearing = int(t[0]), t[8], t[12]
            # use t[6] or t[7] instead of t[8] if your printed tags are 5 cm or 7 cm wide
            print(f"tag {tag_id}: {distance_10cm_tag:.0f} away, bearing {bearing:.0f} degrees (negative left, positive right)")
        # each QR code: [text, center_x, center_y, height, width, area]
        for q in got.get_qrcode_total_info() or []:
            print(f"QR code says: {q[0]}")
        time.sleep(0.25)
finally:
    got.release_models()

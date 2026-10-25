"""05 - Find coloured objects (for picking the right block).

    python examples/05_colours.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import time
from robot import connect

got = connect()
got.load_models(["color_recognition"])
try:
    for _ in range(40):
        result = got.get_color_total_info()
        # each result: [color, shape, center_x, center_y, height, width, area]
        # (the SDK may give one result or a list of them, so handle both)
        rows = result if result and isinstance(result[0], (list, tuple)) else ([result] if result else [])
        for color, shape, cx, cy, h, w, area in rows:
            print(f"{color} {shape} at ({cx:.0f}, {cy:.0f}), size {area:.0f}")
        time.sleep(0.25)
finally:
    got.release_models()

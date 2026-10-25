"""08 - Arm and gripper (engineer build only).

The arm has three joints and a clamp. mechanical_move_axis() is the easy way to aim it:
  r      reach in front of the robot, -5.5 to 24.9 cm
  h      height, -18 to 18.2 cm
  theta  left/right angle in radians, -1.57 to 1.57
  duration  milliseconds, 20 to 5000 (use 2000 or more at first)
Start with small moves and keep hands clear.

    python examples/08_arm_gripper.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import time
from robot import connect, chassis

got = connect()
if chassis(got) != "engineer":
    raise SystemExit(f"This robot is built as '{chassis(got)}'. The arm and gripper need the engineer build.")

got.mechanical_arms_restory()                       # arm to its rest position
time.sleep(2)

got.mechanical_clamp_release()                      # open
time.sleep(1)
got.mechanical_move_axis(12, 0, 0, 2000)            # reach 12 cm out, level, straight ahead
time.sleep(2.5)
got.mechanical_clamp_close()                        # close on whatever is there
time.sleep(1)
print("clamp status:", got.mechanical_get_clamp_status(), "(0 open, 1 closed)")

got.mechanical_move_axis(5, 8, 0, 2000)             # lift it up and back a little
time.sleep(2.5)
got.mechanical_clamp_release()                      # let go
time.sleep(1)
got.mechanical_arms_restory()

"""07 - Drive safely: ramp the speed, and ALWAYS stop at the end.

model_common_move(speed, turn) works on every build. speed is cm/s (negative = backwards),
turn is degrees/s (positive = left, negative = right).
Clear half a metre around the robot first. Keep speeds low while testing.

    python examples/07_drive.py --speed 15
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import argparse
import time
from robot import connect, chassis, stop

ap = argparse.ArgumentParser()
ap.add_argument("--speed", type=int, default=15, help="cm/s, 5 to 30")
args = ap.parse_args()
speed = max(5, min(30, args.speed))

got = connect()
build = chassis(got)
if build == "box":
    raise SystemExit("Build is 'box': movement commands are ignored. Check the robot is assembled and its build is selected.")

# Balancing builds must be started before they will move.
if build == "wheel_legged":
    got.wheelleg_start_balancing(); time.sleep(1.5)
elif build == "balance":
    got.balance_start_balancing(); time.sleep(1.5)

def move_for(seconds, speed, turn=0, ramp=0.4):
    """Ease up to the speed (a sudden jump can tip a balancing robot), hold, then ease down."""
    steps = 8
    for i in range(1, steps + 1):                                  # ease in
        got.model_common_move(int(speed * i / steps), int(turn * i / steps)); time.sleep(ramp / steps)
    end = time.time() + seconds
    while time.time() < end:                                       # hold (commands must keep arriving)
        got.model_common_move(speed, turn); time.sleep(0.1)
    for i in range(steps - 1, -1, -1):                             # ease out
        got.model_common_move(int(speed * i / steps), int(turn * i / steps)); time.sleep(ramp / steps)

try:
    move_for(1.5, speed)               # forward
    time.sleep(0.5)
    move_for(1.0, 0, turn=40)          # turn left
finally:
    stop(got)                          # runs even if your code crashes

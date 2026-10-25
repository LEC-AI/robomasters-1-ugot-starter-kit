"""01 - Find a robot and read its basics.   Run:  python examples/01_connect.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from robot import find_robots, connect, chassis

print("Robots on this Wi-Fi:", find_robots())

got = connect()                                   # first robot found
pct, plugged_in, status = got.get_power_status()  # battery %, charger plugged in, status code
volume, muted = got.get_volume()
build = chassis(got)

print(f"{got.robot_name}: build={build}  battery={pct}%  volume={volume}{'  (MUTED)' if muted else ''}")
if build == "box":
    print("Build is 'box': the SDK ignores movement commands in this mode. Check the robot is assembled and its build is selected.")
if muted:
    print("The robot is muted, so speech and sounds will be silent. Unmute it in the UGOT app or on the robot.")

"""robot.py - the one helper every example uses. It is short, so read it.

    from robot import connect
    got = connect()                    # first robot found on the Wi-Fi
    got = connect(name="UGOT_XXXX")    # a specific one
    got = connect(ip="192.168.1.50")   # skip discovery if you know the address

`got` is the normal SDK object (ugot.UGOT). Everything in the SDK works on it.
"""
import os
import sys
import time

import grpc
from ugot import ugot


def find_robots(tries=4, wait=1.5):
    """Return {"UGOT_XXXX": "192.168.1.50", ...}. Discovery uses multicast and can miss a robot
    on one pass, so it looks a few times."""
    scanner = ugot.UGOT()
    found = {}
    for _ in range(tries):
        found.update(dict(scanner.scan_device()))
        if found:
            break
        time.sleep(wait)
    return found


def _finish_language_setup():
    """Some robots do not implement getLanguage, which the SDK calls as the very last step of
    initialize(). The SDK then raises UNIMPLEMENTED even though the connection is fine and
    everything else is already set up. We set the default (English) the way the SDK would have."""
    from ugot.src.configure_string_single import ConfigureStringSingle
    locale_dir = os.path.join(os.path.dirname(os.path.realpath(ugot.__file__)), "src", "locale")
    ugot.LANGUAGE_CONFIGURE = ConfigureStringSingle(locale_dir, "ugot", language=["en"])


def connect(name=None, ip=None, quiet=False):
    """Find a robot (or use the ip you give) and return a ready-to-use SDK object."""
    if ip is None:
        robots = find_robots()
        if not robots:
            sys.exit("No robots found.\n"
                     "  - Is your laptop on the same Wi-Fi as the robots?\n"
                     "  - Is a VPN switched on? Switch it off.\n"
                     "  - Is the robot on? Try again, or pass ip='...'.")
        if name is None:
            name = sorted(robots)[0]
            if len(robots) > 1 and not quiet:
                print(f"[robot] {len(robots)} robots found {sorted(robots)}; using {name}. "
                      f"Pick one with connect(name=...)", file=sys.stderr)
        if name not in robots:
            sys.exit(f"{name} not found. Robots seen: {sorted(robots)}")
        ip = robots[name]
    got = ugot.UGOT()
    try:
        got.initialize(ip)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNIMPLEMENTED:
            _finish_language_setup()
        else:
            raise
    got.robot_name, got.robot_ip = name or ip, ip
    return got


def chassis(got):
    """What the robot is built as: 'engineer', 'mecanum', 'wheel_legged', 'dog', ...
    'box' means just the brain unit; the SDK ignores movement commands in that mode."""
    return got.DEVICE.getDeviceModel()


def stop(got):
    """Stop all motion. Safe to call any time."""
    try:
        got.stop_chassis()
    except Exception:
        pass

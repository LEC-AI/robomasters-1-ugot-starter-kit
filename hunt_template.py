"""hunt_template.py - your team's starting point for the six treasure hunt checkpoints.

Each checkpoint is one function. Fill them in one at a time, then run:

    python hunt_template.py            # runs the checkpoints in order, stops at the first TODO
    python hunt_template.py 4          # run only checkpoint 4

The examples/ folder shows every SDK call you need. find_tag() below already works.
"""
import sys
import time
from robot import connect, chassis, stop


def find_tag(got, tag_id, timeout=10):
    """Look for an AprilTag for up to `timeout` seconds. Returns (distance, bearing) or None.
    Needs got.load_models(["apriltag_qrcode"]) to have been called first."""
    end = time.time() + timeout
    while time.time() < end:
        for t in got.get_apriltag_total_info() or []:
            if int(t[0]) == tag_id:
                return t[8], t[12]            # distance (10 cm tag), bearing in degrees
        time.sleep(0.2)
    return None


def checkpoint_1_build(got):
    """Robot is assembled, connected, and says the team name aloud."""
    # got.play_audio_tts("We are team ...", 0, wait=True)
    raise NotImplementedError("TODO: checkpoint 1 - see examples/02_speak_light_screen.py")


def checkpoint_2_move(got):
    """Drive a set route into a taped box, then stop 15 to 25 cm short of a wall using the distance sensor."""
    # got.read_distance_data(port) returns centimetres, or -1 if there is no reading
    raise NotImplementedError("TODO: checkpoint 2 - see examples/07_drive.py")


def checkpoint_3_talk(got):
    """Turn toward a voice or clap, and speak the battery level and tilt."""
    # got.enable_audio_direction(); got.get_audio_direction(); got.get_power_status(); got.read_gyro_data()
    raise NotImplementedError("TODO: checkpoint 3 - see examples/06_audio.py")


def checkpoint_4_find_clue(got):
    """Find your team's tag, drive up to it, read the QR code beneath it. Return the colour it names."""
    # got.load_models(["apriltag_qrcode"]); find_tag(...); got.get_qrcode_total_info()
    raise NotImplementedError("TODO: checkpoint 4 - see examples/04_tags_and_qr.py")


def checkpoint_5_grab(got, colour):
    """Pick the block of that colour, grip it, and drop it in your team's chest."""
    # got.load_models(["color_recognition"]); arm and clamp calls
    raise NotImplementedError("TODO: checkpoint 5 - see examples/05_colours.py and examples/08_arm_gripper.py")


def checkpoint_6_full_run(got):
    """Checkpoints 2 to 5 as one run from a single command, in under three minutes."""
    checkpoint_2_move(got)
    colour = checkpoint_4_find_clue(got)
    checkpoint_5_grab(got, colour)


def main():
    got = connect()
    print(f"connected to {got.robot_name} (build: {chassis(got)})")
    steps = {1: checkpoint_1_build, 2: checkpoint_2_move, 3: checkpoint_3_talk,
             4: checkpoint_4_find_clue, 5: lambda g: checkpoint_5_grab(g, "red"), 6: checkpoint_6_full_run}
    wanted = [int(sys.argv[1])] if len(sys.argv) > 1 else sorted(steps)
    try:
        for n in wanted:
            print(f"--- checkpoint {n} ---")
            steps[n](got)
    except NotImplementedError as todo:
        print(todo)
    finally:
        stop(got)


if __name__ == "__main__":
    main()

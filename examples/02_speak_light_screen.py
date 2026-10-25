"""02 - Make the robot speak, play a sound, light up and show a face.
None of this moves the robot.   Run:  python examples/02_speak_light_screen.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import time
from robot import connect

got = connect()

got.play_audio_tts("Hello from my code", 0, wait=True)   # text, voice (0 female / 1 male), wait until done
got.play_sound("dog", wait=True)                         # 52 built-in effects, e.g. dog, lion, laser, robot
got.show_light_rgb_effect(0, 255, 0, 0)                  # red, green, blue (0-255), effect: 0 steady 1 off 2 breathe 3 flash
got.screen_print_text("Hello team", 6)                   # text, colour 0-8 (6 = green)
got.screen_display_emotion("Smile")                      # WakeUp Smile Doubt Search Love Anger Proud Ticklish Sleep ...
time.sleep(3)
got.screen_clear()
got.show_light_rgb_effect(0, 0, 0, 1)                    # lights off

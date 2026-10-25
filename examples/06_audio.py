"""06 - Audio: which way is a sound coming from, and recording a clip on the robot.

What the robot gives you:
  - the direction of a sound (Left / Right / Front / Back)
  - speech to text via start_audio_asr_doa() (it can return nothing on some robots)
  - recording a clip ON the robot and playing it back
It does NOT stream raw microphone audio to your laptop. For your own speech recognition,
use your laptop's microphone.

    python examples/06_audio.py direction     # clap or talk near the robot
    python examples/06_audio.py record        # records 3 s on the robot, then plays it back
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sys
import time
from robot import connect

mode = sys.argv[1] if len(sys.argv) > 1 else "direction"
got = connect()

if mode == "direction":
    got.enable_audio_direction()
    try:
        for _ in range(40):
            side = got.get_audio_direction()          # 'Left', 'Right', 'Front', 'Back', or '' for no sound
            if side:
                print("sound from:", side)
            time.sleep(0.25)
    finally:
        got.disable_audio_direction()

elif mode == "record":
    # Recording is not wrapped by the high-level SDK, so we call the robot's audio service directly.
    from ugot.grpc_pb import audio_pb2
    audio = got.AUDIO.client
    RECORDED = 1                                     # clip type: recorded on the robot
    print("recording for 3 seconds, make a noise...")
    audio.startRecordAudioFile(audio_pb2.AudioEmptyRequest())
    time.sleep(3)
    audio.stopRecordAudioFile(audio_pb2.AudioEmptyRequest())
    # stopping is not enough: the clip is only kept once you give it a name
    audio.insertAudioFile(audio_pb2.AudioFileRequest(audio_name="my_clip", audio_type=RECORDED))
    audio.playAudioFile(audio_pb2.AudioPlayRequest(audio_file="my_clip", audio_type=RECORDED))
    print("playing it back")
else:
    sys.exit("use: direction or record")

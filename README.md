# RoboMasters Treasure Hunt: UGOT starter kit

Small, copy-and-edit Python examples for the UGOT robot. Each one does one thing, so you can
see how it works and build on it. You program the robot from your laptop over Wi-Fi.
Nothing needs installing on the robot.

## Set up

You need Python 3 (3.11 works) and your laptop on the same Wi-Fi as the robot. Switch off any VPN.

```bash
git clone https://github.com/LEC-AI/robomasters-1-ugot-starter-kit
cd robomasters-1-ugot-starter-kit
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python examples/01_connect.py
```

If `01_connect.py` prints your robot's name and battery, you are ready.

## The examples

| Run | What it shows | Moves the robot? |
|---|---|---|
| `examples/01_connect.py` | Find a robot, read battery, volume and build | no |
| `examples/02_speak_light_screen.py` | Speech, sound effects, lights, screen and faces | no |
| `examples/03_camera_frames.py` | **Get camera frames** as JPEG bytes; save them or view live | no |
| `examples/04_tags_and_qr.py` | AprilTags (id, distance, bearing) and QR codes | no |
| `examples/05_colours.py` | Find coloured objects | no |
| `examples/06_audio.py` | **Sound direction**, and recording and playback on the robot | no |
| `examples/07_drive.py` | Drive with a safe speed ramp and a guaranteed stop | **yes** |
| `examples/08_arm_gripper.py` | Arm and gripper (engineer build) | **yes** |
| `hunt_template.py` | The six checkpoints as empty functions to fill in | when you add it |

## What can I get from the robot?

- **Camera:** `got.open_camera()` once, then `got.read_camera_data()` returns a JPEG as bytes, or `None` if no new frame is ready. Decode it with Pillow or OpenCV and run your own detector.
- **Vision on the robot:** `got.load_models([...])` then read results. Models include `apriltag_qrcode`, `color_recognition`, `word_recognition`, `face_recognition`, `gesture`, `human_pose`, `traffic_sign`, `line_recognition`. Call `got.release_models()` when done.
- **Audio:** which side a sound came from, speech to text, and recording a clip on the robot. The robot does not stream raw microphone audio to your laptop. Use your laptop's mic if you want that.
- **Sensors:** `get_power_status()`, `read_gyro_data()`, `get_attitude()`, `read_distance_data(port)`.
- **Movement:** `model_common_move(speed, turn)` works on every build.

Every SDK method has a docstring: `python -c "from ugot import ugot; help(ugot.UGOT)"`

## If something goes wrong

- **No robots found:** same Wi-Fi? VPN off? Robot switched on? Wi-Fi that isolates devices from each other blocks discovery. Pass `connect(ip="...")` if you know the robot's address.
- **No sound:** the robot may be muted. `01_connect.py` tells you. Unmute it in the UGOT app or on the robot.
- **Robot will not move, build is `box`:** the SDK ignores movement commands in that mode. Check the robot is assembled and its build is selected.
- **`UNIMPLEMENTED` when connecting:** `robot.py` already handles this for you. If you call `got.initialize(ip)` yourself, use `connect()` instead.
- **The robot wobbles or tips:** change speed gradually, as in `07_drive.py`.

## Safety

Clear half a metre around a robot before it moves. Put a time limit on every move and always call
`stop(got)` in a `finally` block. Keep speeds at 10 to 20 cm/s while testing. Ask before moving a
robot someone else is using.

# FPS Movement Tracker

Professional FPS game movement tracking system for PS4 capture card input. Track player movement, enemies, velocity, and generate detailed analysis reports.

## Features

✅ **Real-time Movement Tracking**
- PS4 capture card integration (4K 1080p60)
- Color-based player detection (black/white/red outfit)
- Motion detection using optical flow
- Player velocity and acceleration calculation

✅ **Multi-object Detection**
- Track player position and movement
- Detect enemy/moving objects
- Animation state recognition
- Movement trajectory recording

✅ **Data Recording & Analysis**
- Save movement data (JSON + Pickle binary)
- Playback recorded sessions
- Generate statistics and heatmaps
- Export analysis reports

✅ **Easy to Use**
- Simple menu-driven interface
- Works in VS Code
- One-command setup
- Real-time visualization

---

## Installation

### Step 1: Prerequisites
- Python 3.8+
- VS Code (recommended)
- PS4 capture card connected to PC

### Step 2: Install Dependencies

Run setup script (automatic):
```bash
python setup.py
```

Or manual install:
```bash
pip install -r requirements.txt
```

**If OpenCV import error occurs**, try:
```bash
pip install opencv-python opencv-contrib-python --upgrade --force-reinstall
```

---

## Quick Start

### Run the tracker:
```bash
python main.py
```

### Main Menu Options:
1. **Live Tracking** - Stream from PS4 capture card
2. **Analyze Video** - Load and analyze recorded video file
3. **Playback** - Review saved movement data
4. **Settings** - Configure tracking parameters

---

## Usage Guide

### Live Tracking Mode
```
1. Connect PS4 capture card to PC
2. Run: python main.py
3. Select option 1 (Live Tracking)
4. Controls:
   - Q: Quit tracking
   - S: Save current data
   - P: Playback recording
```

### Recording Video
```
- Live tracking automatically records movement data
- Files saved to: output/movement_YYYYMMDD_HHMMSS.json
- Also saves: .pkl (binary) format for faster loading
```

### Analyze Recorded Video
```
1. Run: python main.py
2. Select option 2
3. Enter path to video file
4. Tracker analyzes movement frame by frame
5. Data saved automatically
```

### Playback Analysis
```
1. Run: python main.py
2. Select option 3
3. Enter saved data file (.json or .pkl)
4. Press Space to pause, Q to quit
```

---

## Configuration

Edit `config.json` to customize:

```json
{
  "camera": {
    "device_id": 0,           // Capture card ID
    "resolution": [1920, 1080],
    "fps": 60
  },
  "color_ranges": {
    "player_black": {...},    // Player outfit colors
    "player_red": {...},
    "player_white": {...}
  },
  "motion_detection": {
    "sensitivity": 10,        // Optical flow threshold
    "min_motion_area": 100
  },
  "output_directory": "output"
}
```

---

## Output Files

### Saved Data Formats

**JSON** (`movement_YYYYMMDD_HHMMSS.json`)
- Human-readable format
- Contains all frame data
- Good for analysis/export

**Pickle** (`movement_YYYYMMDD_HHMMSS.pkl`)
- Binary format (faster to load)
- Complete movement history
- Recommended for large files

### Analysis Report
```
movement_analysis_YYYYMMDD_HHMMSS.txt

Contains:
- Total frames and duration
- Player movement statistics
- Velocity analysis
- Animation states detected
- Object detection summary
```

---

## Real-time Display

The tracker shows:
- **Player position** (green circle)
- **Velocity vector** (magenta arrow)
- **Motion vectors** (cyan arrows)
- **Detected objects** (red boxes)
- **Animation states** (text labels)
- **FPS and statistics** (HUD)

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Q | Quit tracker |
| S | Save current data |
| P | Toggle playback |
| Space | Pause (playback mode) |

---

## Data Structure

Movement data saved as JSON:
```json
{
  "frame": 100,
  "timestamp": 1.67,
  "player_position": [960, 540],
  "player_velocity": [45.2, -12.3],
  "enemy_positions": [
    {"center": [500, 300], "bounds": [480, 280, 40, 40], "area": 1600}
  ],
  "animations": ["moving_sideways"],
  "motion_vectors": [...]
}
```

---

## Troubleshooting

### ImportError: No module named 'cv2'
```bash
pip install opencv-python --upgrade --force-reinstall
pip install opencv-contrib-python
```

### Camera not detected
- Check capture card is connected
- Try device_id 1, 2, etc. in config.json
- Run: `ls /dev/video*` (Linux) or check Device Manager (Windows)

### Low FPS / Stuttering
- Reduce resolution in config.json
- Lower motion detection sensitivity
- Close other applications

### No player detection
- Adjust color ranges in config.json
- Ensure good lighting on player
- Check outfit colors match configuration

---

## Performance

- **1080p60**: ~30-40ms per frame
- **4K processing**: Downscaled to 1080p for real-time performance
- **Motion detection**: Optical flow calculation ~15-20ms
- **Memory**: ~500MB for 60 seconds of tracking

---

## API Usage (Advanced)

```python
from fps_tracker import FPSMovementTracker

# Initialize
tracker = FPSMovementTracker(
    input_source="camera",
    resolution=(1920, 1080),
    fps=60,
    enable_recording=True,
    enable_analysis=True
)

# Start tracking
tracker.start_tracking()

# Analyze video
tracker.analyze_video()

# Access movement data
print(f"Frames tracked: {len(tracker.movement_history)}")
print(f"Player positions: {[f['player_position'] for f in tracker.movement_history]}")
```

---

## Requirements

- Python 3.8+
- OpenCV 4.8+
- NumPy 1.24+
- Pillow 10+
- Matplotlib 3.7+
- scikit-image 0.21+
- SciPy 1.11+

---

## License

Open source - modify and distribute freely

## Support

For issues:
1. Check troubleshooting section
2. Verify config.json settings
3. Review OpenCV installation
4. Check capture card connection

---

**Ready to track? Run `python main.py` now!** 🎮

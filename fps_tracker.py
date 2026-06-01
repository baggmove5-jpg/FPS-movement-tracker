"""
Core FPS Movement Tracker
Handles video input, tracking, and data recording
"""

import cv2
import numpy as np
import json
import pickle
from datetime import datetime
from pathlib import Path
import time

from movement_detector import MovementDetector
from color_tracker import ColorTracker
from data_manager import DataManager
from visualizer import Visualizer

class FPSMovementTracker:
    def __init__(self, input_source="camera", resolution=(1920, 1080), fps=60):
        """Initialize tracker"""
        self.input_source = input_source
        self.width, self.height = resolution
        self.fps = fps
        self.frame_time = 1.0 / fps
        
        self.movement_detector = MovementDetector()
        self.color_tracker = ColorTracker()
        self.data_manager = DataManager()
        self.visualizer = Visualizer(resolution)
        
        self.movement_history = []
        self.frame_count = 0
        self.start_time = None
        
        self.config = self._load_config()
        
        print(f"✓ FPS Movement Tracker initialized")
        print(f"  Resolution: {self.width}x{self.height}")
        print(f"  FPS: {fps}")
    
    def _load_config(self):
        """Load configuration from config.json"""
        config_file = Path("config.json")
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        
        return {
            "color_ranges": {
                "player_black": {"lower": [0, 0, 0], "upper": [50, 50, 50]},
                "player_red": {"lower": [200, 0, 0], "upper": [255, 100, 100]},
                "player_white": {"lower": [200, 200, 200], "upper": [255, 255, 255]}
            },
            "output_directory": "output"
        }
    
    def start_tracking(self):
        """Start live tracking from camera/capture card"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        if not cap.isOpened():
            print("ERROR: Could not open camera!")
            return
        
        self.start_time = time.time()
        print("\n🎮 TRACKING (Q=Quit | S=Save)\n")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.resize(frame, (self.width, self.height))
                results = self._process_frame(frame)
                
                display = self.visualizer.draw_results(frame.copy(), results)
                cv2.imshow("FPS Tracker", display)
                
                self.frame_count += 1
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    self.save_data()
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"\n💾 Saving {len(self.movement_history)} frames...")
            self.save_data()
    
    def analyze_video(self, video_path):
        """Analyze a recorded video file"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"ERROR: Could not open {video_path}")
            return
        
        print(f"\n📊 Analyzing: {video_path}\n")
        self.start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.resize(frame, (self.width, self.height))
                results = self._process_frame(frame)
                
                display = self.visualizer.draw_results(frame.copy(), results)
                cv2.imshow("Analysis", display)
                
                self.frame_count += 1
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self._print_stats()
            self.save_data()
    
    def _process_frame(self, frame):
        """Process single frame for tracking"""
        results = {
            "frame": self.frame_count,
            "timestamp": time.time() - self.start_time,
            "player_position": None,
            "enemy_positions": [],
            "motion_vectors": [],
            "player_velocity": None,
            "animations": []
        }
        
        player = self.color_tracker.track_player(frame, self.config)
        if player:
            results["player_position"] = player["center"]
            results["animations"] = player.get("animations", [])
        
        motion = self.movement_detector.detect_motion(frame)
        results["motion_vectors"] = motion["vectors"]
        results["enemy_positions"] = motion["moving_objects"]
        
        if self.movement_history:
            prev = self.movement_history[-1]
            if prev["player_position"] and results["player_position"]:
                dt = results["timestamp"] - prev["timestamp"]
                if dt > 0:
                    dx = results["player_position"][0] - prev["player_position"][0]
                    dy = results["player_position"][1] - prev["player_position"][1]
                    results["player_velocity"] = [dx/dt, dy/dt]
        
        self.movement_history.append(results)
        return results
    
    def save_data(self):
        """Save movement data to files"""
        if not self.movement_history:
            return
        
        out = Path(self.config["output_directory"])
        out.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_f = out / f"movement_{ts}.json"
        with open(json_f, "w") as f:
            json.dump([{
                "frame": f["frame"],
                "timestamp": f["timestamp"],
                "player_position": f["player_position"],
                "player_velocity": f["player_velocity"],
                "enemy_positions": f["enemy_positions"]
            } for f in self.movement_history], f, indent=2)
        print(f"✓ {json_f}")
        
        pkl_f = out / f"movement_{ts}.pkl"
        with open(pkl_f, "wb") as f:
            pickle.dump(self.movement_history, f)
        print(f"✓ {pkl_f}")
    
    def playback_analysis(self):
        """Playback and visualize recorded tracking data"""
        if not self.movement_history:
            return
        
        print("▶️  PLAYBACK (Q=Quit | Space=Pause)\n")
        paused = False
        idx = 0
        
        while idx < len(self.movement_history):
            if paused:
                idx -= 1
            
            f = self.movement_history[idx]
            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            
            results = {
                "frame": f["frame"],
                "timestamp": f["timestamp"],
                "player_position": f["player_position"],
                "player_velocity": f["player_velocity"],
                "enemy_positions": f["enemy_positions"],
                "animations": f["animations"],
                "motion_vectors": []
            }
            
            display = self.visualizer.draw_results(img, results)
            cv2.imshow("Playback", display)
            
            key = cv2.waitKey(int(1000/self.fps)) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                paused = not paused
            else:
                idx += 1
        
        cv2.destroyAllWindows()
        self._print_stats()
    
    def _print_stats(self):
        """Print movement statistics"""
        if not self.movement_history:
            return
        
        print("\n" + "="*50)
        print("STATISTICS")
        print("="*50)
        print(f"Frames: {len(self.movement_history)}")
        print(f"Duration: {self.movement_history[-1]['timestamp']:.2f}s")
        
        pos = [f["player_position"] for f in self.movement_history if f["player_position"]]
        if pos:
            pos = np.array(pos)
            print(f"Player: {len(pos)} detections")
            print(f"  X: {pos[:, 0].min():.0f} - {pos[:, 0].max():.0f}")
            print(f"  Y: {pos[:, 1].min():.0f} - {pos[:, 1].max():.0f}")
        
        vel = [f["player_velocity"] for f in self.movement_history if f["player_velocity"]]
        if vel:
            vel = np.array(vel)
            speeds = np.linalg.norm(vel, axis=1)
            print(f"Velocity: max={speeds.max():.1f}, avg={speeds.mean():.1f} px/s")
        print("="*50)
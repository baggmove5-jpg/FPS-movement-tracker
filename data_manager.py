"""
Data Management Module
Save, load, and analyze movement data
"""

import json
import pickle
from pathlib import Path
from datetime import datetime
import numpy as np

class DataManager:
    def __init__(self):
        """Initialize data manager"""
        self.data = []
        self.metadata = {}
    
    def save_as_json(self, filepath, movement_data):
        """Save movement data as JSON"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        json_data = []
        for frame in movement_data:
            json_data.append({
                "frame": frame.get("frame"),
                "timestamp": frame.get("timestamp"),
                "player_position": frame.get("player_position"),
                "player_velocity": frame.get("player_velocity"),
                "enemy_positions": frame.get("enemy_positions", []),
                "animations": frame.get("animations", [])
            })
        
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        return filepath
    
    def save_as_pickle(self, filepath, movement_data):
        """Save movement data as Pickle (binary, faster)"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(movement_data, f)
        
        return filepath
    
    def load_from_json(self, filepath):
        """Load movement data from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.data = data
        return data
    
    def load_from_pickle(self, filepath):
        """Load movement data from Pickle"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.data = data
        return data
    
    def analyze_movement(self, movement_data):
        """Analyze movement data and generate statistics"""
        analysis = {
            "total_frames": len(movement_data),
            "duration_seconds": 0,
            "player_stats": {},
            "velocity_stats": {}
        }
        
        if not movement_data:
            return analysis
        
        if len(movement_data) > 1:
            analysis["duration_seconds"] = (
                movement_data[-1]["timestamp"] - movement_data[0]["timestamp"]
            )
        
        # Player position analysis
        player_positions = [f["player_position"] for f in movement_data
                          if f["player_position"]]
        
        if player_positions:
            player_pos_array = np.array(player_positions)
            analysis["player_stats"] = {
                "detections": len(player_positions),
                "x_min": float(player_pos_array[:, 0].min()),
                "x_max": float(player_pos_array[:, 0].max()),
                "y_min": float(player_pos_array[:, 1].min()),
                "y_max": float(player_pos_array[:, 1].max()),
                "x_mean": float(player_pos_array[:, 0].mean()),
                "y_mean": float(player_pos_array[:, 1].mean())
            }
        
        # Velocity analysis
        velocities = [f["player_velocity"] for f in movement_data
                     if f["player_velocity"]]
        
        if velocities:
            vel_array = np.array(velocities)
            speeds = np.linalg.norm(vel_array, axis=1)
            analysis["velocity_stats"] = {
                "max_speed": float(speeds.max()),
                "min_speed": float(speeds.min()),
                "mean_speed": float(speeds.mean()),
                "std_speed": float(speeds.std())
            }
        
        return analysis
    
    def export_statistics(self, movement_data, output_file):
        """Export analysis as text report"""
        analysis = self.analyze_movement(movement_data)
        
        report = []
        report.append("=" * 60)
        report.append("FPS MOVEMENT ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().isoformat()}\n")
        
        report.append("SUMMARY")
        report.append(f"  Total Frames: {analysis['total_frames']}")
        report.append(f"  Duration: {analysis['duration_seconds']:.2f}s")
        
        if analysis["player_stats"]:
            report.append("\nPLAYER MOVEMENT")
            stats = analysis["player_stats"]
            report.append(f"  Detections: {stats['detections']}")
            report.append(f"  X Range: {stats['x_min']:.0f} - {stats['x_max']:.0f}")
            report.append(f"  Y Range: {stats['y_min']:.0f} - {stats['y_max']:.0f}")
            report.append(f"  Center: ({stats['x_mean']:.0f}, {stats['y_mean']:.0f})")
        
        if analysis["velocity_stats"]:
            report.append("\nVELOCITY")
            stats = analysis["velocity_stats"]
            report.append(f"  Max Speed: {stats['max_speed']:.2f} px/s")
            report.append(f"  Avg Speed: {stats['mean_speed']:.2f} px/s")
        
        report.append("\n" + "=" * 60)
        
        with open(output_file, 'w') as f:
            f.write("\n".join(report))
"""
Visualization Module
Draw tracking results on frames
"""

import cv2
import numpy as np

class Visualizer:
    def __init__(self, resolution=(1920, 1080)):
        """Initialize visualizer"""
        self.width, self.height = resolution
        self.colors = {
            "player": (0, 255, 0),      # Green
            "enemy": (0, 0, 255),       # Red
            "motion": (255, 255, 0),    # Cyan
            "velocity": (255, 0, 255),  # Magenta
            "text": (255, 255, 255),    # White
            "grid": (100, 100, 100)     # Gray
        }
    
    def draw_results(self, frame, results):
        """Draw all tracking results on frame"""
        output = frame.copy()
        
        # Draw grid
        self._draw_grid(output)
        
        # Draw player
        if results.get("player_position"):
            self._draw_player(output, results)
        
        # Draw enemies
        if results.get("enemy_positions"):
            self._draw_enemies(output, results)
        
        # Draw motion vectors
        if results.get("motion_vectors"):
            self._draw_motion_vectors(output, results)
        
        # Draw HUD
        self._draw_hud(output, results)
        
        return output
    
    def _draw_grid(self, frame):
        """Draw reference grid"""
        grid_spacing = 100
        
        for x in range(0, self.width, grid_spacing):
            cv2.line(frame, (x, 0), (x, self.height), self.colors["grid"], 1)
        
        for y in range(0, self.height, grid_spacing):
            cv2.line(frame, (0, y), (self.width, y), self.colors["grid"], 1)
    
    def _draw_player(self, frame, results):
        """Draw player position and velocity"""
        pos = results["player_position"]
        
        if pos:
            # Draw player center
            cv2.circle(frame, (int(pos[0]), int(pos[1])), 10,
                      self.colors["player"], -1)
            cv2.circle(frame, (int(pos[0]), int(pos[1])), 10,
                      self.colors["text"], 2)
            
            # Draw velocity vector
            if results.get("player_velocity"):
                vel = results["player_velocity"]
                vel_scale = 5
                end_point = (int(pos[0] + vel[0] * vel_scale),
                           int(pos[1] + vel[1] * vel_scale))
                cv2.arrowedLine(frame, (int(pos[0]), int(pos[1])),
                              end_point, self.colors["velocity"], 2)
                
                # Speed text
                speed = np.sqrt(vel[0]**2 + vel[1]**2)
                cv2.putText(frame, f"Speed: {speed:.1f} px/s",
                          (int(pos[0]) + 20, int(pos[1]) - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                          self.colors["velocity"], 1)
            
            # Animation state
            if results.get("animations"):
                anim_text = ", ".join(results["animations"][:2])
                cv2.putText(frame, anim_text,
                          (int(pos[0]) + 20, int(pos[1]) + 20),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                          self.colors["text"], 1)
    
    def _draw_enemies(self, frame, results):
        """Draw enemy/moving object positions"""
        for i, enemy in enumerate(results.get("enemy_positions", [])):
            center = enemy["center"]
            bounds = enemy["bounds"]
            
            # Draw bounding box
            x, y, w, h = bounds
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                         self.colors["enemy"], 2)
            
            # Draw center
            cv2.circle(frame, (int(center[0]), int(center[1])), 5,
                      self.colors["enemy"], -1)
            
            # Label
            cv2.putText(frame, f"E{i}", (x + 5, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                       self.colors["enemy"], 1)
    
    def _draw_motion_vectors(self, frame, results):
        """Draw motion vectors"""
        for vector in results.get("motion_vectors", [])[:50]:
            pos = vector["position"]
            vel = vector["vector"]
            magnitude = vector["magnitude"]
            
            end_x = int(pos[0] + vel[0] * 2)
            end_y = int(pos[1] + vel[1] * 2)
            
            color_intensity = min(255, int(magnitude * 10))
            color = (100, color_intensity, 100)
            
            cv2.arrowedLine(frame, (int(pos[0]), int(pos[1])),
                          (end_x, end_y), color, 1)
    
    def _draw_hud(self, frame, results):
        """Draw HUD information"""
        y_offset = 30
        x_offset = 10
        
        cv2.putText(frame, f"Frame: {results['frame']}",
                   (x_offset, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                   self.colors["text"], 1)
        
        cv2.putText(frame, f"Time: {results['timestamp']:.2f}s",
                   (x_offset, y_offset + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                   self.colors["text"], 1)
        
        enemy_count = len(results.get("enemy_positions", []))
        cv2.putText(frame, f"Objects: {enemy_count}",
                   (x_offset, y_offset + 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                   self.colors["text"], 1)
        
        cv2.putText(frame, "Q:Quit | S:Save",
                   (x_offset, self.height - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                   self.colors["grid"], 1)
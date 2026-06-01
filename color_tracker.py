"""
Color-Based Player Tracking
Track player by outfit color (black, white, red)
"""

import cv2
import numpy as np

class ColorTracker:
    def __init__(self):
        """Initialize color tracker"""
        self.tracked_positions = []
        self.tracking_id = None
    
    def track_player(self, frame, config):
        """
        Track player by color in frame
        
        Args:
            frame: BGR image
            config: config dict with color_ranges
        
        Returns:
            dict with player position and metadata
        """
        player_data = {
            "center": None,
            "contours": [],
            "animations": [],
            "confidence": 0
        }
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        colors = config.get("color_ranges", {})
        combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        
        # Create mask for all player colors
        for color_name, color_range in colors.items():
            lower = np.array(color_range["lower"])
            upper = np.array(color_range["upper"])
            
            # Convert RGB to HSV
            lower_hsv = cv2.cvtColor(np.uint8([[lower]]), cv2.COLOR_BGR2HSV)[0][0]
            upper_hsv = cv2.cvtColor(np.uint8([[upper]]), cv2.COLOR_BGR2HSV)[0][0]
            
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(
            combined_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return None
        
        # Find largest contour (main player)
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        if area < 100:
            return None
        
        # Get center
        M = cv2.moments(largest_contour)
        if M["m00"] == 0:
            return None
        
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        player_data["center"] = (cx, cy)
        player_data["contours"] = [largest_contour]
        player_data["confidence"] = min(1.0, area / 10000)
        
        # Detect animation state
        player_data["animations"] = self._detect_animation_state(largest_contour)
        
        return player_data
    
    def _detect_animation_state(self, contour):
        """Detect player animation state from silhouette"""
        animations = []
        
        x, y, w, h = cv2.boundingRect(contour)
        
        # Aspect ratio analysis
        aspect_ratio = float(w) / h if h > 0 else 0
        
        if aspect_ratio > 0.8:
            animations.append("moving_sideways")
        elif aspect_ratio < 0.5:
            animations.append("idle_or_walking")
        
        # Convexity analysis
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        contour_area = cv2.contourArea(contour)
        
        if hull_area > 0:
            solidity = float(contour_area) / hull_area
            if solidity < 0.7:
                animations.append("jumping_or_falling")
        
        return animations
    
    def update_tracking(self, new_center, max_distance=50):
        """Update tracking with new position"""
        if self.tracking_id is None:
            self.tracking_id = 0
        
        if len(self.tracked_positions) > 0:
            last_pos = self.tracked_positions[-1]
            distance = np.sqrt((new_center[0] - last_pos[0])**2 +
                             (new_center[1] - last_pos[1])**2)
            
            if distance > max_distance:
                self.tracking_id = None
                return False
        
        self.tracked_positions.append(new_center)
        
        # Keep last 100 positions
        if len(self.tracked_positions) > 100:
            self.tracked_positions.pop(0)
        
        return True
"""
Motion Detection Module
Optical flow-based movement detection
"""

import cv2
import numpy as np

class MovementDetector:
    def __init__(self):
        """Initialize motion detector"""
        self.prev_gray = None
        self.prev_frame = None
    
    def detect_motion(self, frame):
        """
        Detect motion using optical flow (Farneback method)
        
        Returns:
            dict with motion vectors and moving objects
        """
        results = {
            "vectors": [],
            "moving_objects": [],
            "flow_magnitude": None
        }
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.prev_gray is not None:
            # Calculate optical flow
            flow = cv2.calcOpticalFlowFarneback(
                self.prev_gray, gray,
                None, 0.5, 3, 15, 3, 5, 1.2, 0
            )
            
            # Get magnitude
            results["flow_magnitude"] = cv2.magnitude(flow[..., 0], flow[..., 1])
            
            # Convert to magnitude and angle
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            
            # Threshold motion
            threshold = np.percentile(mag, 70)
            motion_mask = mag > threshold
            
            # Find moving objects
            motion_mask_uint8 = motion_mask.astype(np.uint8) * 255
            motion_mask_uint8 = cv2.morphologyEx(
                motion_mask_uint8,
                cv2.MORPH_CLOSE,
                cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            )
            
            contours, _ = cv2.findContours(
                motion_mask_uint8,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 5 and h > 5:
                    results["moving_objects"].append({
                        "center": (x + w // 2, y + h // 2),
                        "bounds": (x, y, w, h),
                        "area": w * h
                    })
            
            # Extract motion vectors
            vectors = []
            h_img, w_img = flow.shape[:2]
            
            for y in range(0, h_img, 20):
                for x in range(0, w_img, 20):
                    if motion_mask[y, x]:
                        fx, fy = flow[y, x]
                        magnitude = np.sqrt(fx*fx + fy*fy)
                        if magnitude > 1:
                            vectors.append({
                                "position": (x, y),
                                "vector": (fx, fy),
                                "magnitude": magnitude
                            })
            
            results["vectors"] = vectors
        
        self.prev_gray = gray
        self.prev_frame = frame
        
        return results
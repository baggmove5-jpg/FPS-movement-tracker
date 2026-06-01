"""FPS Movement Tracker - Main Entry Point
Easy menu-driven interface for tracking PS4 capture input
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fps_tracker import FPSMovementTracker

def main():
    print("="*60)
    print("FPS MOVEMENT TRACKER v1.0")
    print("="*60)
    print("\n🎮 OPTIONS:")
    print("  1. Live Tracking (PS4 Capture Card)")
    print("  2. Analyze Video File")
    print("  3. Playback Saved Data")
    print("  4. View Settings")
    print("\nEnter choice (1-4): ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        print("\nStarting live tracking...")
        tracker = FPSMovementTracker(input_source="camera", resolution=(1920, 1080), fps=60)
        tracker.start_tracking()
    
    elif choice == "2":
        video = input("Enter video path: ").strip()
        if os.path.exists(video):
            tracker = FPSMovementTracker(resolution=(1920, 1080), fps=60)
            tracker.analyze_video(video)
        else:
            print(f"File not found: {video}")
    
    elif choice == "3":
        data_file = input("Enter data file path (.json/.pkl): ").strip()
        if os.path.exists(data_file):
            tracker = FPSMovementTracker()
            if data_file.endswith('.json'):
                tracker.movement_history = tracker.data_manager.load_from_json(data_file)
            else:
                tracker.movement_history = tracker.data_manager.load_from_pickle(data_file)
            print(f"✓ Loaded {len(tracker.movement_history)} frames")
            tracker.playback_analysis()
        else:
            print(f"File not found: {data_file}")
    
    elif choice == "4":
        print("\nEdit config.json to customize settings:")
        print("  - Camera ID / Resolution")
        print("  - Color ranges for player detection")
        print("  - Motion sensitivity")
        print("  - Output folder")
    
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nStopped.")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
"""
Setup script for FPS Movement Tracker
Run: python setup.py
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python dependencies"""
    print("=" * 60)
    print("FPS MOVEMENT TRACKER - SETUP")
    print("=" * 60)
    
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        requirements = [
            "opencv-python==4.8.1.78",
            "opencv-contrib-python==4.8.1.78",
            "numpy==1.24.3",
            "Pillow==10.0.0",
            "matplotlib==3.7.2",
            "scikit-image==0.21.0",
            "scipy==1.11.2"
        ]
        
        for package in requirements:
            print(f"\n  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("\n✅ All dependencies installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("\nTo start tracking:")
    print("  python main.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    install_requirements()

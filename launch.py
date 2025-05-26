#!/usr/bin/env python3
"""
Quick Signal Analyzer Launcher
Simple script to quickly launch the main signal analyzer
"""

import subprocess
import sys
import os

def main():
    print("🤖 Telegram Signal Analyzer Launcher")
    print("=" * 40)
    
    # Check if main analyzer exists
    analyzer_path = "signal_analyzer.py"
    if not os.path.exists(analyzer_path):
        print("❌ Main analyzer not found!")
        print("Please ensure signal_analyzer.py exists in the current directory.")
        return
    
    # Check dependencies
    try:
        import pandas
        import numpy
        import sklearn
        print("✅ Dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Launch main analyzer
    print("🚀 Launching Signal Analyzer...")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, analyzer_path], check=True)
    except KeyboardInterrupt:
        print("\n👋 Analyzer stopped by user")
    except Exception as e:
        print(f"❌ Error launching analyzer: {e}")

if __name__ == "__main__":
    main()

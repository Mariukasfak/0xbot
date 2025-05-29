#!/usr/bin/env python3
"""
0xBot Launcher - Unified Signal Analysis Platform
Simple launcher for the comprehensive crypto signal analysis system
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_and_install_dependencies():
    """Check and auto-install required dependencies"""
    print("🔧 Checking dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✅ All dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_sample_data():
    """Create sample data if not exists"""
    if not os.path.exists('parsed_telegram_data.csv'):
        print("📊 Creating sample data...")
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Create sample telegram data
        sample_data = []
        strategies = ['Viper Vision', 'Cobra Scan', 'Alpha Hunter']
        tokens = ['MEME', 'PEPE', 'DOGE', 'SHIB', 'BONK', 'WIF', 'POPCAT']
        
        for i in range(100):
            date = datetime.now() - timedelta(days=np.random.randint(1, 30))
            sample_data.append({
                'date': date,
                'strategy': np.random.choice(strategies),
                'token_name': f"{np.random.choice(tokens)}{np.random.randint(1, 999)}",
                'contract_address': f"0x{''.join([f'{np.random.randint(0,15):x}' for _ in range(40)])}",
                'initial_mc': f"${np.random.randint(10, 500)}K",
                'initial_mc_value': np.random.randint(10000, 500000),
                'max_gain': np.random.uniform(-0.5, 10.0),
                'top_holders_percent': np.random.uniform(20, 60),
                'initial_lp_sol': np.random.uniform(5, 100),
                'lp_burned': np.random.choice([True, False]),
                'freeze_disabled': np.random.choice([True, False]),
                'mint_disabled': np.random.choice([True, False])
            })
        
        df = pd.DataFrame(sample_data)
        df.to_csv('parsed_telegram_data.csv', index=False)
        print("✅ Sample data created!")

    # Create ML report if it doesn't exist
    if not os.path.exists('advanced_ml_report.json'):
        import json
        
        ml_report = {
            'timestamp': str(datetime.now()),
            'model_performance': {
                'accuracy': 0.732,
                'precision': 0.685,
                'recall': 0.718,
                'f1_score': 0.701
            },
            'insights': {
                'feature_importance': {
                    'initial_mc_value': 0.25,
                    'top_holders_percent': 0.22,
                    'lp_burned': 0.18,
                    'strategy_encoded': 0.15
                },
                'success_rate_by_strategy': {
                    'Viper Vision': 0.68,
                    'Cobra Scan': 0.71,
                    'Alpha Hunter': 0.65
                }
            }
        }
        
        with open('advanced_ml_report.json', 'w') as f:
            json.dump(ml_report, f, indent=2)
        print("✅ Sample ML report created!")

def main():
    """Main launcher function"""
    print("🤖 0xBot - Crypto Signal Intelligence Platform")
    print("=" * 50)
    
    # Check dependencies
    if not check_and_install_dependencies():
        print("❌ Failed to install dependencies. Please check your Python environment.")
        return
    
    # Create sample data if needed
    create_sample_data()
    
    print("\n🚀 Starting 0xBot Web Dashboard...")
    print("📊 This will open the comprehensive signal analysis platform")
    print("🔍 Features included:")
    print("   • Live signal analysis with AI predictions")
    print("   • Advanced wallet & holder analysis")
    print("   • Deployer intelligence & reputation")
    print("   • Historical performance tracking")
    print("   • ML model training center")
    print("\n" + "=" * 50)
    print("📡 Opening dashboard at: http://localhost:8501")
    print("⚠️ To stop the dashboard, press Ctrl+C")
    print("=" * 50)
    
    try:
        # Launch the Streamlit dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_dashboard.py", 
            "--server.port=8501",
            "--server.headless=false",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure you have Python 3.8+ installed")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Try running manually: streamlit run web_dashboard.py")

if __name__ == "__main__":
    main()

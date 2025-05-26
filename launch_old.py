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
    
    try:
        # Launch the Streamlit dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_dashboard.py", 
            "--server.port=8501",
            "--server.headless=true",
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
    
    # Check if data files exist
    data_files = [
        'parsed_telegram_data.csv',
        'advanced_ml_report.json'
    ]
    
    missing_files = []
    for file in data_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ Missing data files: {', '.join(missing_files)}")
        print("Creating sample data files...")
        create_sample_data()
    
    print("✅ Environment setup complete!")

def create_sample_data():
    """Create sample data files for testing"""
    import pandas as pd
    import json
    from datetime import datetime, timedelta
    import numpy as np
    
    # Create sample telegram data
    sample_data = []
    strategies = ['Viper Vision', 'Cobra Scan', 'Eagle Eye']
    
    for i in range(100):
        date = datetime.now() - timedelta(days=np.random.randint(1, 30))
        sample_data.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'strategy': np.random.choice(strategies),
            'token_name': f'TestToken{i}',
            'initial_mc_value': np.random.uniform(10000, 500000),
            'max_gain': np.random.uniform(-50, 300),
            'top_holders_percent': np.random.uniform(20, 60),
            'initial_lp_sol': np.random.uniform(5, 100),
            'lp_burned': np.random.choice([True, False]),
            'freeze_disabled': np.random.choice([True, False]),
            'mint_disabled': np.random.choice([True, False])
        })
    
    df = pd.DataFrame(sample_data)
    df.to_csv('parsed_telegram_data.csv', index=False)
    print("✅ Created sample telegram data")
    
    # Create sample ML report
    ml_report = {
        'timestamp': datetime.now().isoformat(),
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
                'strategy_encoded': 0.15,
                'initial_lp_sol': 0.12,
                'hour': 0.08
            },
            'success_rate_by_strategy': {
                'Viper Vision': 0.68,
                'Cobra Scan': 0.71,
                'Eagle Eye': 0.65
            }
        }
    }
    
    with open('advanced_ml_report.json', 'w') as f:
        json.dump(ml_report, f, indent=2)
    print("✅ Created sample ML report")

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching 0xBot Web Dashboard...")
    print("📡 The dashboard will open in your web browser")
    print("🔗 URL: http://localhost:8501")
    print("")
    print("💡 Features available:")
    print("   • Live Signal Analysis")
    print("   • Deep Wallet Analysis")
    print("   • Deployer Intelligence")
    print("   • AI Training Center")
    print("   • Historical Performance")
    print("")
    print("⚠️ To stop the dashboard, press Ctrl+C in this terminal")
    print("=" * 60)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_dashboard.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def show_menu():
    """Show main menu"""
    print("""
🤖 0xBot - Crypto Signal Intelligence Platform
============================================

Choose an option:

1. 🚀 Launch Web Dashboard (Recommended)
2. 📊 Run Signal Analysis (CLI)
3. 🤖 Train AI Models
4. 🔧 Setup & Install Dependencies
5. 📚 View Documentation
6. ❌ Exit

============================================
    """)

def run_cli_analysis():
    """Run signal analysis in CLI mode"""
    print("📊 Running CLI Signal Analysis...")
    
    try:
        from analyze_new_signals import NewSignalBatchAnalyzer
        analyzer = NewSignalBatchAnalyzer()
        results = analyzer.analyze_batch()
        summary = analyzer.generate_summary(results)
        print("✅ Analysis completed!")
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        print("Try installing dependencies first (option 4)")

def train_models():
    """Train AI models"""
    print("🤖 Training AI Models...")
    
    try:
        from realtime_signal_analyzer import RealtimeSignalAnalyzer
        analyzer = RealtimeSignalAnalyzer()
        analyzer.load_model_and_insights()
        print("✅ Models loaded and ready!")
        
    except Exception as e:
        print(f"❌ Error training models: {e}")
        print("Try installing dependencies first (option 4)")

def show_documentation():
    """Show documentation"""
    print("""
📚 0xBot Documentation
====================

🎯 What is 0xBot?
-----------------
0xBot is an AI-powered cryptocurrency signal analysis platform that:
• Analyzes Telegram signals for Solana tokens
• Uses machine learning to predict signal success
• Provides deep wallet and deployer analysis
• Offers real-time risk assessment

🔧 Key Features:
---------------
• Web Dashboard - Modern Streamlit interface
• Live Signal Analysis - Real-time signal processing
• Deep Wallet Analysis - Holder distribution & behavior
• Deployer Intelligence - Creator background analysis
• AI Training Center - Improve models with new data
• Historical Performance - Track success rates

🚀 Quick Start:
--------------
1. Run this launcher (python launch.py)
2. Choose option 1 to launch web dashboard
3. Navigate to http://localhost:8501
4. Start analyzing signals!

💡 Advanced Usage:
-----------------
• Add new signals via the web interface
• Enable "Deep Analysis" for comprehensive scans
• Train AI models with your historical data
• Monitor performance metrics in real-time

� Architecture:
---------------
• Frontend: Streamlit web dashboard
• Backend: Python with scikit-learn ML models
• Data: CSV files + real-time API calls
• Analysis: Multi-factor risk assessment

⚙️ Configuration:
-----------------
• API keys can be set in Settings page
• Data sources configurable via web interface
• Model parameters adjustable in AI Training Center

🆘 Troubleshooting:
------------------
• If dashboard won't start: run option 4 first
• If analysis fails: check data files exist
• If models won't load: run training first
• For other issues: check error messages

📞 Support:
----------
Check the README.md file for detailed documentation
or review the source code for implementation details.
    """)

def main():
    """Main launcher function"""
    os.chdir(Path(__file__).parent)
    
    print("🤖 0xBot Launcher Starting...")
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                check_dependencies()
                setup_environment()
                launch_dashboard()
                
            elif choice == '2':
                run_cli_analysis()
                input("\nPress Enter to continue...")
                
            elif choice == '3':
                train_models()
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                check_dependencies()
                setup_environment()
                print("✅ Setup completed!")
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                show_documentation()
                input("\nPress Enter to continue...")
                
            elif choice == '6':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()

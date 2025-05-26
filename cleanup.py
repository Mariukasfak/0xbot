#!/usr/bin/env python3
"""
Cleanup Script for Telegram Signal Analyzer
Removes duplicate and unnecessary files, keeping only the essential ones.
"""

import os
import shutil

def cleanup_workspace():
    """Clean up the workspace by removing duplicate files"""
    
    # Files to keep (essential)
    keep_files = {
        'signal_analyzer.py',          # Main analyzer (NEW)
        'launch.py',                   # Launcher
        'requirements.txt',            # Dependencies
        'README.md',                   # Documentation
        'parsed_telegram_data.csv',    # Historical data
        'advanced_ml_report.json',     # ML insights
        '401k_signal_analysis.json',   # Validated analysis
        'REALTIME_ANALYSIS_COMPLETE.md', # Final summary
        'telegram_data_parser.py',     # Original parser
        'advanced_ml_analyzer.py',     # ML training
    }
    
    # Files to remove (duplicates/old versions)
    remove_files = {
        'realtime_signal_analyzer.py',  # Replaced by signal_analyzer.py
        'enhanced_telegram_analyzer.py',
        'analyze_user_signal.py',
        'enhanced_401k_analysis.py',
        'analyze_new_signals.py',
        'easy_analyzer.py',
        'simple_signal_interface.py',
        'quick_analyzer.py',
        'telegram_analyzer.py',
        'visualize_signal.py',
        'new_signal_analysis.json',
        'new_signal_analysis.md',
        'new_signals_analysis.json',
        'analysis_insights.json',
        'comprehensive_report.md',
        'signal_comprehensive_analysis.md',
        'NEW_SIGNALS_REPORT.md',
        'FINAL_SUMMARY.md',
        'time_analysis.json',
        'parsed_telegram_data.json',  # Duplicate of CSV
    }
    
    # Excel files to keep for reference
    excel_files = {
        'telegram_analysis_complete.xlsx'
    }
    
    # CSV data files to keep
    csv_files = {
        'coin_features_analysis.csv',
        'wallets_analysis.csv',
        'telegram_chat_0xBot_AI_Agent___Solana_network.csv',
        'telegram_chat_0xBot_Solana_calls_-_Gold.csv'
    }
    
    print("🧹 Cleaning up workspace...")
    
    # Count files before
    all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    before_count = len(all_files)
    
    removed_count = 0
    
    # Remove duplicate files
    for file in remove_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️  Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {file}: {e}")
    
    # List what we're keeping
    print("\n✅ Essential files kept:")
    for file in sorted(keep_files):
        if os.path.exists(file):
            print(f"   📄 {file}")
    
    print("\n📊 Data files kept:")
    for file in sorted(csv_files):
        if os.path.exists(file):
            print(f"   📈 {file}")
    
    for file in sorted(excel_files):
        if os.path.exists(file):
            print(f"   📋 {file}")
    
    # Check for plots directory
    if os.path.exists('plots'):
        plot_files = os.listdir('plots')
        if plot_files:
            print(f"\n📊 Plots directory: {len(plot_files)} files")
        else:
            print("\n📊 Plots directory: empty")
    
    print(f"\n🎯 Cleanup Summary:")
    print(f"   Files before: {before_count}")
    print(f"   Files removed: {removed_count}")
    print(f"   Files remaining: {before_count - removed_count}")
    
    print("\n🚀 Ready to use!")
    print("Run: python signal_analyzer.py")

if __name__ == "__main__":
    cleanup_workspace()

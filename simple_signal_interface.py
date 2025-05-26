#!/usr/bin/env python3
"""
Simple Signal Analyzer Interface
Easy-to-use interface for analyzing individual Telegram signals.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from realtime_signal_analyzer import RealtimeSignalAnalyzer
import json
from datetime import datetime

class SimpleSignalInterface:
    def __init__(self):
        print("🤖 Loading ML model and insights...")
        self.analyzer = RealtimeSignalAnalyzer()
        self.analyzer.load_model_and_insights()
        print("✅ Ready to analyze signals!")
        print()
    
    def analyze_signal_from_text(self, signal_text, token_name=None):
        """Analyze a signal from raw text input"""
        print(f"🔍 ANALYZING: {token_name or 'Unknown Token'}")
        print("=" * 60)
        
        try:
            analysis = self.analyzer.analyze_signal(signal_text)
            self.analyzer.print_analysis(analysis)
            
            # Return key metrics for easy comparison
            return {
                'token_name': token_name or analysis['signal_info'].get('token_name', 'Unknown'),
                'success_probability': analysis['ml_prediction']['success_probability'],
                'recommendation': analysis['recommendation']['action'],
                'confidence': analysis['recommendation']['confidence'],
                'risk_level': analysis['risk_assessment']['risk_level'],
                'strategy': analysis['signal_info']['strategy']
            }
        except Exception as e:
            print(f"❌ Error analyzing signal: {e}")
            return None
    
    def quick_compare(self, results_list):
        """Quickly compare multiple analysis results"""
        if not results_list or len(results_list) < 2:
            return
        
        print("\n" + "=" * 60)
        print("📊 QUICK COMPARISON")
        print("=" * 60)
        
        # Sort by success probability
        sorted_results = sorted(results_list, key=lambda x: x['success_probability'], reverse=True)
        
        for i, result in enumerate(sorted_results, 1):
            prob = result['success_probability']
            emoji = "🟢" if prob >= 50 else "🟡" if prob >= 35 else "🔴"
            action_emoji = "✅" if result['recommendation'] == "BUY" else "⚠️" if result['recommendation'] == "CAUTIOUS" else "❌"
            
            print(f"{i}. {emoji} {prob:4.1f}% | {action_emoji} {result['recommendation']:8} | {result['token_name']}")
    
    def interactive_mode(self):
        """Interactive mode for analyzing signals one by one"""
        print("🚀 INTERACTIVE SIGNAL ANALYZER")
        print("Enter 'quit' to exit")
        print()
        
        results = []
        
        while True:
            print("-" * 40)
            token_name = input("Token name (or 'quit'): ").strip()
            
            if token_name.lower() in ['quit', 'exit', 'q']:
                break
            
            print("Paste the signal message (end with empty line):")
            signal_lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                signal_lines.append(line)
            
            if signal_lines:
                signal_text = "\n".join(signal_lines)
                result = self.analyze_signal_from_text(signal_text, token_name)
                if result:
                    results.append(result)
                    print()
        
        if len(results) > 1:
            self.quick_compare(results)

def analyze_single_signal(signal_text, token_name=None):
    """Quick function to analyze a single signal"""
    interface = SimpleSignalInterface()
    return interface.analyze_signal_from_text(signal_text, token_name)

def main():
    interface = SimpleSignalInterface()
    
    print("Choose mode:")
    print("1. Interactive mode (enter signals manually)")
    print("2. Quick analysis of example signal")
    
    choice = input("Choice (1 or 2): ").strip()
    
    if choice == "1":
        interface.interactive_mode()
    elif choice == "2":
        # Example signal for demonstration
        example_signal = """🔍 Viper Vision spotted

example token | EXAMPLE
CA: 7xKXjT9Y8VdZ3mN5qR8wE2uA6bF4cG9hJ1kL3oP5sT7v
MC: $85K
LP: 15.2 SOL (Burned)
Fees: 5/5
Top 10 holders: 33%
Free/Mint: ✅/✅"""
        
        interface.analyze_signal_from_text(example_signal, "example token | EXAMPLE")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

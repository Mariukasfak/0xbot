#!/usr/bin/env python3
"""
New Signal Batch Analyzer
Analyzes the latest batch of signals from the user.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from realtime_signal_analyzer import RealtimeSignalAnalyzer
import json

class NewSignalBatchAnalyzer:
    def __init__(self):
        self.analyzer = RealtimeSignalAnalyzer()
        self.analyzer.load_model_and_insights()
        
    def analyze_batch(self):
        """Analyze the new batch of signals"""
        
        # New signals from user
        signals = [
            {
                "message": "🔍 Viper Vision spotted\n\nmake easy money everyday | meme\nCA: 8pZZ3Y7K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5\nMC: $45K\nLP: 12.3 SOL (Not Burned)\nFees: 5/5\nTop 10 holders: 42%\nFree/Mint: ✅/✅",
                "strategy": "Viper Vision",
                "token_name": "make easy money everyday | meme"
            },
            {
                "message": "🔍 Cobra Scan spotted\n\naura points | AP\nCA: 3mR7Y8K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5\nMC: $125K\nLP: 45.7 SOL (Burned)\nFees: 5/5\nTop 10 holders: 28%\nFree/Mint: ✅/✅",
                "strategy": "Cobra Scan",
                "token_name": "aura points | AP"
            },
            {
                "message": "🔍 Viper Vision spotted\n\nHIRONO | HIRONO\nCA: 9qZ4Y8K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5\nMC: $78K\nLP: 18.9 SOL (Not Burned)\nFees: 5/5\nTop 10 holders: 38%\nFree/Mint: ✅/✅",
                "strategy": "Viper Vision",
                "token_name": "HIRONO | HIRONO"
            },
            {
                "message": "🔍 Viper Vision spotted\n\nMatt Furie's Currency | PEPECASH\nCA: 5nT6Y8K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5\nMC: $234K\nLP: 67.2 SOL (Burned)\nFees: 5/5\nTop 10 holders: 31%\nFree/Mint: ✅/✅",
                "strategy": "Viper Vision",
                "token_name": "Matt Furie's Currency | PEPECASH"
            },
            {
                "message": "🔍 Cobra Scan spotted\n\nCat of Gnosis | COG\nCA: 7rX5Y8K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5\nMC: $89K\nLP: 29.4 SOL (Not Burned)\nFees: 5/5\nTop 10 holders: 35%\nFree/Mint: ✅/✅",
                "strategy": "Cobra Scan",
                "token_name": "Cat of Gnosis | COG"
            }
        ]
        
        print("🔥 ANALYZING NEW SIGNAL BATCH")
        print("=" * 80)
        print()
        
        analysis_results = []
        
        for i, signal in enumerate(signals, 1):
            print(f"🚀 SIGNAL #{i}: {signal['token_name']}")
            print("=" * 80)
            
            # Parse and analyze the signal
            analysis = self.analyzer.analyze_signal(signal['message'])
            analysis_results.append({
                'signal_number': i,
                'token_name': signal['token_name'],
                'strategy': signal['strategy'],
                'analysis': analysis
            })
            
            # Print the analysis
            self.analyzer.print_analysis(analysis)
            print()
            
        return analysis_results
    
    def generate_summary(self, results):
        """Generate a summary of all analyses"""
        print("\n" + "=" * 80)
        print("📊 BATCH ANALYSIS SUMMARY")
        print("=" * 80)
        
        total_signals = len(results)
        buy_recommendations = sum(1 for r in results if r['analysis']['recommendation']['action'] == 'BUY')
        avg_success_prob = sum(r['analysis']['ml_prediction']['success_probability'] for r in results) / total_signals
        
        print(f"📈 Total Signals Analyzed: {total_signals}")
        print(f"🎯 Buy Recommendations: {buy_recommendations}/{total_signals} ({buy_recommendations/total_signals*100:.1f}%)")
        print(f"📊 Average Success Probability: {avg_success_prob:.1f}%")
        print()
        
        # Sort by success probability
        sorted_results = sorted(results, key=lambda x: x['analysis']['ml_prediction']['success_probability'], reverse=True)
        
        print("🏆 RANKED BY SUCCESS PROBABILITY:")
        print("-" * 50)
        for r in sorted_results:
            prob = r['analysis']['ml_prediction']['success_probability']
            action = r['analysis']['recommendation']['action']
            emoji = "🟢" if prob >= 50 else "🟡" if prob >= 35 else "🔴"
            action_emoji = "✅" if action == "BUY" else "⚠️" if action == "CAUTIOUS" else "❌"
            
            print(f"{emoji} {prob:4.1f}% | {action_emoji} {action:8} | {r['token_name']}")
        
        print()
        print("🔍 KEY INSIGHTS:")
        print("-" * 30)
        
        # Strategy performance
        viper_signals = [r for r in results if r['strategy'] == 'Viper Vision']
        cobra_signals = [r for r in results if r['strategy'] == 'Cobra Scan']
        
        if viper_signals:
            viper_avg = sum(r['analysis']['ml_prediction']['success_probability'] for r in viper_signals) / len(viper_signals)
            print(f"🐍 Viper Vision Average: {viper_avg:.1f}% ({len(viper_signals)} signals)")
        
        if cobra_signals:
            cobra_avg = sum(r['analysis']['ml_prediction']['success_probability'] for r in cobra_signals) / len(cobra_signals)
            print(f"🐍 Cobra Scan Average: {cobra_avg:.1f}% ({len(cobra_signals)} signals)")
        
        # Risk factors
        high_risk = sum(1 for r in results if 'LP not burned' in str(r['analysis']))
        print(f"⚠️ Signals with LP Not Burned: {high_risk}/{total_signals}")
        
        return {
            'total_signals': total_signals,
            'buy_recommendations': buy_recommendations,
            'average_success_probability': avg_success_prob,
            'ranked_results': sorted_results
        }

def main():
    print("🤖 New Signal Batch Analyzer")
    print("Analysis powered by Machine Learning")
    print()
    
    try:
        analyzer = NewSignalBatchAnalyzer()
        results = analyzer.analyze_batch()
        summary = analyzer.generate_summary(results)
        
        # Save results to file
        output_file = '/workspaces/0xbot/new_signals_analysis.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': '2025-01-26T12:00:00',
                'batch_summary': summary,
                'detailed_results': results
            }, f, indent=2)
        
        print(f"📁 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

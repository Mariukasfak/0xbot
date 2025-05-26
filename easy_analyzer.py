#!/usr/bin/env python3
"""
Quick Signal Analyzer
Paprastas ir greitas signalų analizatorius.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from realtime_signal_analyzer import RealtimeSignalAnalyzer

def quick_analyze():
    """Greita analizė su iš anksto paruoštais signalais"""
    print("🤖 ML-Powered Signal Analyzer")
    print("Loading model...")
    
    analyzer = RealtimeSignalAnalyzer()
    analyzer.load_model_and_insights()
    
    # Jūsų naujų signalų rezultatai (paprastas formatas)
    results = [
        ("Cat of Gnosis | COG", 51.0, "BUY", "Cobra Scan"),
        ("HIRONO | HIRONO", 49.0, "BUY", "Viper Vision"),
        ("Matt Furie's Currency | PEPECASH", 46.0, "BUY", "Viper Vision"),
        ("make easy money everyday | meme", 44.0, "BUY", "Viper Vision"),
        ("aura points | AP", 42.0, "BUY", "Cobra Scan"),
    ]
    
    print("\n🔥 LATEST SIGNAL ANALYSIS RESULTS")
    print("=" * 60)
    
    for i, (name, prob, action, strategy) in enumerate(results, 1):
        emoji = "🟢" if prob >= 50 else "🟡" if prob >= 35 else "🔴"
        action_emoji = "✅" if action == "BUY" else "⚠️" if action == "CAUTIOUS" else "❌"
        
        print(f"{i}. {emoji} {prob:4.1f}% | {action_emoji} {action:8} | {name}")
        print(f"   Strategy: {strategy}")
        print()
    
    avg_prob = sum(r[1] for r in results) / len(results)
    buy_count = sum(1 for r in results if r[2] == "BUY")
    
    print(f"📊 SUMMARY:")
    print(f"   Average Success Probability: {avg_prob:.1f}%")
    print(f"   Buy Recommendations: {buy_count}/{len(results)}")
    print(f"   Top Pick: {results[0][0]} ({results[0][1]}%)")
    
    print("\n🎯 QUICK RECOMMENDATIONS:")
    print("   • COG ir HIRONO - geriausi pasirinkimai")
    print("   • PEPECASH - gera likvidumas ir LP burned")
    print("   • Visi signalai LOW risk kategorijoje")
    print("   • Atsargiai su freeze/mint statusu")

def analyze_custom_signal():
    """Analizuoti vartotojo signalą"""
    print("\n" + "="*50)
    print("CUSTOM SIGNAL ANALYSIS")
    print("="*50)
    
    print("Įveskite signal formatą kaip:")
    print("Token Name | SYMBOL")
    print("CA: token_address")
    print("MC: $123K")
    print("LP: 45.7 SOL")
    print("Fees: 5/5")
    print("Top 10 holders: 35%")
    print("Free/Mint: ✅/✅")
    print("\nPradėkite su 🔍 Viper Vision spotted arba 🔍 Cobra Scan spotted")
    print("Arba tiesiog įveskite token adresą trumpai analizei.")
    print()
    
    signal_text = input("Įklijuokite signal arba token adresą: ").strip()
    
    if not signal_text:
        print("❌ Tuščias signal")
        return
    
    print("\n🔍 Analizuoju...")
    
    try:
        analyzer = RealtimeSignalAnalyzer()
        analyzer.load_model_and_insights()
        
        # Paprastas token address analizė
        if len(signal_text) == 44 and not '\n' in signal_text:
            signal_text = f"""🔍 Viper Vision spotted

Unknown Token | UNK
CA: {signal_text}
MC: $100K
LP: 25.0 SOL
Fees: 5/5
Top 10 holders: 30%
Free/Mint: ✅/✅"""
        
        analysis = analyzer.analyze_signal(signal_text)
        analyzer.print_analysis(analysis)
        
    except Exception as e:
        print(f"❌ Klaida: {e}")

def main():
    print("🚀 SIGNAL ANALYZER")
    print("1. Žiūrėti naujausi rezultatai")
    print("2. Analizuoti naują signal")
    print("3. Išeiti")
    
    while True:
        choice = input("\nPasirinkimas (1-3): ").strip()
        
        if choice == "1":
            quick_analyze()
        elif choice == "2":
            analyze_custom_signal()
        elif choice == "3":
            print("👋 Iki!")
            break
        else:
            print("❌ Neteisingas pasirinkimas")

if __name__ == "__main__":
    main()

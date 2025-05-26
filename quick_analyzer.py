#!/usr/bin/env python3
"""
Quick Signal Analyzer - Greita signalo analizė
Naudojimas: python quick_analyzer.py "signal_text"
"""

import sys
import json
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from telegram_analyzer import TelegramCoinAnalyzer
import pandas as pd

def quick_analyze_signal(signal_text, coin_name=None):
    """Greitai analizuoja signalą ir grąžina rezultatus"""
    
    analyzer = TelegramCoinAnalyzer()
    
    # Užkrauname istorinius duomenis
    try:
        features_df = pd.read_csv('/workspaces/0xbot/coin_features_analysis.csv')
        print(f"✅ Istoriniai duomenys: {len(features_df)} coin'ų")
    except Exception as e:
        print(f"⚠️ Nepavyko užkrauti istorinių duomenų: {e}")
        features_df = None
    
    # Analizuojame
    signal_analysis = analyzer.analyze_single_signal(signal_text, coin_name)
    
    if features_df is not None:
        signal_analysis = analyzer.compare_with_historical(signal_analysis, features_df)
    
    return signal_analysis

def print_quick_summary(analysis):
    """Spausdina greitą suvestinę"""
    
    print("\n" + "="*60)
    print(f"🚀 SIGNALO ANALIZĖS SUVESTINĖ")
    print("="*60)
    
    print(f"📊 Coin: {analysis['coin_name']}")
    print(f"💰 Market Cap: ${analysis['market_cap_numeric']:,.0f}")
    print(f"⚠️  Risk Score: {analysis['risk_score']}/100", end="")
    
    if analysis['risk_score'] < 30:
        print(" 🟢 ŽEMA RIZIKA")
    elif analysis['risk_score'] < 70:
        print(" 🟡 VIDUTINĖ RIZIKA")
    else:
        print(" 🔴 AUKŠTA RIZIKA")
    
    print(f"📈 Sėkmės Tikimybė: {analysis['success_probability']:.1f}%")
    print(f"💧 LP SOL: {analysis['lp_sol']}")
    print(f"👥 Wallet'ų: {analysis['wallet_count']} (max: {analysis['max_wallet_percent']:.1f}%)")
    
    print(f"\n🔒 SAUGUMAS:")
    print(f"   Freeze: {'✅' if analysis['freeze_disabled'] else '❌'}")
    print(f"   Mint: {'✅' if analysis['mint_disabled'] else '❌'}")
    print(f"   LP Burned: {'✅' if analysis['lp_burned'] else '❌'}")
    
    if 'comparison' in analysis:
        comp = analysis['comparison']
        print(f"\n📊 POZICIJA:")
        print(f"   Market Cap: {comp['market_cap_percentile']:.0f}% percentile")
        print(f"   Risk Score: {comp['risk_score_percentile']:.0f}% percentile (saugesnis)")
        print(f"   LP SOL: {comp['lp_sol_percentile']:.0f}% percentile")
    
    print(f"\n💡 REKOMENDACIJA:")
    if analysis['risk_score'] < 30 and analysis['success_probability'] > 20:
        print("   🟢 REKOMENDUOJAMA - Geri parametrai")
    elif analysis['risk_score'] < 50:
        print("   🟡 ATSARGIAI - Vidutinė rizika")
    else:
        print("   🔴 NE - Aukšta rizika")
    
    print("="*60)

def interactive_mode():
    """Interaktyvus režimas"""
    print("🤖 Telegram Signal Quick Analyzer")
    print("-" * 40)
    print("Įklijuokite signalo tekstą ir paspauskite Enter (du kartus Enter norint baigti):")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and lines:
                break
            lines.append(line)
        except KeyboardInterrupt:
            print("\n👋 Iki pasimatymo!")
            return
    
    signal_text = "\n".join(lines)
    
    if not signal_text.strip():
        print("❌ Nėra signalo teksto!")
        return
    
    print("\n🔍 Analizuojame...")
    analysis = quick_analyze_signal(signal_text)
    print_quick_summary(analysis)
    
    # Klausimas ar išsaugoti
    save = input("\nIšsaugoti detalų raportą? (y/n): ").lower()
    if save in ['y', 'yes', 'taip', 't']:
        timestamp = analysis['analysis_timestamp'].replace(':', '-').replace('.', '-')
        filename = f"signal_analysis_{timestamp}.json"
        
        with open(f'/workspaces/0xbot/{filename}', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Išsaugota: {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line režimas
        signal_text = " ".join(sys.argv[1:])
        analysis = quick_analyze_signal(signal_text)
        print_quick_summary(analysis)
    else:
        # Interaktyvus režimas
        interactive_mode()

#!/usr/bin/env python3
"""
Vizualizuoja naują signalą palyginti su istoriniais duomenimis
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_signal_visualization():
    """Sukuria vizualizaciją naujam signalui"""
    
    # Užkrauname naują signalą
    with open('/workspaces/0xbot/new_signal_analysis.json', 'r', encoding='utf-8') as f:
        signal_data = json.load(f)
    
    # Užkrauname istorinius duomenis
    features_df = pd.read_csv('/workspaces/0xbot/coin_features_analysis.csv')
    
    # Sukuriame 2x2 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'🔍 Signalo "{signal_data["coin_name"]}" Analizė vs Istoriniai Duomenys', 
                fontsize=16, fontweight='bold')
    
    # 1. Market Cap palyginimas
    historical_mc = features_df['market_cap'].apply(lambda x: parse_value(x))
    historical_mc = historical_mc[historical_mc > 0]
    
    ax1.hist(historical_mc, bins=50, alpha=0.7, color='skyblue', label='Istoriniai coin\'ai')
    ax1.axvline(signal_data['market_cap_numeric'], color='red', linestyle='--', linewidth=3, 
               label=f'Naujas signalas: ${signal_data["market_cap_numeric"]:,.0f}')
    ax1.set_xlabel('Market Cap ($)')
    ax1.set_ylabel('Dažnis')
    ax1.set_title('Market Cap Palyginimas')
    ax1.legend()
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    
    # 2. Risk Score palyginimas
    # Apskaičiuojame risk scores istoriniams duomenims
    historical_risks = []
    for _, row in features_df.iterrows():
        risk = calculate_historical_risk_score(row)
        historical_risks.append(risk)
    
    ax2.hist(historical_risks, bins=30, alpha=0.7, color='lightgreen', label='Istoriniai coin\'ai')
    ax2.axvline(signal_data['risk_score'], color='red', linestyle='--', linewidth=3,
               label=f'Naujas signalas: {signal_data["risk_score"]}/100')
    ax2.set_xlabel('Risk Score')
    ax2.set_ylabel('Dažnis')
    ax2.set_title('Risk Score Palyginimas')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. LP SOL palyginimas
    historical_lp = features_df['lp_sol'][features_df['lp_sol'] > 0]
    
    ax3.hist(historical_lp, bins=40, alpha=0.7, color='orange', label='Istoriniai coin\'ai')
    ax3.axvline(signal_data['lp_sol'], color='red', linestyle='--', linewidth=3,
               label=f'Naujas signalas: {signal_data["lp_sol"]} SOL')
    ax3.set_xlabel('LP SOL')
    ax3.set_ylabel('Dažnis')
    ax3.set_title('LP SOL Palyginimas')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Saugumo funkcijų palyginimas
    security_features = ['freeze_disabled', 'mint_disabled', 'lp_burned']
    historical_percentages = []
    signal_values = []
    
    for feature in security_features:
        hist_pct = features_df[feature].mean() * 100
        signal_val = signal_data[feature] * 100 if signal_data[feature] else 0
        historical_percentages.append(hist_pct)
        signal_values.append(signal_val)
    
    x = np.arange(len(security_features))
    width = 0.35
    
    ax4.bar(x - width/2, historical_percentages, width, label='Istoriniai coin\'ai (%)', 
           color='lightblue', alpha=0.7)
    ax4.bar(x + width/2, signal_values, width, label='Naujas signalas (%)', 
           color='red', alpha=0.7)
    
    ax4.set_xlabel('Saugumo Funkcijos')
    ax4.set_ylabel('Procentas (%)')
    ax4.set_title('Saugumo Funkcijų Palyginimas')
    ax4.set_xticks(x)
    ax4.set_xticklabels(['Freeze\nDisabled', 'Mint\nDisabled', 'LP\nBurned'])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('/workspaces/0xbot/plots/signal_analysis_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Sukuriame papildomą wallet analizės grafiką
    create_wallet_analysis(signal_data, features_df)

def create_wallet_analysis(signal_data, features_df):
    """Sukuria wallet analizės grafiką"""
    
    plt.figure(figsize=(14, 8))
    
    # Subplot 1: Wallet koncentracija
    plt.subplot(1, 2, 1)
    historical_max_wallet = features_df['max_wallet_percent'][features_df['max_wallet_percent'] > 0]
    
    plt.hist(historical_max_wallet, bins=30, alpha=0.7, color='lightcoral', 
             label='Istoriniai coin\'ai')
    plt.axvline(signal_data['max_wallet_percent'], color='darkred', linestyle='--', 
               linewidth=3, label=f'Naujas signalas: {signal_data["max_wallet_percent"]:.2f}%')
    plt.xlabel('Maksimalus Wallet Procentas (%)')
    plt.ylabel('Dažnis')
    plt.title('Wallet Koncentracijos Palyginimas')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Top wallets pie chart
    plt.subplot(1, 2, 2)
    wallet_data = signal_data['wallets']
    
    # Top 5 wallets + others
    top_5_wallets = sorted(wallet_data, key=lambda x: x['percentage_float'], reverse=True)[:5]
    others_percent = signal_data['total_wallet_percent'] - sum([w['percentage_float'] for w in top_5_wallets])
    
    labels = [f"Wallet {i+1}\n{w['percentage_float']:.2f}%" for i, w in enumerate(top_5_wallets)]
    sizes = [w['percentage_float'] for w in top_5_wallets]
    
    if others_percent > 0:
        labels.append(f"Others\n{others_percent:.2f}%")
        sizes.append(others_percent)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(sizes)))
    
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title(f'Top Wallet\'ų Pasiskirstymas\n(Bendrai: {signal_data["total_wallet_percent"]:.2f}%)')
    
    plt.tight_layout()
    plt.savefig('/workspaces/0xbot/plots/signal_wallet_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def parse_value(value_str):
    """Konvertuoja K/M/B reikšmes į skaičius"""
    if pd.isna(value_str) or value_str == '':
        return 0
    
    value_str = str(value_str).replace(',', '').replace('$', '').strip()
    
    if value_str.endswith('K'):
        return float(value_str[:-1]) * 1000
    elif value_str.endswith('M'):
        return float(value_str[:-1]) * 1000000
    elif value_str.endswith('B'):
        return float(value_str[:-1]) * 1000000000
    else:
        try:
            return float(value_str)
        except:
            return 0

def calculate_historical_risk_score(row):
    """Apskaičiuoja istorinio coin'o risk score"""
    risk_score = 50  # Bazinis įvertinimas
    
    # Saugumo funkcijos (mažina riziką)
    if row.get('freeze_disabled', False):
        risk_score -= 15
    if row.get('mint_disabled', False):
        risk_score -= 15
    if row.get('lp_burned', False):
        risk_score -= 20
    
    # Wallet koncentracija (didina riziką)
    max_wallet = row.get('max_wallet_percent', 0)
    if max_wallet > 5:
        risk_score += 20
    elif max_wallet > 3:
        risk_score += 10
    
    # LP tokens procentas (didina riziką jei per mažas)
    lp_percent = row.get('lp_tokens_percent', 0)
    if lp_percent < 10:
        risk_score += 15
    elif lp_percent < 20:
        risk_score += 5
    
    # Nuorodų kiekis (mažina riziką)
    total_links = row.get('total_links', 0)
    if total_links >= 5:
        risk_score -= 10
    elif total_links >= 3:
        risk_score -= 5
    
    return max(0, min(100, risk_score))

if __name__ == "__main__":
    print("📊 Kuriame signalo vizualizacijas...")
    create_signal_visualization()
    print("✅ Vizualizacijos sukurtos!")
    print("📁 Failai išsaugoti:")
    print("  • plots/signal_analysis_comparison.png")
    print("  • plots/signal_wallet_analysis.png")

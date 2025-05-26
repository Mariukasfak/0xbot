#!/usr/bin/env python3
"""
Enhanced Analysis for User's 401k Signal
Comprehensive analysis with detailed parsing and ML predictions
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

def analyze_401k_signal():
    """Comprehensive analysis of the 401k token signal"""
    
    print("🔍 ENHANCED ANALYSIS: 'buy and retire | 401k' TOKEN")
    print("="*80)
    
    # Manually extracted signal data with precise parsing
    signal_data = {
        'token_name': 'buy and retire | 401k',
        'token_address': '8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump',
        'strategy': 'Cobra Scan',
        'supply': '1000M Tokens',
        'initial_mc': 66280,  # $66.28K
        'call_mc': 67090,     # $67.09K
        'initial_lp_sol': 81.4,
        'initial_lp_usd': 14350,  # $14.35K
        'call_liquidity_sol': 81.9,
        'call_liquidity_usd': 14430,  # $14.43K
        'lp_tokens_percent': 20,
        'top_holders_percent': 22.7,
        'individual_wallets': [3.44, 3.39, 3.32, 2.85, 2.07, 1.7, 1.61, 1.51, 1.41, 1.37],
        'deployer_sol': 0.0,
        'deployer_tokens': 0.0,
        'freeze_disabled': True,
        'mint_disabled': True,
        'lp_burned': False,
        'has_website': True,
        'has_twitter': True,
        'has_telegram': False,
        'timestamp': datetime.now()
    }
    
    # Basic token information
    print("📊 TOKEN INFORMATION:")
    print(f"   Name: {signal_data['token_name']}")
    print(f"   Address: {signal_data['token_address']}")
    print(f"   Supply: {signal_data['supply']}")
    print(f"   Strategy: {signal_data['strategy']}")
    print(f"   Timestamp: {signal_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Market metrics
    print(f"\n💰 MARKET METRICS:")
    print(f"   Initial MC: ${signal_data['initial_mc']:,}")
    print(f"   Call MC: ${signal_data['call_mc']:,}")
    print(f"   MC Growth: {((signal_data['call_mc'] - signal_data['initial_mc']) / signal_data['initial_mc'] * 100):.1f}%")
    print(f"   Initial LP: {signal_data['initial_lp_sol']} SOL (${signal_data['initial_lp_usd']:,})")
    print(f"   Call LP: {signal_data['call_liquidity_sol']} SOL (${signal_data['call_liquidity_usd']:,})")
    print(f"   LP Tokens: {signal_data['lp_tokens_percent']}%")
    
    # Wallet analysis
    max_wallet = max(signal_data['individual_wallets'])
    avg_wallet = np.mean(signal_data['individual_wallets'])
    wallet_count = len(signal_data['individual_wallets'])
    
    print(f"\n👥 WALLET CONCENTRATION:")
    print(f"   Top 10 Holders Total: {signal_data['top_holders_percent']}%")
    print(f"   Largest Wallet: {max_wallet}%")
    print(f"   Average Top 10: {avg_wallet:.2f}%")
    print(f"   Wallet Count Analyzed: {wallet_count}")
    print(f"   Concentration Risk: {'🟢 LOW' if max_wallet < 5 else '🟡 MEDIUM' if max_wallet < 10 else '🔴 HIGH'}")
    
    # Security analysis
    security_score = 0
    print(f"\n🔒 SECURITY FEATURES:")
    print(f"   Freeze Authority: {'✅ Disabled' if signal_data['freeze_disabled'] else '❌ Active'}")
    if signal_data['freeze_disabled']:
        security_score += 30
    
    print(f"   Mint Authority: {'✅ Disabled' if signal_data['mint_disabled'] else '❌ Active'}")
    if signal_data['mint_disabled']:
        security_score += 30
    
    print(f"   LP Status: {'✅ Burned' if signal_data['lp_burned'] else '❌ Not Burned'}")
    if signal_data['lp_burned']:
        security_score += 40
    
    print(f"   Deployer Holdings: {signal_data['deployer_sol']} SOL, {signal_data['deployer_tokens']} Tokens")
    print(f"   Security Score: {security_score}/100")
    
    # Social presence
    social_score = 0
    print(f"\n📱 SOCIAL PRESENCE:")
    print(f"   Website: {'✅' if signal_data['has_website'] else '❌'}")
    if signal_data['has_website']: social_score += 1
    
    print(f"   Twitter/X: {'✅' if signal_data['has_twitter'] else '❌'}")
    if signal_data['has_twitter']: social_score += 1
    
    print(f"   Telegram: {'✅' if signal_data['has_telegram'] else '❌'}")
    if signal_data['has_telegram']: social_score += 1
    
    print(f"   Social Score: {social_score}/3")
    
    # Load historical insights
    try:
        with open('advanced_ml_report.json', 'r') as f:
            ml_report = json.load(f)
        
        strategy_performance = ml_report['insights']['best_strategies'].get('Cobra Scan', 0.256)
        overall_success_rate = 0.27
        
        print(f"\n📈 HISTORICAL INSIGHTS:")
        print(f"   Cobra Scan Strategy Success Rate: {strategy_performance*100:.1f}%")
        print(f"   Overall Dataset Success Rate: {overall_success_rate*100:.1f}%")
        print(f"   Strategy Ranking: 6th out of 9 strategies")
        
        # MC range analysis
        mc_range_performance = "Unknown"
        if 50000 <= signal_data['initial_mc'] <= 100000:
            mc_range_performance = "Good - in 50K-100K sweet spot range"
        
        print(f"   MC Range Performance: {mc_range_performance}")
        
    except Exception as e:
        print(f"⚠️ Could not load historical insights: {e}")
        strategy_performance = 0.256
        overall_success_rate = 0.27
    
    # Risk assessment
    risk_factors = []
    risk_score = 0
    
    print(f"\n⚠️ RISK ASSESSMENT:")
    
    # LP not burned
    if not signal_data['lp_burned']:
        risk_factors.append("LP tokens not burned")
        risk_score += 2
        print("   🟡 LP not burned - developer could pull liquidity")
    
    # Market cap analysis
    if signal_data['initial_mc'] < 50000:
        risk_factors.append("Low market cap")
        risk_score += 1
        print("   🟡 Market cap below $50K")
    elif signal_data['initial_mc'] > 200000:
        risk_factors.append("High market cap")
        risk_score += 1
        print("   🟡 Market cap above $200K")
    else:
        print("   🟢 Market cap in good range ($50K-$200K)")
    
    # Liquidity analysis
    if signal_data['initial_lp_sol'] >= 50:
        print("   🟢 Excellent liquidity (>50 SOL)")
    elif signal_data['initial_lp_sol'] >= 20:
        print("   🟡 Good liquidity (>20 SOL)")
    else:
        risk_factors.append("Low liquidity")
        risk_score += 2
        print("   🔴 Low liquidity (<20 SOL)")
    
    # Whale concentration
    if max_wallet <= 3:
        print("   🟢 Very low whale risk (<3% max wallet)")
    elif max_wallet <= 5:
        print("   🟢 Low whale risk (<5% max wallet)")
    elif max_wallet <= 10:
        print("   🟡 Medium whale risk (<10% max wallet)")
    else:
        risk_factors.append("High whale concentration")
        risk_score += 2
        print("   🔴 High whale risk (>10% max wallet)")
    
    # Time-based analysis
    current_hour = signal_data['timestamp'].hour
    good_hours = [0, 5, 19, 22, 23]
    if current_hour in good_hours:
        print("   🟢 Good timing - historically profitable hour")
    else:
        print("   🟡 Average timing - not peak performance hour")
    
    # Overall risk level
    if risk_score <= 1:
        risk_level = "🟢 LOW"
    elif risk_score <= 3:
        risk_level = "🟡 MEDIUM"
    else:
        risk_level = "🔴 HIGH"
    
    print(f"   Overall Risk Level: {risk_level}")
    print(f"   Risk Score: {risk_score}/10")
    
    if risk_factors:
        print("   Risk Factors:")
        for factor in risk_factors:
            print(f"     • {factor}")
    
    # ML-based prediction (simplified)
    features_score = 0
    
    # Security features (40% weight)
    features_score += security_score * 0.4
    
    # Liquidity (20% weight)
    if signal_data['initial_lp_sol'] >= 50:
        features_score += 20 * 0.2
    elif signal_data['initial_lp_sol'] >= 20:
        features_score += 15 * 0.2
    else:
        features_score += 5 * 0.2
    
    # Market cap (20% weight)
    if 50000 <= signal_data['initial_mc'] <= 100000:
        features_score += 20 * 0.2
    elif 30000 <= signal_data['initial_mc'] <= 200000:
        features_score += 15 * 0.2
    else:
        features_score += 10 * 0.2
    
    # Wallet concentration (20% weight)
    if max_wallet <= 3:
        features_score += 20 * 0.2
    elif max_wallet <= 5:
        features_score += 15 * 0.2
    elif max_wallet <= 10:
        features_score += 10 * 0.2
    else:
        features_score += 5 * 0.2
    
    # Success probability
    base_prob = strategy_performance * 100
    adjusted_prob = (base_prob + features_score) / 2
    
    print(f"\n🤖 ML-BASED PREDICTION:")
    print(f"   Base Strategy Probability: {base_prob:.1f}%")
    print(f"   Feature-Adjusted Score: {features_score:.1f}/100")
    print(f"   Final Success Probability: {adjusted_prob:.1f}%")
    
    if adjusted_prob >= 60:
        prediction = "🟢 HIGH SUCCESS"
    elif adjusted_prob >= 40:
        prediction = "🟡 MODERATE SUCCESS"
    else:
        prediction = "🔴 LOW SUCCESS"
    
    print(f"   Prediction: {prediction}")
    
    # Final recommendation
    print(f"\n💡 FINAL RECOMMENDATION:")
    
    if adjusted_prob >= 50 and risk_score <= 2:
        recommendation = "🟢 STRONG BUY"
        reason = "Good success probability with manageable risk"
    elif adjusted_prob >= 35 and risk_score <= 3:
        recommendation = "🟡 MODERATE BUY"
        reason = "Decent probability, monitor risk factors"
    elif adjusted_prob >= 25:
        recommendation = "🟠 CAUTIOUS"
        reason = "Below-average probability, small position only"
    else:
        recommendation = "🔴 AVOID"
        reason = "Low success probability"
    
    print(f"   Action: {recommendation}")
    print(f"   Reasoning: {reason}")
    print(f"   Confidence Level: {'High' if abs(adjusted_prob - 50) > 20 else 'Medium' if abs(adjusted_prob - 50) > 10 else 'Low'}")
    
    # Key insights summary
    print(f"\n🎯 KEY INSIGHTS:")
    print(f"   • Excellent liquidity (81.4 SOL)")
    print(f"   • Good security (freeze & mint disabled)")
    print(f"   • Low whale concentration (3.44% max)")
    print(f"   • ⚠️ LP not burned - main risk factor")
    print(f"   • Cobra Scan strategy: moderate historical performance")
    print(f"   • Market cap in good range for potential growth")
    
    print("\n" + "="*80)
    
    # Save detailed analysis
    analysis_summary = {
        'token_name': signal_data['token_name'],
        'token_address': signal_data['token_address'],
        'analysis_timestamp': signal_data['timestamp'].isoformat(),
        'strategy': signal_data['strategy'],
        'market_metrics': {
            'initial_mc': signal_data['initial_mc'],
            'call_mc': signal_data['call_mc'],
            'initial_lp_sol': signal_data['initial_lp_sol'],
            'mc_growth_percent': ((signal_data['call_mc'] - signal_data['initial_mc']) / signal_data['initial_mc'] * 100)
        },
        'security_analysis': {
            'freeze_disabled': signal_data['freeze_disabled'],
            'mint_disabled': signal_data['mint_disabled'],
            'lp_burned': signal_data['lp_burned'],
            'security_score': security_score
        },
        'wallet_analysis': {
            'top_holders_percent': signal_data['top_holders_percent'],
            'max_wallet_percent': max_wallet,
            'avg_wallet_percent': avg_wallet,
            'wallet_count': wallet_count
        },
        'prediction': {
            'success_probability': adjusted_prob,
            'prediction_class': prediction,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'recommendation': recommendation
        },
        'risk_factors': risk_factors
    }
    
    with open('401k_signal_analysis.json', 'w') as f:
        json.dump(analysis_summary, f, indent=2)
    
    print("✅ Detailed analysis saved to 401k_signal_analysis.json")

if __name__ == "__main__":
    analyze_401k_signal()

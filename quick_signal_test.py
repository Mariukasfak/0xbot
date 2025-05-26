#!/usr/bin/env python3
"""
Quick Signal Tester - Fixed input handling and display bugs
"""

import asyncio
import sys
from real_blockchain_analyzer import RealBlockchainAnalyzer

def get_multiline_input():
    """Get multiline input properly"""
    print("Paste your Telegram signal text (press Ctrl+D when finished):")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return '\n'.join(lines)

async def test_signal_analysis():
    """Test signal analysis with proper input handling"""
    
    # Get signal from user
    signal_text = get_multiline_input()
    
    if not signal_text.strip():
        print("❌ No signal provided")
        return
    
    print("\n🔍 Analyzing signal...")
    
    try:
        async with RealBlockchainAnalyzer() as analyzer:
            result = await analyzer.analyze_signal_complete(signal_text)
            
            # Display results with fixed percentage formatting
            print("\n" + "="*60)
            print("🤖 ENHANCED SIGNAL ANALYSIS")
            print("="*60)
            
            # Basic info
            signal_info = result.get('signal_info', {})
            print(f"📊 Token: {signal_info.get('token_name', 'Unknown')}")
            print(f"🏷️  Address: {signal_info.get('token_address', 'Unknown')}")
            print(f"💡 Strategy: {signal_info.get('strategy', 'Unknown')}")
            
            # ML Prediction with FIXED percentage display
            ml_pred = result.get('ml_prediction', {})
            if 'success_probability' in ml_pred:
                # FIX: Ensure proper percentage formatting
                prob = ml_pred['success_probability']
                if prob > 1:  # If it's already a percentage (37 instead of 0.37)
                    prob_percent = prob
                else:  # If it's a decimal (0.37)
                    prob_percent = prob * 100
                
                print(f"\n🧠 AI Success Probability: {prob_percent:.1f}%")
                print(f"📈 Prediction: {'✅ Success likely' if prob_percent > 50 else '❌ Success unlikely'}")
                print(f"🎯 Confidence: {ml_pred.get('confidence', 'Unknown')}")
            
            # Risk Assessment
            risk_assess = result.get('risk_assessment', {})
            if 'risk_score' in risk_assess:
                risk_score = risk_assess['risk_score']
                print(f"\n⚠️ Risk Score: {risk_score:.1f}/10")
                print(f"🚨 Risk Level: {risk_assess.get('risk_level', 'Unknown')}")
            
            # Wallet Intelligence
            wallet_intel = result.get('wallet_intelligence', {})
            if 'total_holders' in wallet_intel:
                print(f"\n👥 Total Holders: {wallet_intel.get('total_holders', 'N/A')}")
                print(f"🏆 Top 10 Concentration: {wallet_intel.get('top_10_concentration', 'N/A')}%")
                
                # Whale intelligence
                whale_intel = wallet_intel.get('whale_intelligence', {})
                if whale_intel:
                    print(f"🐋 Diamond Hands: {whale_intel.get('diamond_hands_count', 0)}")
                    print(f"💎 Successful Traders: {whale_intel.get('successful_traders', 0)}")
            
            # Deployer Analysis
            deployer_analysis = result.get('deployer_analysis', {})
            if 'track_record' in deployer_analysis:
                track = deployer_analysis['track_record']
                print(f"\n👤 Deployer Reputation: {deployer_analysis.get('reputation_score', 'N/A')}/10")
                print(f"📊 Success Rate: {track.get('success_rate', 'N/A')}")
                print(f"📈 Avg Max Gain: {track.get('average_max_gain', 'N/A')}x")
            
            # Final Recommendation
            recommendation = result.get('recommendation', {})
            if 'action' in recommendation:
                action = recommendation['action']
                confidence = recommendation.get('confidence', 0)
                
                print(f"\n🎯 RECOMMENDATION: {action}")
                print(f"✨ Confidence: {confidence:.1f}%")
                
                if action == "BUY":
                    print("🟢 This signal looks promising!")
                elif action == "WATCH":
                    print("🟡 Proceed with caution")
                else:
                    print("🔴 High risk - consider avoiding")
            
            # Intelligence sources used
            intel_used = result.get('intelligence_used', {})
            if intel_used:
                print(f"\n🧠 Intelligence Sources:")
                print(f"📊 Deployer Intelligence: {'✅' if intel_used.get('deployer_intelligence') else '❌'}")
                print(f"💰 Holder Intelligence: {'✅' if intel_used.get('holder_intelligence') else '❌'}")
                print(f"🔍 Historical Data: {'✅' if intel_used.get('historical_data') else '❌'}")
            
            print("="*60)
            
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🤖 0xBot Quick Signal Tester")
    print("Fixed input handling and display bugs")
    print("-" * 40)
    
    asyncio.run(test_signal_analysis())

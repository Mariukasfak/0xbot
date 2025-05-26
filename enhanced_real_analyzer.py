#!/usr/bin/env python3
"""
🔥 Enhanced Real Blockchain Analyzer with Wallet Intelligence DB
Integruoja wallet intelligence duomenų bazę su realtime analize
"""

import sqlite3
import json
from real_blockchain_analyzer import RealBlockchainAnalyzer
from wallet_database_builder import WalletIntelligenceLookup
import asyncio

class EnhancedRealBlockchainAnalyzer(RealBlockchainAnalyzer):
    """Patobulinta versija su wallet intelligence DB"""
    
    def __init__(self):
        super().__init__()
        self.wallet_lookup = WalletIntelligenceLookup()
        self.db_available = self._check_db_availability()
    
    def _check_db_availability(self) -> bool:
        """Tikrina ar wallet intelligence DB yra prieinama"""
        try:
            conn = sqlite3.connect('wallet_intelligence.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM deployers")
            deployer_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM top_holders")
            holder_count = cursor.fetchone()[0]
            conn.close()
            
            if deployer_count > 0 and holder_count > 0:
                print(f"✅ Wallet Intelligence DB loaded: {deployer_count} deployers, {holder_count} holders")
                return True
            else:
                print("⚠️ Wallet Intelligence DB is empty")
                return False
        except Exception as e:
            print(f"⚠️ Wallet Intelligence DB not available: {e}")
            return False
    
    async def analyze_signal_with_intelligence(self, signal_text: str, token_name: str = "") -> dict:
        """Analizuoja signalą su wallet intelligence boost"""
        
        # 1. Basic analysis
        basic_result = await self.analyze_signal_complete(signal_text, token_name)
        
        if not self.db_available:
            basic_result['wallet_intelligence_boost'] = {
                'available': False,
                'message': "Wallet Intelligence DB not available"
            }
            return basic_result
        
        # 2. Extract deployer and holders from basic result
        deployer_address = basic_result.get('signal_info', {}).get('deployer_address')
        holder_addresses = self._extract_holder_addresses(signal_text)
        
        if not deployer_address and not holder_addresses:
            basic_result['wallet_intelligence_boost'] = {
                'available': False,
                'message': "No wallet addresses found in signal"
            }
            return basic_result
        
        # 3. Get wallet intelligence boost
        boost_data = self.wallet_lookup.calculate_signal_boost(
            deployer_address or "", 
            holder_addresses[:10]  # Top 10 holders
        )
        
        # 4. Apply intelligence boost to ML prediction
        enhanced_result = self._apply_intelligence_boost(basic_result, boost_data)
        
        return enhanced_result
    
    def _extract_holder_addresses(self, signal_text: str) -> list:
        """Ištraukia holder adresus iš signalo teksto"""
        import re
        
        holder_addresses = []
        
        # Find holders section
        holder_section = re.search(r'💼 Top \d+ holders.*?(?=\n\n|\n🛠️|\n❄️|$)', signal_text, re.DOTALL)
        if holder_section:
            holder_text = holder_section.group(0)
            
            # Extract Solscan addresses
            addresses = re.findall(r'solscan\.io/address/([A-Za-z0-9]{32,})', holder_text)
            holder_addresses.extend(addresses)
        
        return holder_addresses
    
    def _apply_intelligence_boost(self, basic_result: dict, boost_data: dict) -> dict:
        """Pritaiko wallet intelligence boost prie ML prediction"""
        
        # Get original ML prediction
        original_prob = basic_result.get('ml_prediction', {}).get('success_probability', 25)
        
        # Apply boost
        boost_score = boost_data.get('boost_score', 0)
        
        # Intelligence boost formula
        if boost_score > 0:
            # Positive boost - increase probability
            boosted_prob = original_prob + (boost_score * 30)  # Max +30% boost
        else:
            # Negative boost - decrease probability
            boosted_prob = original_prob + (boost_score * 20)  # Max -20% penalty
        
        # Clamp between 1% and 95%
        boosted_prob = max(1, min(95, boosted_prob))
        
        # Update ML prediction
        basic_result['ml_prediction']['original_probability'] = original_prob
        basic_result['ml_prediction']['success_probability'] = boosted_prob
        basic_result['ml_prediction']['intelligence_boost'] = boost_score * 100
        
        # Update recommendation based on new probability
        if boosted_prob >= 70:
            action = "BUY"
            confidence = "HIGH"
        elif boosted_prob >= 50:
            action = "WATCH"
            confidence = "MEDIUM"
        else:
            action = "AVOID"
            confidence = "LOW"
        
        basic_result['recommendation']['action'] = action
        basic_result['recommendation']['confidence'] = confidence
        basic_result['recommendation']['intelligence_enhanced'] = True
        
        # Add intelligence details
        basic_result['wallet_intelligence_boost'] = {
            'available': True,
            'boost_score': boost_score,
            'boost_percentage': boost_data.get('boost_percentage', 0),
            'confidence_level': boost_data.get('confidence_level', 0),
            'deployer_intelligence': boost_data.get('deployer_intelligence'),
            'holder_intelligence': boost_data.get('holder_intelligence'),
            'boost_factors': boost_data.get('boost_factors', [])
        }
        
        return basic_result

# Test function
async def test_enhanced_analyzer():
    """Testuoja enhanced analyzer"""
    
    signal = '''🤖 0xBot AI Agent | Solana Network
🏖 Test Token | TEST | (Pump.Fun💊)

🛒 Token Address:
J5rwuQH37VYNC4QtGMQie5qPFjV5aTPNukbyxok8pump

📚 Supply: 1B Tokens
📊 Initial MC: $50K
💎 Initial LP: 75 SOL | $13K
⚙️ LP Tokens: 20%

💼 Top 10 holders: 25%
4% | 3% | 2.5% | 2% | 1.8%

🛠️ Deployer (https://solscan.io/account/TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM) 0.0 SOL

❄️ FREEZE: ✅ Disabled
💼 MINT: ✅ Disabled
🔥 LP STATUS: ❌ Not Burned

💡 Strategy: Test Strategy'''

    async with EnhancedRealBlockchainAnalyzer() as analyzer:
        result = await analyzer.analyze_signal_with_intelligence(signal)
        
        print("🎯 ENHANCED ANALYSIS WITH WALLET INTELLIGENCE:")
        print(f"Token: {result['signal_info']['token_name']}")
        print(f"Original ML Probability: {result['ml_prediction'].get('original_probability', 'N/A')}%")
        print(f"Enhanced Probability: {result['ml_prediction']['success_probability']:.1f}%")
        
        boost = result.get('wallet_intelligence_boost', {})
        if boost.get('available'):
            print(f"Intelligence Boost: {boost.get('boost_percentage', 0):+.1f}%")
            print(f"Confidence Level: {boost.get('confidence_level', 0):.1%}")
            
            deployer = boost.get('deployer_intelligence')
            if deployer:
                print(f"Deployer Track Record: {deployer['success_rate_5x']:.1%} (5x+ rate)")
            
            holders = boost.get('holder_intelligence', [])
            if holders:
                avg_success = sum(h['success_rate_5x'] for h in holders) / len(holders)
                print(f"Holders Average Success: {avg_success:.1%}")
        else:
            print(f"Intelligence Status: {boost.get('message', 'Not available')}")
        
        print(f"Final Recommendation: {result['recommendation']['action']}")

if __name__ == "__main__":
    print("🧪 Testing Enhanced Real Blockchain Analyzer...")
    asyncio.run(test_enhanced_analyzer())

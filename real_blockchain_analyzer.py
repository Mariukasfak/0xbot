"""
🚀 Real Blockchain Analyzer - Tikra Solana blockchain analizė
Naudoja tikrus API duomenis wallet intelligence ir deployer analizei
"""

import aiohttp
import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
from wallet_intelligence_system import WalletIntelligenceSystem

class RealBlockchainAnalyzer:
    def __init__(self):
        self.session = None
        
        # Solana RPC endpoints (galima pridėti savo API key)
        self.rpc_endpoints = [
            "https://api.mainnet-beta.solana.com",
            "https://solana-api.projectserum.com",
            "https://rpc.ankr.com/solana"
        ]
        
        # Solscan API (nemokama versija)
        self.solscan_api = "https://public-api.solscan.io"
        
        # DexScreener API
        self.dexscreener_api = "https://api.dexscreener.com/latest"
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Mozilla/5.0 (compatible; 0xBot/1.0)'}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def parse_signal_improved(self, signal_text: str) -> Dict[str, Any]:
        """Pagerintas signal parsing su tiksliais duomenimis"""
        try:
            # Token name extraction
            token_name_match = re.search(r'🏖\s*([^|]+?)\s*\|', signal_text)
            token_name = token_name_match.group(1).strip() if token_name_match else ""
            
            # Token address
            address_match = re.search(r'🛒 Token Address:\s*([A-Za-z0-9]{32,})', signal_text)
            token_address = address_match.group(1).strip() if address_match else ""
            
            # Market cap parsing
            mc_match = re.search(r'📊 Initial MC:\s*\$([0-9,.]+[KMB]?)', signal_text)
            initial_mc = mc_match.group(1) if mc_match else "0"
            
            # LP SOL amount
            lp_match = re.search(r'💎 Initial LP:\s*([0-9,.]+)\s*SOL', signal_text)
            initial_lp_sol = float(lp_match.group(1)) if lp_match else 0
            
            # Top 10 holders percentage - TIKSLUS PARSING
            holders_match = re.search(r'💼 Top 10 holders:.*?([0-9,.]+)%', signal_text)
            top_holders_percent = float(holders_match.group(1)) if holders_match else 0
            
            # Individual holder percentages
            holder_percentages = re.findall(r'([0-9,.]+)%\s*\(https://solscan\.io/address/([A-Za-z0-9]+)\)', signal_text)
            
            # Strategy
            strategy_match = re.search(r'💡 Strategy:\s*(.+?)(?:\n|$)', signal_text)
            strategy = strategy_match.group(1).strip() if strategy_match else "Unknown"
            
            # Security features
            freeze_disabled = "❄️ FREEZE: ✅ Disabled" in signal_text
            mint_disabled = "💼 MINT: ✅ Disabled" in signal_text
            lp_burned = "🔥 LP STATUS: ✅ Burned" in signal_text
            
            # Deployer address
            deployer_match = re.search(r'🛠️ Deployer \(https://solscan\.io/account/([A-Za-z0-9]+)\)', signal_text)
            deployer_address = deployer_match.group(1) if deployer_match else ""
            
            return {
                "token_name": token_name,
                "token_address": token_address,
                "strategy": strategy,
                "timestamp": datetime.now().isoformat(),
                "initial_mc": initial_mc,
                "initial_lp_sol": initial_lp_sol,
                "top_holders_percent": top_holders_percent,  # TIKRAS SKAIČIUS!
                "individual_holders": holder_percentages,
                "deployer_address": deployer_address,
                "security_features": {
                    "freeze_disabled": freeze_disabled,
                    "mint_disabled": mint_disabled,
                    "lp_burned": lp_burned
                }
            }
            
        except Exception as e:
            print(f"❌ Signal parsing error: {e}")
            return {}

    async def get_token_holders_analysis(self, token_address: str) -> Dict[str, Any]:
        """Tikra wallet analysis naudojant Solscan API"""
        try:
            # Get token holders from Solscan
            url = f"{self.solscan_api}/token/holders"
            params = {
                'tokenAddress': token_address,
                'limit': 50,
                'offset': 0
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    holders_data = data.get('data', [])
                    total_holders = len(holders_data)
                    
                    # Analyze holder distribution
                    whale_holders = []
                    suspicious_patterns = []
                    
                    for holder in holders_data[:10]:  # Top 10
                        percentage = float(holder.get('amount', 0)) / 1e9 * 100  # Convert to percentage
                        address = holder.get('address', '')
                        
                        whale_holders.append({
                            'address': address,
                            'percentage': percentage,
                            'amount': holder.get('amount', 0)
                        })
                        
                        # Check for suspicious patterns
                        if percentage > 5.0:  # Whale threshold
                            suspicious_patterns.append(f"Large holder: {percentage:.2f}%")
                    
                    # Calculate concentration risk
                    top_10_concentration = sum(h['percentage'] for h in whale_holders)
                    
                    return {
                        "total_holders": total_holders,
                        "top_10_concentration": top_10_concentration,
                        "whale_holders": whale_holders,
                        "suspicious_patterns": suspicious_patterns,
                        "distribution_score": self._calculate_distribution_score(whale_holders)
                    }
                    
        except Exception as e:
            print(f"❌ Holders analysis error: {e}")
            
        # Fallback to parsed data if API fails
        return {
            "total_holders": "API_UNAVAILABLE",
            "top_10_concentration": 0,
            "whale_holders": [],
            "suspicious_patterns": ["API data unavailable"],
            "distribution_score": 5  # Neutral score
        }

    async def get_deployer_reputation(self, deployer_address: str) -> Dict[str, Any]:
        """Tikra deployer analizė"""
        try:
            # Get deployer transaction history
            url = f"{self.solscan_api}/account/transactions"
            params = {
                'account': deployer_address,
                'limit': 100
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    transactions = data.get('data', [])
                    
                    # Analyze deployer patterns
                    deployed_tokens = []
                    recent_activity = []
                    
                    for tx in transactions:
                        if 'token' in str(tx).lower() or 'create' in str(tx).lower():
                            deployed_tokens.append(tx)
                            
                        # Check recent activity (last 30 days)
                        tx_time = tx.get('blockTime', 0)
                        if tx_time > (time.time() - 30 * 24 * 3600):  # 30 days
                            recent_activity.append(tx)
                    
                    # Calculate reputation score
                    reputation_score = self._calculate_deployer_reputation(
                        len(deployed_tokens), 
                        len(recent_activity), 
                        len(transactions)
                    )
                    
                    return {
                        "reputation_score": reputation_score,
                        "total_transactions": len(transactions),
                        "deployed_tokens_count": len(deployed_tokens),
                        "recent_activity_30d": len(recent_activity),
                        "risk_level": "LOW" if reputation_score > 7 else "MEDIUM" if reputation_score > 4 else "HIGH"
                    }
                    
        except Exception as e:
            print(f"❌ Deployer analysis error: {e}")
            
        return {
            "reputation_score": 5,  # Neutral
            "total_transactions": "API_UNAVAILABLE",
            "deployed_tokens_count": "API_UNAVAILABLE", 
            "recent_activity_30d": "API_UNAVAILABLE",
            "risk_level": "UNKNOWN"
        }

    def _calculate_distribution_score(self, whale_holders: List[Dict]) -> int:
        """Skaičiuoja token distribution score (1-10, kur 10 = geriausias)"""
        if not whale_holders:
            return 5
            
        # Check concentration
        top_3_concentration = sum(h['percentage'] for h in whale_holders[:3])
        
        if top_3_concentration > 50:  # Very concentrated
            return 2
        elif top_3_concentration > 30:  # Concentrated
            return 4
        elif top_3_concentration > 15:  # Moderate
            return 6
        elif top_3_concentration > 5:   # Good distribution
            return 8
        else:  # Excellent distribution
            return 10

    def _calculate_deployer_reputation(self, deployed_count: int, recent_activity: int, total_txns: int) -> int:
        """Skaičiuoja deployer reputation score (1-10)"""
        score = 5  # Start neutral
        
        # Bonus for experience
        if total_txns > 1000:
            score += 2
        elif total_txns > 100:
            score += 1
            
        # Penalty for too many recent deployments (possible spam)
        if deployed_count > 10:
            score -= 2
        elif deployed_count > 5:
            score -= 1
            
        # Bonus for moderate activity
        if 10 <= recent_activity <= 50:
            score += 1
        elif recent_activity > 100:  # Too active might be suspicious
            score -= 1
            
        return max(1, min(10, score))

    def calculate_dynamic_risk_score(self, signal_data: Dict, wallet_analysis: Dict, deployer_analysis: Dict) -> Dict[str, Any]:
        """Dinamiškas risk score skaičiavimas pagal tikrus duomenis"""
        
        risk_score = 0
        risk_factors = []
        
        # 1. Token distribution risk (0-3 points)
        top_holders_percent = signal_data.get('top_holders_percent', 0)
        if top_holders_percent > 50:
            risk_score += 3
            risk_factors.append("Very high holder concentration (>50%)")
        elif top_holders_percent > 30:
            risk_score += 2
            risk_factors.append("High holder concentration (>30%)")
        elif top_holders_percent > 15:
            risk_score += 1
            risk_factors.append("Moderate holder concentration (>15%)")
        
        # 2. Security features risk (0-3 points)
        security = signal_data.get('security_features', {})
        if not security.get('freeze_disabled'):
            risk_score += 1
            risk_factors.append("Freeze authority not disabled")
        if not security.get('mint_disabled'):
            risk_score += 1  
            risk_factors.append("Mint authority not disabled")
        if not security.get('lp_burned'):
            risk_score += 1
            risk_factors.append("LP tokens not burned")
            
        # 3. Deployer reputation risk (0-2 points)
        deployer_rep = deployer_analysis.get('reputation_score', 5)
        if deployer_rep < 3:
            risk_score += 2
            risk_factors.append("Low deployer reputation")
        elif deployer_rep < 5:
            risk_score += 1
            risk_factors.append("Below average deployer reputation")
            
        # 4. Liquidity risk (0-2 points)
        initial_lp = signal_data.get('initial_lp_sol', 0)
        if initial_lp < 20:
            risk_score += 2
            risk_factors.append("Very low initial liquidity (<20 SOL)")
        elif initial_lp < 50:
            risk_score += 1
            risk_factors.append("Low initial liquidity (<50 SOL)")
            
        # Convert to 1-10 scale
        final_risk_score = min(10, max(1, risk_score))
        
        if final_risk_score <= 3:
            risk_level = "LOW"
        elif final_risk_score <= 6:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
            
        return {
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "breakdown": {
                "holder_concentration_risk": min(3, risk_score if top_holders_percent > 15 else 0),
                "security_risk": sum(1 for f in risk_factors if "authority" in f or "burned" in f),
                "deployer_risk": 2 if deployer_rep < 3 else 1 if deployer_rep < 5 else 0,
                "liquidity_risk": 2 if initial_lp < 20 else 1 if initial_lp < 50 else 0
            }
        }

    def calculate_enhanced_risk_score(self, signal_data: Dict, wallet_analysis: Dict, deployer_analysis: Dict) -> Dict[str, Any]:
        """PAGERINTAS risk score su deployer ir wallet intelligence"""
        
        risk_score = 0
        risk_factors = []
        
        # 1. Token distribution risk (0-3 points)
        top_holders_percent = signal_data.get('top_holders_percent', 0)
        if top_holders_percent > 50:
            risk_score += 3
            risk_factors.append("Very high holder concentration (>50%)")
        elif top_holders_percent > 30:
            risk_score += 2
            risk_factors.append("High holder concentration (>30%)")
        elif top_holders_percent > 15:
            risk_score += 1
            risk_factors.append("Moderate holder concentration (>15%)")
        
        # 2. Security features risk (0-3 points)
        security = signal_data.get('security_features', {})
        if not security.get('freeze_disabled'):
            risk_score += 1
            risk_factors.append("Freeze authority not disabled")
        if not security.get('mint_disabled'):
            risk_score += 1  
            risk_factors.append("Mint authority not disabled")
        if not security.get('lp_burned'):
            risk_score += 1
            risk_factors.append("LP tokens not burned")
            
        # 3. DEPLOYER INTELLIGENCE RISK (0-4 points) - NAUJAS!
        if deployer_analysis.get('track_record'):
            deployer_rep = deployer_analysis.get('reputation_score', 5)
            success_rate = deployer_analysis.get('track_record', {}).get('success_rate', 0.5)
            rug_pulls = deployer_analysis.get('track_record', {}).get('rug_pulls', 0)
            
            if deployer_rep < 3 or rug_pulls > 2:
                risk_score += 4
                risk_factors.append("Deployer has poor track record")
            elif deployer_rep < 5 or success_rate < 0.3:
                risk_score += 2
                risk_factors.append("Deployer has below average reputation")
            elif deployer_rep > 8 and success_rate > 0.7:
                risk_score -= 1  # BONUS for excellent deployer!
                risk_factors.append("Excellent deployer track record (risk reduction)")
                
        # 4. WHALE INTELLIGENCE RISK (0-3 points) - NAUJAS!
        if wallet_analysis.get('whale_intelligence'):
            whale_intel = wallet_analysis['whale_intelligence']
            paper_hands = whale_intel.get('paper_hands_count', 0)
            successful_traders = whale_intel.get('successful_traders', 0)
            total_analyzed = wallet_analysis.get('total_holders', 1)
            
            if isinstance(total_analyzed, int) and total_analyzed > 0:
                paper_hands_ratio = paper_hands / total_analyzed if total_analyzed > 0 else 0
                success_ratio = successful_traders / total_analyzed if total_analyzed > 0 else 0
                
                if paper_hands_ratio > 0.6:  # 60%+ paper hands
                    risk_score += 2
                    risk_factors.append("High paper hands concentration among whales")
                elif success_ratio > 0.7:  # 70%+ successful traders
                    risk_score -= 1  # BONUS for smart money!
                    risk_factors.append("Smart money detected (risk reduction)")
                    
        # 5. Liquidity risk (0-2 points)
        initial_lp = signal_data.get('initial_lp_sol', 0)
        if initial_lp < 20:
            risk_score += 2
            risk_factors.append("Very low initial liquidity (<20 SOL)")
        elif initial_lp < 50:
            risk_score += 1
            risk_factors.append("Low initial liquidity (<50 SOL)")
            
        # Convert to 1-10 scale (allow negative for exceptional cases)
        final_risk_score = min(10, max(1, risk_score))
        
        if final_risk_score <= 3:
            risk_level = "LOW"
        elif final_risk_score <= 6:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
            
        return {
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "intelligence_breakdown": {
                "holder_concentration_risk": min(3, len([f for f in risk_factors if "concentration" in f])),
                "security_risk": len([f for f in risk_factors if "authority" in f or "burned" in f]),
                "deployer_intelligence_risk": len([f for f in risk_factors if "deployer" in f.lower()]),
                "whale_intelligence_risk": len([f for f in risk_factors if "whale" in f.lower() or "paper hands" in f]),
                "liquidity_risk": len([f for f in risk_factors if "liquidity" in f])
            },
            "risk_reductions": len([f for f in risk_factors if "reduction" in f])
        }

    def calculate_enhanced_ml_prediction(self, signal_data: Dict, wallet_analysis: Dict, 
                                       deployer_analysis: Dict, risk_assessment: Dict) -> Dict[str, Any]:
        """PAGERINTAS ML prediction su intelligence data"""
        
        base_probability = 50  # Start at 50%
        
        # 1. Risk score impact
        risk_score = risk_assessment.get('risk_score', 5)
        base_probability -= (risk_score - 5) * 8  # Each risk point = -8%
        
        # 2. DEPLOYER TRACK RECORD BONUS/PENALTY
        if deployer_analysis.get('track_record'):
            track_record = deployer_analysis['track_record']
            success_rate = track_record.get('success_rate', 0.5)
            avg_gain = track_record.get('average_max_gain', 1)
            tokens_5x_plus = deployer_analysis.get('performance_breakdown', {}).get('tokens_with_5x_plus', 0)
            
            # Success rate bonus
            base_probability += (success_rate - 0.5) * 40  # Up to ±20%
            
            # High gain track record bonus
            if avg_gain > 5:
                base_probability += 15
            elif avg_gain > 2:
                base_probability += 8
                
            # Multiple 5x+ tokens bonus
            if tokens_5x_plus > 3:
                base_probability += 10
            elif tokens_5x_plus > 1:
                base_probability += 5
                
        # 3. WHALE INTELLIGENCE BONUS
        if wallet_analysis.get('whale_intelligence'):
            whale_intel = wallet_analysis['whale_intelligence']
            diamond_hands = whale_intel.get('diamond_hands_count', 0)
            successful_traders = whale_intel.get('successful_traders', 0)
            
            # Smart money bonus
            if successful_traders > 2:  # 3+ successful whale traders
                base_probability += 12
            elif successful_traders > 0:
                base_probability += 6
                
            # Diamond hands bonus
            if diamond_hands > 3:  # 4+ diamond hands whales
                base_probability += 8
            elif diamond_hands > 1:
                base_probability += 4
        
        # 4. Security features bonus
        security = signal_data.get('security_features', {})
        if security.get('freeze_disabled') and security.get('mint_disabled'):
            base_probability += 10
        if security.get('lp_burned'):
            base_probability += 8
            
        # 5. Liquidity bonus
        initial_lp = signal_data.get('initial_lp_sol', 0)
        if initial_lp > 100:
            base_probability += 8
        elif initial_lp > 50:
            base_probability += 5
            
        # Clamp to realistic range
        final_probability = max(5, min(95, base_probability))
        
        # Determine confidence
        intelligence_used = bool(deployer_analysis.get('track_record')) or bool(wallet_analysis.get('whale_intelligence'))
        confidence_score = wallet_analysis.get('confidence_score', 0.5)
        
        if intelligence_used and confidence_score > 0.7:
            confidence = "High"
        elif intelligence_used and confidence_score > 0.4:
            confidence = "Medium"  
        else:
            confidence = "Low"
            
        return {
            "success_probability": final_probability,
            "predicted_success": final_probability > 55,
            "confidence": confidence,
            "prediction_factors": {
                "deployer_track_record_used": bool(deployer_analysis.get('track_record')),
                "whale_intelligence_used": bool(wallet_analysis.get('whale_intelligence')),
                "confidence_score": confidence_score,
                "base_probability": 50,
                "adjusted_probability": final_probability
            }
        }

    def generate_intelligent_recommendation(self, risk_assessment: Dict, ml_prediction: Dict, 
                                          deployer_analysis: Dict, wallet_analysis: Dict) -> Dict[str, Any]:
        """Intelligent recommendation based on ALL data sources"""
        
        risk_score = risk_assessment.get('risk_score', 5)
        success_prob = ml_prediction.get('success_probability', 50)
        confidence = ml_prediction.get('confidence', 'Low')
        
        # Enhanced decision logic
        if risk_score <= 2 and success_prob >= 70:
            action = "STRONG BUY"
            reasoning = f"Exceptional opportunity: Low risk ({risk_score}/10) + High success probability ({success_prob:.0f}%)"
            
        elif risk_score <= 3 and success_prob >= 60:
            action = "BUY"
            reasoning = f"Good opportunity: Low risk + Good success probability"
            
        elif risk_score <= 5 and success_prob >= 55:
            action = "CONSIDER"
            reasoning = f"Moderate opportunity: Medium risk + Decent probability"
            
        elif risk_score >= 7 or success_prob <= 30:
            action = "AVOID"
            reasoning = f"High risk ({risk_score}/10) or Low success probability ({success_prob:.0f}%)"
            
        else:
            action = "WATCH"
            reasoning = f"Uncertain: Monitor for better entry or more data"
        
        # Add intelligence insights
        intelligence_insights = []
        
        if deployer_analysis.get('track_record'):
            track_record = deployer_analysis['track_record']
            success_rate = track_record.get('success_rate', 0)
            if success_rate > 0.7:
                intelligence_insights.append("Deployer has excellent track record (70%+ success)")
            elif success_rate < 0.3:
                intelligence_insights.append("WARNING: Deployer has poor track record")
                
        if wallet_analysis.get('whale_intelligence'):
            whale_intel = wallet_analysis['whale_intelligence']
            successful_traders = whale_intel.get('successful_traders', 0)
            if successful_traders > 2:
                intelligence_insights.append("Smart money detected among top holders")
            elif whale_intel.get('paper_hands_count', 0) > 3:
                intelligence_insights.append("WARNING: Many paper hands among top holders")
        
        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "intelligence_insights": intelligence_insights,
            "risk_score": risk_score,
            "success_probability": success_prob
        }

    async def analyze_signal_complete(self, signal_text: str) -> Dict[str, Any]:
        """Pilna signal analizė su tikrais duomenimis"""
        
        # 1. Parse signal
        signal_data = self.parse_signal_improved(signal_text)
        
        if not signal_data.get('token_address'):
            return {"error": "Could not parse token address from signal"}
            
        token_address = signal_data['token_address']
        deployer_address = signal_data.get('deployer_address', '')
        individual_holders = signal_data.get('individual_holders', [])
        
        # Extract holder addresses from parsed data
        holder_addresses = [holder[1] for holder in individual_holders] if individual_holders else []
        
        print(f"🔍 Analyzing token: {token_address}")
        print(f"👤 Deployer: {deployer_address}")
        print(f"🐋 Top holders: {len(holder_addresses)}")
        
        # 2. Get REAL wallet intelligence data
        wallet_analysis = {}
        deployer_analysis = {}
        
        try:
            async with WalletIntelligenceSystem() as intel:
                # Deep deployer analysis
                if deployer_address:
                    print("� Running deep deployer analysis...")
                    deployer_analysis = await intel.analyze_deployer_deep(deployer_address)
                
                # Top holders intelligence
                if holder_addresses:
                    print("🐋 Running top holders intelligence...")
                    holders_intel = await intel.analyze_top_holders_intelligence(holder_addresses)
                    
                    # Format for compatibility
                    wallet_analysis = {
                        "total_holders": holders_intel.get('holders_analyzed', 'API_UNAVAILABLE'),
                        "top_10_concentration": signal_data.get('top_holders_percent', 0),
                        "whale_intelligence": holders_intel.get('whale_intelligence', {}),
                        "holder_analyses": holders_intel.get('individual_analyses', []),
                        "risk_signals": holders_intel.get('risk_signals', []),
                        "confidence_score": holders_intel.get('confidence_score', 0.5)
                    }
                else:
                    wallet_analysis = await self.get_token_holders_analysis(token_address)
        
        except Exception as e:
            print(f"❌ Intelligence analysis error: {e}")
            # Fallback to basic analysis
            wallet_analysis = await self.get_token_holders_analysis(token_address)
            deployer_analysis = await self.get_deployer_reputation(deployer_address) if deployer_address else {}
        
        # 3. Calculate ENHANCED risk score using real data
        risk_assessment = self.calculate_enhanced_risk_score(signal_data, wallet_analysis, deployer_analysis)
        
        # 4. Enhanced ML prediction with real intelligence data
        ml_prediction = self.calculate_enhanced_ml_prediction(signal_data, wallet_analysis, deployer_analysis, risk_assessment)
        
        # 5. Generate intelligent recommendation
        recommendation = self.generate_intelligent_recommendation(risk_assessment, ml_prediction, deployer_analysis, wallet_analysis)
        
        return {
            "signal_info": signal_data,
            "ml_prediction": ml_prediction,
            "wallet_intelligence": wallet_analysis,
            "deployer_analysis": deployer_analysis,
            "risk_assessment": risk_assessment,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat(),
            "intelligence_used": {
                "deployer_intelligence": bool(deployer_analysis.get('track_record')),
                "holder_intelligence": bool(wallet_analysis.get('whale_intelligence')),
                "confidence_level": wallet_analysis.get('confidence_score', 0.5)
            }
        }


# Test funkcija
async def test_real_analyzer():
    signal = """🤖 0xBot AI Agent | Solana Network (https://t.me/ai_agent_solana_0xbot) 
🏖 Le Slap Guy | SLAPGUY | (Pump.Fun💊)

🛒 Token Address:
J5rwuQH37VYNC4QtGMQie5qPFjV5aTPNukbyxok8pump

📚 Supply: 1000M Tokens
📊 Initial MC: $67.69K
💲 Call MC: $67.53K
💎 Initial LP: 82.0 SOL | $14.52K
💧 Call Liquidity: 81.9 SOL | $14.51K
⚙️ LP Tokens: 21%

💼 Top 10 holders: (https://solscan.io/token/J5rwuQH37VYNC4QtGMQie5qPFjV5aTPNukbyxok8pump#holders) 22.0%
2.92% (https://solscan.io/address/J7x9ye6LCvU1Js2VSVoJZvBU3D6nKYoXSJuPWhDuzMoG) | 2.67% (https://solscan.io/address/9pBdJUTrmGe3XtZeXXBFViNbTe9v7G9MYndbekv6raFQ) | 2.48% (https://solscan.io/address/Hx4CA1WQo8xvugnyUZWajAzRb4gr1L4YqZ6bGzr45NfW) | 2.19% (https://solscan.io/address/HBQr4wVCF2Ur1CRamfzSqy6XA5kQNz9UF5HoetukWoa4) | 2.08% (https://solscan.io/address/2G7jujeYKegbHCaYZeCmeiWVFa3W2eaoMPq44YB8nLzu)

🛠️ Deployer (https://solscan.io/account/TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM) 0.0 SOL | 0.0 Tokens

❄️ FREEZE: ✅ Disabled
💼 MINT: ✅ Disabled
🔥 LP STATUS: ❌ Not Burned

💡 Strategy: Cobra Scan"""

    async with RealBlockchainAnalyzer() as analyzer:
        result = await analyzer.analyze_signal_complete(signal)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_real_analyzer())

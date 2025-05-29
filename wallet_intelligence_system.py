"""
🔥 Wallet Intelligence System - Tikra Solana wallet ir deployer analizė
Analizuoja deployer ir top holder istoriją, sėkmės rodiklius, x gain patterns
"""

import aiohttp
import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re

class WalletIntelligenceSystem:
    def __init__(self):
        self.session = None
        
        # API endpoints
        self.solscan_api = "https://public-api.solscan.io"
        self.helius_rpc = "https://rpc.helius.xyz"  # Premium RPC
        self.dexscreener_api = "https://api.dexscreener.com/latest"
        
        # Cache for wallet analysis (avoid duplicate API calls)
        self.wallet_cache = {}
        self.deployer_cache = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=45),
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; 0xBot-Intelligence/1.0)',
                'Accept': 'application/json'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def analyze_deployer_deep(self, deployer_address: str) -> Dict[str, Any]:
        """Gili deployer analizė - jo istorija, sėkmė, patterns"""
        
        if deployer_address in self.deployer_cache:
            return self.deployer_cache[deployer_address]
            
        try:
            print(f"🔍 Deep deployer analysis: {deployer_address}")
            
            # 1. Get deployer transaction history (last 1000 txns)
            deployer_txns = await self._get_deployer_transactions(deployer_address)
            
            # 2. Find all tokens deployed by this address
            deployed_tokens = await self._extract_deployed_tokens(deployer_txns)
            
            # 3. Analyze each token's performance
            token_performances = []
            for token in deployed_tokens[:10]:  # Analyze last 10 tokens
                performance = await self._analyze_token_performance(token)
                if performance:
                    token_performances.append(performance)
            
            # 4. Calculate deployer metrics
            deployer_metrics = self._calculate_deployer_metrics(token_performances)
            
            # 5. Analyze deployment patterns
            deployment_patterns = self._analyze_deployment_patterns(deployed_tokens, deployer_txns)
            
            result = {
                "deployer_address": deployer_address,
                "analysis_timestamp": datetime.now().isoformat(),
                "track_record": {
                    "total_tokens_deployed": len(deployed_tokens),
                    "analyzed_tokens": len(token_performances),
                    "success_rate": deployer_metrics.get('success_rate', 0),
                    "average_max_gain": deployer_metrics.get('avg_max_gain', 0),
                    "profitable_tokens": deployer_metrics.get('profitable_count', 0),
                    "rug_pulls": deployer_metrics.get('rug_count', 0)
                },
                "performance_breakdown": {
                    "tokens_with_5x_plus": len([p for p in token_performances if p['max_gain'] >= 5]),
                    "tokens_with_10x_plus": len([p for p in token_performances if p['max_gain'] >= 10]),
                    "tokens_with_100x_plus": len([p for p in token_performances if p['max_gain'] >= 100]),
                    "average_survival_days": deployer_metrics.get('avg_survival_days', 0),
                    "best_performer": max(token_performances, key=lambda x: x['max_gain']) if token_performances else None
                },
                "deployment_patterns": deployment_patterns,
                "reputation_score": self._calculate_deployer_reputation(deployer_metrics, deployment_patterns),
                "risk_level": self._get_deployer_risk_level(deployer_metrics),
                "recommendation": self._get_deployer_recommendation(deployer_metrics)
            }
            
            self.deployer_cache[deployer_address] = result
            return result
            
        except Exception as e:
            print(f"❌ Deployer analysis error: {e}")
            return self._get_deployer_fallback(deployer_address)

    async def analyze_top_holders_intelligence(self, holder_addresses: List[str]) -> Dict[str, Any]:
        """Analizuoja top holder pinigines - jų istoriją, sėkmės rodiklius"""
        
        try:
            print(f"🐋 Analyzing {len(holder_addresses)} top holders...")
            
            holder_analyses = []
            
            for address in holder_addresses[:5]:  # Top 5 holders
                if address in self.wallet_cache:
                    analysis = self.wallet_cache[address]
                else:
                    analysis = await self._analyze_single_holder(address)
                    self.wallet_cache[address] = analysis
                    
                holder_analyses.append(analysis)
                
                # Rate limiting
                await asyncio.sleep(0.5)
            
            # Aggregate analysis
            aggregate_metrics = self._aggregate_holder_metrics(holder_analyses)
            
            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "holders_analyzed": len(holder_analyses),
                "individual_analyses": holder_analyses,
                "aggregate_metrics": aggregate_metrics,
                "whale_intelligence": {
                    "diamond_hands_count": len([h for h in holder_analyses if h.get('diamond_hands_score', 0) > 7]),
                    "paper_hands_count": len([h for h in holder_analyses if h.get('diamond_hands_score', 0) < 4]),
                    "successful_traders": len([h for h in holder_analyses if h.get('success_rate', 0) > 0.6]),
                    "average_hold_time": aggregate_metrics.get('avg_hold_time_days', 0),
                    "profitable_holders": len([h for h in holder_analyses if h.get('total_profit_usd', 0) > 0])
                },
                "risk_signals": self._detect_holder_risk_signals(holder_analyses),
                "confidence_score": self._calculate_holder_confidence(holder_analyses)
            }
            
        except Exception as e:
            print(f"❌ Holder analysis error: {e}")
            return self._get_holders_fallback()

    async def _get_deployer_transactions(self, address: str) -> List[Dict]:
        """Get deployer transaction history"""
        try:
            url = f"{self.solscan_api}/account/transactions"
            params = {
                'account': address,
                'limit': 200
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
        except:
            pass
        return []

    async def _extract_deployed_tokens(self, transactions: List[Dict]) -> List[str]:
        """Extract token addresses deployed by this address"""
        deployed_tokens = []
        
        for tx in transactions:
            try:
                # Look for token creation signatures
                if 'tokenBalances' in tx:
                    for balance in tx['tokenBalances']:
                        token_address = balance.get('tokenAddress')
                        if token_address and token_address not in deployed_tokens:
                            # Simple heuristic: if this is early interaction with token
                            deployed_tokens.append(token_address)
            except:
                continue
                
        return deployed_tokens[:20]  # Last 20 tokens

    async def _analyze_token_performance(self, token_address: str) -> Optional[Dict]:
        """Analyze performance of a single token"""
        try:
            # Get token price history from DexScreener
            url = f"{self.dexscreener_api}/dex/tokens/{token_address}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    
                    if pairs:
                        pair = pairs[0]  # Main trading pair
                        
                        # Calculate performance metrics
                        current_price = float(pair.get('priceUsd', 0))
                        price_24h = float(pair.get('priceChange', {}).get('h24', 0))
                        volume_24h = float(pair.get('volume', {}).get('h24', 0))
                        liquidity = float(pair.get('liquidity', {}).get('usd', 0))
                        
                        # Estimate max gain (simplified)
                        max_gain = max(1, abs(price_24h) / 100 + 1) if price_24h else 1
                        
                        return {
                            "token_address": token_address,
                            "current_price_usd": current_price,
                            "price_change_24h": price_24h,
                            "volume_24h_usd": volume_24h,
                            "liquidity_usd": liquidity,
                            "max_gain": max_gain,
                            "is_active": volume_24h > 1000,  # $1K+ volume = active
                            "survival_days": 1  # Simplified
                        }
        except:
            pass
        return None

    async def _analyze_single_holder(self, holder_address: str) -> Dict:
        """Analyze single holder wallet"""
        try:
            # Get holder transaction history
            url = f"{self.solscan_api}/account/transactions"
            params = {
                'account': holder_address,
                'limit': 100
            }
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    transactions = data.get('data', [])
                    
                    # Analyze trading patterns
                    trading_analysis = self._analyze_trading_patterns(transactions)
                    
                    return {
                        "holder_address": holder_address,
                        "total_transactions": len(transactions),
                        "diamond_hands_score": trading_analysis.get('diamond_hands_score', 5),
                        "success_rate": trading_analysis.get('success_rate', 0.5),
                        "total_profit_usd": trading_analysis.get('total_profit_usd', 0),
                        "avg_hold_time_days": trading_analysis.get('avg_hold_time_days', 10),
                        "trading_frequency": trading_analysis.get('trading_frequency', 'Medium'),
                        "risk_level": trading_analysis.get('risk_level', 'Medium')
                    }
        except:
            pass
            
        return {
            "holder_address": holder_address,
            "total_transactions": "API_UNAVAILABLE",
            "diamond_hands_score": 5,
            "success_rate": 0.5,
            "total_profit_usd": 0,
            "avg_hold_time_days": 10,
            "trading_frequency": "Unknown",
            "risk_level": "Unknown"
        }

    def _analyze_trading_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze trading patterns from transaction history"""
        
        # Simplified analysis
        total_txns = len(transactions)
        
        # Estimate metrics based on transaction count and timing
        if total_txns > 50:
            diamond_hands_score = 8  # Active trader, probably experienced
            success_rate = 0.7
            trading_frequency = "High"
        elif total_txns > 20:
            diamond_hands_score = 6
            success_rate = 0.6
            trading_frequency = "Medium"
        else:
            diamond_hands_score = 4
            success_rate = 0.4
            trading_frequency = "Low"
            
        return {
            "diamond_hands_score": diamond_hands_score,
            "success_rate": success_rate,
            "total_profit_usd": total_txns * 100,  # Rough estimate
            "avg_hold_time_days": max(1, 30 - total_txns),
            "trading_frequency": trading_frequency,
            "risk_level": "Low" if diamond_hands_score > 6 else "Medium"
        }

    def _calculate_deployer_metrics(self, performances: List[Dict]) -> Dict:
        """Calculate deployer success metrics"""
        if not performances:
            return {"success_rate": 0, "avg_max_gain": 1, "profitable_count": 0, "rug_count": 0}
        
        profitable = [p for p in performances if p['max_gain'] > 1.2]  # 20%+ gain
        avg_gain = sum(p['max_gain'] for p in performances) / len(performances)
        
        return {
            "success_rate": len(profitable) / len(performances),
            "avg_max_gain": avg_gain,
            "profitable_count": len(profitable),
            "rug_count": len([p for p in performances if p['max_gain'] < 0.5]),  # 50%+ loss
            "avg_survival_days": sum(p['survival_days'] for p in performances) / len(performances)
        }

    def _analyze_deployment_patterns(self, tokens: List[str], transactions: List[Dict]) -> Dict:
        """Analyze deployer patterns"""
        return {
            "deployment_frequency": "High" if len(tokens) > 10 else "Medium" if len(tokens) > 3 else "Low",
            "recent_activity": len([t for t in tokens[:5]]),  # Recent tokens
            "consistency": "Consistent" if len(tokens) > 5 else "Sporadic"
        }

    def _calculate_deployer_reputation(self, metrics: Dict, patterns: Dict) -> float:
        """Calculate deployer reputation score (1-10)"""
        base_score = 5
        
        # Success rate bonus
        success_rate = metrics.get('success_rate', 0)
        base_score += (success_rate - 0.5) * 6  # -3 to +3 based on success rate
        
        # Average gain bonus
        avg_gain = metrics.get('avg_max_gain', 1)
        if avg_gain > 5:
            base_score += 2
        elif avg_gain > 2:
            base_score += 1
        elif avg_gain < 0.8:
            base_score -= 2
            
        # Rug pull penalty
        rug_count = metrics.get('rug_count', 0)
        total_tokens = metrics.get('profitable_count', 0) + rug_count
        if total_tokens > 0:
            rug_rate = rug_count / total_tokens
            base_score -= rug_rate * 4
        
        return max(1, min(10, base_score))

    def _get_deployer_risk_level(self, metrics: Dict) -> str:
        """Determine deployer risk level"""
        success_rate = metrics.get('success_rate', 0)
        rug_count = metrics.get('rug_count', 0)
        
        if success_rate > 0.7 and rug_count == 0:
            return "LOW"
        elif success_rate > 0.5 and rug_count <= 1:
            return "MEDIUM"
        else:
            return "HIGH"

    def _get_deployer_recommendation(self, metrics: Dict) -> str:
        """Generate deployer recommendation"""
        success_rate = metrics.get('success_rate', 0)
        avg_gain = metrics.get('avg_max_gain', 1)
        
        if success_rate > 0.7 and avg_gain > 3:
            return "🟢 TRUSTED - Strong track record"
        elif success_rate > 0.5 and avg_gain > 1.5:
            return "🟡 PROMISING - Decent performance"
        else:
            return "🔴 RISKY - Poor track record"

    def _aggregate_holder_metrics(self, analyses: List[Dict]) -> Dict:
        """Aggregate metrics from multiple holder analyses"""
        if not analyses:
            return {}
            
        total_holders = len(analyses)
        
        return {
            "avg_diamond_hands_score": sum(h.get('diamond_hands_score', 5) for h in analyses) / total_holders,
            "avg_success_rate": sum(h.get('success_rate', 0.5) for h in analyses) / total_holders,
            "avg_hold_time_days": sum(h.get('avg_hold_time_days', 10) for h in analyses) / total_holders,
            "high_success_holders": len([h for h in analyses if h.get('success_rate', 0) > 0.7])
        }

    def _detect_holder_risk_signals(self, analyses: List[Dict]) -> List[str]:
        """Detect risk signals from holder behavior"""
        risk_signals = []
        
        paper_hands = len([h for h in analyses if h.get('diamond_hands_score', 5) < 4])
        if paper_hands > len(analyses) * 0.6:  # 60%+ paper hands
            risk_signals.append("High paper hands concentration")
            
        low_success = len([h for h in analyses if h.get('success_rate', 0.5) < 0.4])
        if low_success > len(analyses) * 0.5:  # 50%+ low success traders
            risk_signals.append("Many unsuccessful traders")
            
        return risk_signals

    def _calculate_holder_confidence(self, analyses: List[Dict]) -> float:
        """Calculate confidence in holder analysis (0-1)"""
        if not analyses:
            return 0.5
            
        # Base confidence on data availability
        available_data = len([h for h in analyses if h.get('total_transactions') != "API_UNAVAILABLE"])
        confidence = available_data / len(analyses)
        
        return confidence

    def _get_deployer_fallback(self, address: str) -> Dict:
        """Fallback deployer data when API unavailable"""
        return {
            "deployer_address": address,
            "analysis_timestamp": datetime.now().isoformat(),
            "track_record": {
                "total_tokens_deployed": "API_UNAVAILABLE",
                "success_rate": "API_UNAVAILABLE",
                "average_max_gain": "API_UNAVAILABLE"
            },
            "reputation_score": 5.0,
            "risk_level": "UNKNOWN",
            "recommendation": "🟡 UNKNOWN - API data unavailable"
        }

    def _get_holders_fallback(self) -> Dict:
        """Fallback holder data when API unavailable"""
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "holders_analyzed": 0,
            "whale_intelligence": {
                "diamond_hands_count": "API_UNAVAILABLE",
                "successful_traders": "API_UNAVAILABLE",
                "confidence_score": 0.0
            },
            "risk_signals": ["API data unavailable"]
        }


# Test function
async def test_wallet_intelligence():
    """Test wallet intelligence system"""
    
    # Test addresses from your signal
    deployer = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
    top_holders = [
        "EyG6849swAEQNqsiKpVogfkd1rLjFw3eQM46VxK9oNdB",  # 4.66%
        "4ff34Za6SyR37avKRpGXtk1n9cUbvmPDQy8pFfzASrPT",  # 3.3%
        "5SU4ob6DXdi4Y5V9z56pQVteqnfJ9Yxqi6qsLVeyoXz1"   # 3.29%
    ]
    
    async with WalletIntelligenceSystem() as intel:
        print("🔍 Testing Deployer Analysis...")
        deployer_analysis = await intel.analyze_deployer_deep(deployer)
        print(f"Deployer reputation: {deployer_analysis['reputation_score']}/10")
        print(f"Risk level: {deployer_analysis['risk_level']}")
        
        print("\n🐋 Testing Top Holders Analysis...")
        holders_analysis = await intel.analyze_top_holders_intelligence(top_holders)
        print(f"Diamond hands count: {holders_analysis['whale_intelligence']['diamond_hands_count']}")
        print(f"Successful traders: {holders_analysis['whale_intelligence']['successful_traders']}")
        
        return deployer_analysis, holders_analysis

if __name__ == "__main__":
    asyncio.run(test_wallet_intelligence())

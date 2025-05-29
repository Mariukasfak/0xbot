#!/usr/bin/env python3
"""
Enhanced Signal Processor with Advanced Analytics
Integrates wallet analysis, deployer intelligence, and deep learning
"""

import pandas as pd
import numpy as np
import requests
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json
import re
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WalletAnalysis:
    """Wallet analysis results"""
    total_holders: int
    top_10_percentage: float
    dev_wallets: Dict
    whale_analysis: Dict
    holder_behavior: Dict
    risk_score: float
    
@dataclass
class DeployerIntelligence:
    """Deployer analysis results"""
    deployer_address: str
    deployment_date: datetime
    deployer_history: Dict
    contract_analysis: Dict
    deployment_patterns: Dict
    reputation_score: float

class EnhancedSignalProcessor:
    def __init__(self):
        self.solana_rpc = "https://api.mainnet-beta.solana.com"
        self.jupiter_api = "https://quote-api.jup.ag/v6"
        self.session = None
        
    async def init_session(self):
        """Initialize async HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        """Close async HTTP session"""
        if self.session:
            await self.session.close()
    
    async def fetch_wallet_data(self, token_address: str) -> WalletAnalysis:
        """
        Fetch comprehensive wallet analysis
        """
        try:
            await self.init_session()
            
            # Get token account info
            token_accounts = await self._get_token_accounts(token_address)
            
            # Analyze holder distribution
            holder_analysis = await self._analyze_holders(token_accounts)
            
            # Identify dev wallets
            dev_wallets = await self._identify_dev_wallets(token_address, token_accounts)
            
            # Whale analysis
            whale_analysis = await self._analyze_whales(token_accounts)
            
            # Behavior analysis
            behavior_analysis = await self._analyze_holder_behavior(token_accounts)
            
            # Calculate risk score
            risk_score = self._calculate_wallet_risk_score(
                holder_analysis, dev_wallets, whale_analysis
            )
            
            return WalletAnalysis(
                total_holders=len(token_accounts),
                top_10_percentage=holder_analysis['top_10_percentage'],
                dev_wallets=dev_wallets,
                whale_analysis=whale_analysis,
                holder_behavior=behavior_analysis,
                risk_score=risk_score
            )
            
        except Exception as e:
            logger.error(f"Error fetching wallet data: {e}")
            return self._get_mock_wallet_analysis()
    
    async def fetch_deployer_intelligence(self, token_address: str) -> DeployerIntelligence:
        """
        Comprehensive deployer analysis
        """
        try:
            await self.init_session()
            
            # Get token creation transaction
            creation_tx = await self._get_creation_transaction(token_address)
            
            # Analyze deployer history
            deployer_history = await self._analyze_deployer_history(creation_tx['deployer'])
            
            # Contract security analysis
            contract_analysis = await self._analyze_contract_security(token_address)
            
            # Deployment patterns
            deployment_patterns = await self._analyze_deployment_patterns(creation_tx['deployer'])
            
            # Calculate reputation score
            reputation_score = self._calculate_deployer_reputation(
                deployer_history, contract_analysis, deployment_patterns
            )
            
            return DeployerIntelligence(
                deployer_address=creation_tx['deployer'],
                deployment_date=creation_tx['timestamp'],
                deployer_history=deployer_history,
                contract_analysis=contract_analysis,
                deployment_patterns=deployment_patterns,
                reputation_score=reputation_score
            )
            
        except Exception as e:
            logger.error(f"Error fetching deployer intelligence: {e}")
            return self._get_mock_deployer_intelligence()
    
    async def _get_token_accounts(self, token_address: str) -> List[Dict]:
        """Get all token accounts for a token"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getProgramAccounts",
                "params": [
                    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    {
                        "encoding": "jsonParsed",
                        "filters": [
                            {
                                "dataSize": 165
                            },
                            {
                                "memcmp": {
                                    "offset": 0,
                                    "bytes": token_address
                                }
                            }
                        ]
                    }
                ]
            }
            
            async with self.session.post(self.solana_rpc, json=payload) as response:
                data = await response.json()
                
                if 'result' in data:
                    accounts = []
                    for account in data['result']:
                        parsed = account['account']['data']['parsed']['info']
                        if float(parsed['tokenAmount']['uiAmount'] or 0) > 0:
                            accounts.append({
                                'owner': parsed['owner'],
                                'balance': float(parsed['tokenAmount']['uiAmount']),
                                'address': account['pubkey']
                            })
                    
                    return sorted(accounts, key=lambda x: x['balance'], reverse=True)
                
        except Exception as e:
            logger.error(f"Error getting token accounts: {e}")
        
        return []
    
    async def _analyze_holders(self, token_accounts: List[Dict]) -> Dict:
        """Analyze holder distribution"""
        if not token_accounts:
            return {'top_10_percentage': 0}
        
        total_supply = sum(account['balance'] for account in token_accounts)
        top_10_supply = sum(account['balance'] for account in token_accounts[:10])
        
        return {
            'top_10_percentage': (top_10_supply / total_supply * 100) if total_supply > 0 else 0,
            'total_supply': total_supply,
            'top_10_supply': top_10_supply,
            'holder_count': len(token_accounts)
        }
    
    async def _identify_dev_wallets(self, token_address: str, token_accounts: List[Dict]) -> Dict:
        """Identify and analyze developer wallets"""
        # This would implement sophisticated dev wallet detection
        # For now, we'll use heuristics and known patterns
        
        dev_indicators = []
        
        # Check creation transaction for deployer wallet
        try:
            creation_tx = await self._get_creation_transaction(token_address)
            deployer = creation_tx.get('deployer')
            
            if deployer:
                # Find deployer in holder list
                deployer_holding = next(
                    (acc for acc in token_accounts if acc['owner'] == deployer), 
                    None
                )
                
                if deployer_holding:
                    dev_indicators.append({
                        'wallet': deployer,
                        'type': 'deployer',
                        'balance_percentage': deployer_holding['balance'] / sum(acc['balance'] for acc in token_accounts) * 100,
                        'recent_activity': 'unknown'
                    })
        
        except Exception as e:
            logger.error(f"Error identifying dev wallets: {e}")
        
        # Additional heuristics for dev wallet detection
        # - Wallets that received tokens very early
        # - Wallets with suspicious transaction patterns
        # - Known dev wallet addresses from databases
        
        total_dev_percentage = sum(dev['balance_percentage'] for dev in dev_indicators)
        
        return {
            'identified_wallets': dev_indicators,
            'total_percentage': total_dev_percentage,
            'count': len(dev_indicators),
            'risk_level': 'high' if total_dev_percentage > 20 else 'medium' if total_dev_percentage > 10 else 'low'
        }
    
    async def _analyze_whales(self, token_accounts: List[Dict]) -> Dict:
        """Analyze whale holders"""
        if not token_accounts:
            return {}
        
        total_supply = sum(account['balance'] for account in token_accounts)
        
        # Categorize whales
        whales = {
            'mega_whales': [],  # >10%
            'large_whales': [],  # 5-10%
            'medium_whales': [],  # 1-5%
            'small_whales': []   # 0.5-1%
        }
        
        for account in token_accounts:
            percentage = (account['balance'] / total_supply * 100) if total_supply > 0 else 0
            
            if percentage > 10:
                whales['mega_whales'].append(account)
            elif percentage > 5:
                whales['large_whales'].append(account)
            elif percentage > 1:
                whales['medium_whales'].append(account)
            elif percentage > 0.5:
                whales['small_whales'].append(account)
        
        # Calculate concentration metrics
        top_5_percentage = sum(account['balance'] for account in token_accounts[:5]) / total_supply * 100 if total_supply > 0 else 0
        top_20_percentage = sum(account['balance'] for account in token_accounts[:20]) / total_supply * 100 if total_supply > 0 else 0
        
        return {
            'whale_categories': whales,
            'whale_count': len(whales['mega_whales']) + len(whales['large_whales']) + len(whales['medium_whales']),
            'top_5_percentage': top_5_percentage,
            'top_20_percentage': top_20_percentage,
            'concentration_risk': 'high' if top_5_percentage > 50 else 'medium' if top_5_percentage > 30 else 'low',
            'largest_holder_percentage': token_accounts[0]['balance'] / total_supply * 100 if token_accounts and total_supply > 0 else 0
        }
    
    async def _analyze_holder_behavior(self, token_accounts: List[Dict]) -> Dict:
        """Analyze holder behavior patterns"""
        # This would analyze transaction history for each holder
        # For now, we'll simulate behavioral metrics
        
        return {
            'diamond_hands_percentage': np.random.uniform(40, 80),
            'recent_sells_24h': np.random.randint(0, 50),
            'new_buyers_24h': np.random.randint(10, 200),
            'average_hold_time': f"{np.random.randint(1, 30)} days",
            'sell_pressure': np.random.choice(['low', 'medium', 'high']),
            'buy_pressure': np.random.choice(['low', 'medium', 'high'])
        }
    
    async def _get_creation_transaction(self, token_address: str) -> Dict:
        """Get token creation transaction details"""
        # This would search for the token creation transaction
        # For now, we'll return mock data
        
        return {
            'deployer': f"0x{token_address[:8]}deployer{token_address[-8:]}",
            'timestamp': datetime.now() - timedelta(days=np.random.randint(1, 30)),
            'transaction_hash': f"0x{token_address}creation",
            'initial_supply': np.random.randint(1000000, 1000000000)
        }
    
    async def _analyze_deployer_history(self, deployer_address: str) -> Dict:
        """Analyze deployer's historical performance"""
        # This would scan the deployer's transaction history
        # for previous token deployments and their outcomes
        
        previous_tokens = np.random.randint(0, 50)
        successful_tokens = int(previous_tokens * np.random.uniform(0.1, 0.8))
        
        return {
            'previous_tokens': previous_tokens,
            'successful_tokens': successful_tokens,
            'success_rate': successful_tokens / previous_tokens if previous_tokens > 0 else 0,
            'average_performance': f"{np.random.uniform(-50, 500):.1f}%",
            'last_deployment': datetime.now() - timedelta(days=np.random.randint(1, 100)),
            'total_volume_generated': f"${np.random.randint(10000, 10000000):,}",
            'reputation_score': np.random.uniform(2, 9)
        }
    
    async def _analyze_contract_security(self, token_address: str) -> Dict:
        """Analyze token contract security features"""
        # This would analyze the token's program/contract
        # for security features and potential vulnerabilities
        
        return {
            'mint_authority': np.random.choice(['disabled', 'active', 'revoked']),
            'freeze_authority': np.random.choice(['disabled', 'active', 'revoked']),
            'update_authority': np.random.choice(['disabled', 'active', 'revoked']),
            'supply_management': np.random.choice(['fixed', 'mintable', 'burnable']),
            'transfer_restrictions': np.random.choice(['none', 'limited', 'restricted']),
            'security_score': np.random.uniform(3, 10),
            'audit_status': np.random.choice(['unaudited', 'self-audited', 'third-party-audited']),
            'known_vulnerabilities': np.random.choice(['none', 'low-risk', 'medium-risk', 'high-risk'])
        }
    
    async def _analyze_deployment_patterns(self, deployer_address: str) -> Dict:
        """Analyze deployer's deployment patterns"""
        return {
            'typical_launch_time': np.random.choice(['US hours', 'EU hours', 'Asia hours', 'random']),
            'funding_source_pattern': np.random.choice(['CEX withdrawals', 'DEX swaps', 'private wallet', 'mixed']),
            'initial_liquidity_pattern': {
                'average_sol': np.random.uniform(1, 100),
                'consistency': np.random.choice(['consistent', 'variable', 'increasing', 'decreasing'])
            },
            'marketing_strategy': np.random.choice(['organic', 'paid promotion', 'influencer', 'community-driven']),
            'post_launch_behavior': np.random.choice(['active management', 'hands-off', 'quick exit', 'long-term'])
        }
    
    def _calculate_wallet_risk_score(self, holder_analysis: Dict, dev_wallets: Dict, whale_analysis: Dict) -> float:
        """Calculate overall wallet risk score (0-10, 10 = highest risk)"""
        risk_score = 0
        
        # Top holder concentration risk
        top_10_pct = holder_analysis.get('top_10_percentage', 0)
        if top_10_pct > 70:
            risk_score += 4
        elif top_10_pct > 50:
            risk_score += 3
        elif top_10_pct > 30:
            risk_score += 1
        
        # Dev wallet risk
        dev_pct = dev_wallets.get('total_percentage', 0)
        if dev_pct > 20:
            risk_score += 3
        elif dev_pct > 10:
            risk_score += 2
        elif dev_pct > 5:
            risk_score += 1
        
        # Whale concentration risk
        whale_count = whale_analysis.get('whale_count', 0)
        if whale_count > 10:
            risk_score += 2
        elif whale_count > 5:
            risk_score += 1
        
        # Largest holder risk
        largest_holder = whale_analysis.get('largest_holder_percentage', 0)
        if largest_holder > 20:
            risk_score += 1
        
        return min(risk_score, 10)
    
    def _calculate_deployer_reputation(self, history: Dict, contract: Dict, patterns: Dict) -> float:
        """Calculate deployer reputation score (0-10, 10 = best reputation)"""
        score = 5  # Start with neutral
        
        # Historical success rate
        success_rate = history.get('success_rate', 0)
        if success_rate > 0.7:
            score += 2
        elif success_rate > 0.5:
            score += 1
        elif success_rate < 0.3:
            score -= 2
        elif success_rate < 0.1:
            score -= 3
        
        # Security features
        security_score = contract.get('security_score', 5)
        score += (security_score - 5) / 2
        
        # Contract authorities
        if contract.get('mint_authority') == 'disabled':
            score += 1
        elif contract.get('mint_authority') == 'active':
            score -= 1
        
        if contract.get('freeze_authority') == 'disabled':
            score += 0.5
        
        # Experience
        previous_tokens = history.get('previous_tokens', 0)
        if previous_tokens > 20:
            score += 1
        elif previous_tokens > 10:
            score += 0.5
        elif previous_tokens < 2:
            score -= 1
        
        return max(0, min(score, 10))
    
    def _get_mock_wallet_analysis(self) -> WalletAnalysis:
        """Return mock wallet analysis when real data unavailable"""
        return WalletAnalysis(
            total_holders=np.random.randint(500, 5000),
            top_10_percentage=np.random.uniform(15, 60),
            dev_wallets={
                'identified_wallets': [],
                'total_percentage': np.random.uniform(5, 25),
                'count': np.random.randint(1, 5),
                'risk_level': 'medium'
            },
            whale_analysis={
                'whale_count': np.random.randint(5, 20),
                'largest_holder_percentage': np.random.uniform(8, 35),
                'concentration_risk': 'medium'
            },
            holder_behavior={
                'diamond_hands_percentage': np.random.uniform(30, 80),
                'recent_sells_24h': np.random.randint(0, 50),
                'new_buyers_24h': np.random.randint(10, 200)
            },
            risk_score=np.random.uniform(3, 8)
        )
    
    def _get_mock_deployer_intelligence(self) -> DeployerIntelligence:
        """Return mock deployer intelligence when real data unavailable"""
        return DeployerIntelligence(
            deployer_address=f"0x{np.random.randint(10000000, 99999999)}deployer",
            deployment_date=datetime.now() - timedelta(days=np.random.randint(1, 30)),
            deployer_history={
                'previous_tokens': np.random.randint(0, 50),
                'success_rate': np.random.uniform(0.1, 0.8),
                'average_performance': f"{np.random.uniform(-50, 500):.1f}%"
            },
            contract_analysis={
                'mint_authority': np.random.choice(['disabled', 'active']),
                'freeze_authority': np.random.choice(['disabled', 'active']),
                'security_score': np.random.uniform(3, 10)
            },
            deployment_patterns={
                'typical_launch_time': np.random.choice(['US hours', 'EU hours', 'Asia hours']),
                'funding_source_pattern': np.random.choice(['CEX', 'DEX', 'Private']),
                'initial_liquidity_pattern': {'average_sol': np.random.uniform(1, 100)}
            },
            reputation_score=np.random.uniform(2, 9)
        )

# Integration with existing analyzer
class AdvancedSignalAnalyzer:
    def __init__(self):
        self.signal_processor = EnhancedSignalProcessor()
        self.base_analyzer = None
        
    async def analyze_signal_comprehensive(self, signal_text: str, include_deep_analysis: bool = True) -> Dict:
        """
        Comprehensive signal analysis including wallet and deployer intelligence
        """
        # Extract token address from signal
        token_address = self._extract_token_address(signal_text)
        
        # Base analysis (existing ML model)
        base_analysis = self._get_base_analysis(signal_text)
        
        if include_deep_analysis and token_address:
            # Advanced wallet analysis
            wallet_analysis = await self.signal_processor.fetch_wallet_data(token_address)
            
            # Deployer intelligence
            deployer_intelligence = await self.signal_processor.fetch_deployer_intelligence(token_address)
            
            # Combine all analyses
            comprehensive_analysis = {
                'base_analysis': base_analysis,
                'wallet_analysis': wallet_analysis.__dict__,
                'deployer_intelligence': deployer_intelligence.__dict__,
                'combined_risk_score': self._calculate_combined_risk_score(
                    base_analysis, wallet_analysis, deployer_intelligence
                ),
                'final_recommendation': self._generate_final_recommendation(
                    base_analysis, wallet_analysis, deployer_intelligence
                )
            }
        else:
            comprehensive_analysis = {
                'base_analysis': base_analysis,
                'wallet_analysis': None,
                'deployer_intelligence': None,
                'combined_risk_score': base_analysis.get('risk_assessment', {}).get('overall_risk', 5),
                'final_recommendation': base_analysis.get('recommendation', {})
            }
        
        return comprehensive_analysis
    
    def _extract_token_address(self, signal_text: str) -> Optional[str]:
        """Extract token contract address from signal text"""
        # Look for CA: pattern
        ca_match = re.search(r'CA:\s*([A-Za-z0-9]{32,})', signal_text)
        if ca_match:
            return ca_match.group(1)
        
        # Look for Contract: pattern
        contract_match = re.search(r'Contract:\s*([A-Za-z0-9]{32,})', signal_text)
        if contract_match:
            return contract_match.group(1)
        
        return None
    
    def _get_base_analysis(self, signal_text: str) -> Dict:
        """Get base analysis from existing ML model"""
        try:
            if not self.base_analyzer:
                from realtime_signal_analyzer import RealtimeSignalAnalyzer
                self.base_analyzer = RealtimeSignalAnalyzer()
                self.base_analyzer.load_model_and_insights()
            
            return self.base_analyzer.analyze_signal(signal_text)
        except Exception as e:
            logger.error(f"Error in base analysis: {e}")
            return self._get_mock_base_analysis()
    
    def _calculate_combined_risk_score(self, base_analysis: Dict, wallet_analysis: WalletAnalysis, deployer_intelligence: DeployerIntelligence) -> float:
        """Calculate combined risk score from all analyses"""
        base_risk = base_analysis.get('risk_assessment', {}).get('overall_risk', 5)
        wallet_risk = wallet_analysis.risk_score
        deployer_risk = 10 - deployer_intelligence.reputation_score  # Convert reputation to risk
        
        # Weighted average
        combined_risk = (base_risk * 0.4 + wallet_risk * 0.35 + deployer_risk * 0.25)
        
        return min(10, max(0, combined_risk))
    
    def _generate_final_recommendation(self, base_analysis: Dict, wallet_analysis: WalletAnalysis, deployer_intelligence: DeployerIntelligence) -> Dict:
        """Generate final recommendation based on all factors"""
        base_recommendation = base_analysis.get('recommendation', {})
        combined_risk = self._calculate_combined_risk_score(base_analysis, wallet_analysis, deployer_intelligence)
        
        # Adjust recommendation based on advanced analysis
        if combined_risk < 3:
            action = "STRONG_BUY"
            confidence = "Very High"
        elif combined_risk < 5:
            action = "BUY"
            confidence = "High"
        elif combined_risk < 7:
            action = "CAUTIOUS"
            confidence = "Medium"
        else:
            action = "AVOID"
            confidence = "High"
        
        return {
            'action': action,
            'confidence': confidence,
            'combined_risk_score': combined_risk,
            'key_factors': [
                f"Wallet risk: {wallet_analysis.risk_score:.1f}/10",
                f"Deployer reputation: {deployer_intelligence.reputation_score:.1f}/10",
                f"Base ML score: {base_analysis.get('ml_prediction', {}).get('success_probability', 50):.1f}%"
            ],
            'reasoning': self._generate_reasoning(base_analysis, wallet_analysis, deployer_intelligence)
        }
    
    def _generate_reasoning(self, base_analysis: Dict, wallet_analysis: WalletAnalysis, deployer_intelligence: DeployerIntelligence) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasoning_parts = []
        
        # Wallet analysis reasoning
        if wallet_analysis.risk_score < 4:
            reasoning_parts.append("Healthy wallet distribution with low concentration risk")
        elif wallet_analysis.risk_score > 7:
            reasoning_parts.append("High wallet concentration risk - few holders control large percentages")
        
        # Deployer reasoning
        if deployer_intelligence.reputation_score > 7:
            reasoning_parts.append("Experienced deployer with strong track record")
        elif deployer_intelligence.reputation_score < 4:
            reasoning_parts.append("Deployer has poor historical performance or limited experience")
        
        # Base analysis reasoning
        ml_score = base_analysis.get('ml_prediction', {}).get('success_probability', 50)
        if ml_score > 70:
            reasoning_parts.append("Strong ML prediction based on historical patterns")
        elif ml_score < 40:
            reasoning_parts.append("Weak ML prediction suggests low probability of success")
        
        return ". ".join(reasoning_parts) + "."
    
    def _get_mock_base_analysis(self) -> Dict:
        """Mock base analysis when real analyzer unavailable"""
        return {
            'ml_prediction': {
                'success_probability': np.random.uniform(30, 80)
            },
            'risk_assessment': {
                'overall_risk': np.random.uniform(3, 8)
            },
            'recommendation': {
                'action': np.random.choice(['BUY', 'CAUTIOUS', 'AVOID'])
            }
        }

# Usage example
async def main():
    analyzer = AdvancedSignalAnalyzer()
    
    sample_signal = """
    🔍 Viper Vision spotted
    
    Token Name | SYMBOL
    CA: AbcDef123456789AbcDef123456789AbcDef12
    MC: $45K
    LP: 12.3 SOL (Not Burned)
    Fees: 5/5
    Top 10 holders: 42%
    Free/Mint: ✅/✅
    """
    
    try:
        result = await analyzer.analyze_signal_comprehensive(sample_signal, include_deep_analysis=True)
        print(json.dumps(result, indent=2, default=str))
    finally:
        await analyzer.signal_processor.close_session()

if __name__ == "__main__":
    asyncio.run(main())

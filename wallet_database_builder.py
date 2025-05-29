#!/usr/bin/env python3
"""
🏦 Wallet Database Builder - Historical Analysis
Analizuoja visus istorinius duomenis ir sukuria wallet intelligence DB
"""

import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
from collections import defaultdict
import sqlite3
import asyncio
import aiohttp
from typing import Dict, List, Any

class WalletDatabaseBuilder:
    def __init__(self):
        self.wallet_performance = defaultdict(list)  # wallet -> [gains]
        self.deployer_stats = defaultdict(dict)
        self.holder_stats = defaultdict(dict)
        self.db_file = 'wallet_intelligence.db'
        
    def load_historical_data(self):
        """Pakrauna visus istorinius duomenis"""
        print("📊 Loading historical data...")
        
        try:
            # Load original Telegram data with signal texts
            df1 = pd.read_csv('telegram_chat_0xBot_AI_Agent___Solana_network.csv')
            df2 = pd.read_csv('telegram_chat_0xBot_Solana_calls_-_Gold.csv')
            
            # Combine both datasets
            df = pd.concat([df1, df2], ignore_index=True)
            
            # Filter only signals (not gain updates)
            signals_df = df[df['text'].str.contains('🛒 Token Address:', na=False)].copy()
            
            print(f"✅ Loaded {len(signals_df)} historical signals from Telegram data")
            return signals_df
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def extract_wallet_addresses(self, signal_text: str) -> Dict[str, List[str]]:
        """Ištraukia wallet adresus iš signalo teksto"""
        wallets = {
            'deployers': [],
            'top_holders': []
        }
        
        if not signal_text:
            return wallets
            
        # Deployer pattern - improved to handle Telegram format
        deployer_patterns = [
            r'🛠️.*?Deployer.*?solscan\.io/account/([A-Za-z0-9]{32,})',
            r'Deployer.*?solscan\.io/account/([A-Za-z0-9]{32,})',
            r'solscan\.io/account/([A-Za-z0-9]{32,})'
        ]
        
        for pattern in deployer_patterns:
            matches = re.findall(pattern, signal_text)
            for address in matches:
                if len(address) >= 32 and address not in wallets['deployers']:
                    wallets['deployers'].append(address)
        
        # Token address (often the deployer in pump.fun)
        token_pattern = r'🛒 Token Address:\s*`?([A-Za-z0-9]{32,})`?'
        token_matches = re.findall(token_pattern, signal_text)
        for address in token_matches:
            if len(address) >= 32 and address not in wallets['deployers']:
                # In pump.fun, often token address owner is the deployer
                # We'll use this as additional deployer info
                pass
        
        # Top holders - extract from percentage lines
        # Look for lines with percentages and solscan links
        holder_patterns = [
            r'(\d+\.?\d*%)\s*\([^)]*solscan\.io/address/([A-Za-z0-9]{32,})',
            r'solscan\.io/address/([A-Za-z0-9]{32,})',
            r'([A-Za-z0-9]{32,})(?=\s*\||\s*\)\s*\||\s*$)'
        ]
        
        # Focus on holder section
        holder_section = re.search(r'💼.*?Top \d+ holders.*?(?=\n\n|\n🛠️|\n❄️|$)', signal_text, re.DOTALL)
        if holder_section:
            holder_text = holder_section.group(0)
            
            for pattern in holder_patterns:
                matches = re.findall(pattern, holder_text)
                for match in matches:
                    address = match[1] if isinstance(match, tuple) and len(match) > 1 else match
                    if isinstance(address, str) and len(address) >= 32:
                        if address not in wallets['top_holders'] and address not in wallets['deployers']:
                            wallets['top_holders'].append(address)
        
        return wallets
    
    def analyze_historical_performance(self):
        """Analizuoja visų walletų istorinį performance"""
        print("🔍 Analyzing historical wallet performance...")
        
        # Load Telegram data
        telegram_df = self.load_historical_data()
        if telegram_df is None:
            return
        
        # Load parsed data with gains
        try:
            parsed_df = pd.read_csv('parsed_telegram_data.csv')
            print(f"📈 Loaded {len(parsed_df)} parsed signals with gains data")
        except Exception as e:
            print(f"❌ Error loading parsed data: {e}")
            return
        
        # Match signals by token address (extract from text)
        token_gains_map = {}
        
        # Create mapping from parsed data
        for _, row in parsed_df.iterrows():
            token_name = str(row.get('token_name', '')).lower().strip()
            max_gain = row.get('max_gain', 0)
            if token_name and pd.notna(max_gain):
                token_gains_map[token_name] = {
                    'max_gain': float(max_gain),
                    'initial_mc_value': row.get('initial_mc_value', 0),
                    'date': row.get('date', ''),
                    'strategy': row.get('strategy', '')
                }
        
        print(f"� Created gains mapping for {len(token_gains_map)} tokens")
        
        wallet_performance = defaultdict(list)
        deployer_tokens = defaultdict(list)
        holder_tokens = defaultdict(list)
        
        processed_count = 0
        for idx, row in telegram_df.iterrows():
            try:
                signal_text = str(row.get('text', ''))
                date = row.get('date', '')
                
                # Extract token name from signal
                token_name = self._extract_token_name(signal_text)
                if not token_name:
                    continue
                
                # Get gains data for this token
                token_key = token_name.lower().strip()
                gains_data = token_gains_map.get(token_key, {})
                max_gain = gains_data.get('max_gain', 0)
                
                # Skip if no gains data
                if max_gain <= 0:
                    continue
                
                # Extract wallets from signal
                wallets = self.extract_wallet_addresses(signal_text)
                
                # Track deployer performance
                for deployer in wallets['deployers']:
                    deployer_tokens[deployer].append({
                        'token': token_name,
                        'gain': max_gain,
                        'initial_mc': gains_data.get('initial_mc_value', 0),
                        'date': date,
                        'signal_idx': idx,
                        'strategy': gains_data.get('strategy', '')
                    })
                
                # Track holder performance
                for holder in wallets['top_holders']:
                    holder_tokens[holder].append({
                        'token': token_name,
                        'gain': max_gain,
                        'initial_mc': gains_data.get('initial_mc_value', 0),
                        'date': date,
                        'signal_idx': idx,
                        'strategy': gains_data.get('strategy', '')
                    })
                
                processed_count += 1
                if processed_count % 1000 == 0:
                    print(f"  Processed {processed_count} signals...")
                    
            except Exception as e:
                print(f"⚠️ Error processing row {idx}: {e}")
                continue
        
        print(f"✅ Processed {processed_count} signals successfully")
        print(f"📊 Found {len(deployer_tokens)} unique deployers")
        print(f"🐋 Found {len(holder_tokens)} unique top holders")
        
        return deployer_tokens, holder_tokens
    
    def _extract_token_name(self, signal_text: str) -> str:
        """Ištraukia token name iš signalo teksto"""
        import re
        
        # Pattern: 🏖 token_name | symbol |
        pattern = r'🏖\s*([^|]+)\s*\|'
        match = re.search(pattern, signal_text)
        if match:
            return match.group(1).strip()
        
        return ""
    
    def calculate_wallet_stats(self, wallet_data: Dict) -> Dict:
        """Skaičiuoja wallet statistikas"""
        if not wallet_data:
            return {}
            
        gains = [t['gain'] for t in wallet_data]
        
        stats = {
            'total_tokens': len(wallet_data),
            'total_gain': sum(gains),
            'average_gain': np.mean(gains),
            'max_gain': max(gains),
            'min_gain': min(gains),
            'median_gain': np.median(gains),
            'success_rate_2x': len([g for g in gains if g >= 2]) / len(gains),
            'success_rate_5x': len([g for g in gains if g >= 5]) / len(gains),
            'success_rate_10x': len([g for g in gains if g >= 10]) / len(gains),
            'success_rate_100x': len([g for g in gains if g >= 100]) / len(gains),
            'profitable_rate': len([g for g in gains if g > 1]) / len(gains),
            'rug_rate': len([g for g in gains if g < 0.5]) / len(gains),
            'last_activity': max([t.get('date', '') for t in wallet_data]),
            'first_activity': min([t.get('date', '') for t in wallet_data]),
            'tokens': wallet_data
        }
        
        return stats
    
    def create_database(self):
        """Sukuria SQLite duomenų bazę"""
        print("🏗️ Creating wallet intelligence database...")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Deployers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deployers (
                address TEXT PRIMARY KEY,
                total_tokens INTEGER,
                average_gain REAL,
                max_gain REAL,
                success_rate_2x REAL,
                success_rate_5x REAL,
                success_rate_10x REAL,
                success_rate_100x REAL,
                profitable_rate REAL,
                rug_rate REAL,
                reputation_score REAL,
                last_activity TEXT,
                first_activity TEXT,
                raw_data TEXT
            )
        ''')
        
        # Top holders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS top_holders (
                address TEXT PRIMARY KEY,
                total_appearances INTEGER,
                average_gain REAL,
                max_gain REAL,
                success_rate_2x REAL,
                success_rate_5x REAL,
                success_rate_10x REAL,
                success_rate_100x REAL,
                profitable_rate REAL,
                diamond_hands_score REAL,
                last_activity TEXT,
                first_activity TEXT,
                raw_data TEXT
            )
        ''')
        
        # Wallet associations table (deployer + holders in same token)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deployer_address TEXT,
                holder_address TEXT,
                token_name TEXT,
                gain REAL,
                date TEXT,
                signal_idx INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database created successfully")
    
    def build_complete_database(self):
        """Sukuria pilną wallet intelligence duomenų bazę"""
        print("🚀 Building complete wallet intelligence database...")
        
        # 1. Analyze historical data
        deployer_data, holder_data = self.analyze_historical_performance()
        
        # 2. Create database
        self.create_database()
        
        # 3. Calculate stats and save to DB
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        print("💾 Saving deployer data...")
        for deployer_addr, tokens in deployer_data.items():
            stats = self.calculate_wallet_stats(tokens)
            
            # Calculate reputation score (weighted by success and volume)
            reputation = (
                stats['success_rate_5x'] * 0.4 +
                stats['profitable_rate'] * 0.3 +
                (1 - stats['rug_rate']) * 0.2 +
                min(stats['total_tokens'] / 10, 1) * 0.1
            )
            
            cursor.execute('''
                INSERT OR REPLACE INTO deployers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                deployer_addr,
                stats['total_tokens'],
                stats['average_gain'],
                stats['max_gain'],
                stats['success_rate_2x'],
                stats['success_rate_5x'],
                stats['success_rate_10x'],
                stats['success_rate_100x'],
                stats['profitable_rate'],
                stats['rug_rate'],
                reputation,
                stats['last_activity'],
                stats['first_activity'],
                json.dumps(tokens)
            ))
        
        print("🐋 Saving holder data...")
        for holder_addr, tokens in holder_data.items():
            stats = self.calculate_wallet_stats(tokens)
            
            # Calculate diamond hands score
            diamond_score = (
                stats['success_rate_5x'] * 0.5 +
                stats['profitable_rate'] * 0.3 +
                min(stats['total_tokens'] / 20, 1) * 0.2
            )
            
            cursor.execute('''
                INSERT OR REPLACE INTO top_holders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                holder_addr,
                stats['total_tokens'],
                stats['average_gain'],
                stats['max_gain'],
                stats['success_rate_2x'],
                stats['success_rate_5x'],
                stats['success_rate_10x'],
                stats['success_rate_100x'],
                stats['profitable_rate'],
                diamond_score,
                stats['last_activity'],
                stats['first_activity'],
                json.dumps(tokens)
            ))
        
        print("🔗 Saving wallet associations...")
        # Save associations between deployers and holders
        for deployer_addr, deployer_tokens in deployer_data.items():
            for token_data in deployer_tokens:
                for holder_addr, holder_tokens in holder_data.items():
                    for holder_token in holder_tokens:
                        if (holder_token['signal_idx'] == token_data['signal_idx'] and
                            holder_token['token'] == token_data['token']):
                            cursor.execute('''
                                INSERT INTO wallet_associations 
                                (deployer_address, holder_address, token_name, gain, date, signal_idx)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (
                                deployer_addr,
                                holder_addr,
                                token_data['token'],
                                token_data['gain'],
                                token_data['date'],
                                token_data['signal_idx']
                            ))
        
        conn.commit()
        conn.close()
        
        print("✅ Wallet intelligence database created successfully!")
        self.print_database_summary()
    
    def print_database_summary(self):
        """Spausdina duomenų bazės santrauką"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        print("\n" + "="*60)
        print("🏦 WALLET INTELLIGENCE DATABASE SUMMARY")
        print("="*60)
        
        # Deployers summary
        cursor.execute("SELECT COUNT(*), AVG(success_rate_5x), AVG(reputation_score) FROM deployers")
        result = cursor.fetchone()
        dep_count, avg_success, avg_reputation = result if result else (0, 0, 0)
        
        print(f"👤 DEPLOYERS: {dep_count}")
        if dep_count > 0 and avg_success is not None:
            print(f"   Average 5x+ Success Rate: {avg_success:.1%}")
            print(f"   Average Reputation Score: {avg_reputation:.2f}")
        else:
            print("   No deployer data available")
        
        # Top performers
        if dep_count > 0:
            cursor.execute("SELECT address, success_rate_5x, total_tokens FROM deployers ORDER BY success_rate_5x DESC LIMIT 5")
            top_deployers = cursor.fetchall()
            print("\n🏆 TOP 5 DEPLOYERS (5x+ success rate):")
            for addr, success, tokens in top_deployers:
                print(f"   {addr[:20]}... {success:.1%} ({tokens} tokens)")
        
        # Holders summary
        cursor.execute("SELECT COUNT(*), AVG(success_rate_5x), AVG(diamond_hands_score) FROM top_holders")
        result = cursor.fetchone()
        hold_count, avg_hold_success, avg_diamond = result if result else (0, 0, 0)
        
        print(f"\n🐋 TOP HOLDERS: {hold_count}")
        if hold_count > 0 and avg_hold_success is not None:
            print(f"   Average 5x+ Success Rate: {avg_hold_success:.1%}")
            print(f"   Average Diamond Hands Score: {avg_diamond:.2f}")
        else:
            print("   No holder data available")
        
        # Top holders
        if hold_count > 0:
            cursor.execute("SELECT address, success_rate_5x, total_appearances FROM top_holders ORDER BY success_rate_5x DESC LIMIT 5")
            top_holders = cursor.fetchall()
            print("\n💎 TOP 5 HOLDERS (5x+ success rate):")
            for addr, success, appearances in top_holders:
                print(f"   {addr[:20]}... {success:.1%} ({appearances} appearances)")
        
        # Associations
        cursor.execute("SELECT COUNT(*) FROM wallet_associations")
        result = cursor.fetchone()
        assoc_count = result[0] if result else 0
        print(f"\n🔗 WALLET ASSOCIATIONS: {assoc_count}")
        
        conn.close()
        print("="*60)

class WalletIntelligenceLookup:
    """Klases walletų paieškai duomenų bazėje"""
    
    def __init__(self):
        self.db_file = 'wallet_intelligence.db'
    
    def get_deployer_intelligence(self, deployer_address: str) -> Dict:
        """Gauna deployer intelligence iš DB"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM deployers WHERE address = ?", (deployer_address,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'address': result[0],
                'total_tokens': result[1],
                'average_gain': result[2],
                'max_gain': result[3],
                'success_rate_2x': result[4],
                'success_rate_5x': result[5],
                'success_rate_10x': result[6],
                'success_rate_100x': result[7],
                'profitable_rate': result[8],
                'rug_rate': result[9],
                'reputation_score': result[10],
                'last_activity': result[11],
                'first_activity': result[12],
                'intelligence_level': 'HIGH' if result[1] >= 5 else 'MEDIUM' if result[1] >= 2 else 'LOW'
            }
        
        return None
    
    def get_holder_intelligence(self, holder_addresses: List[str]) -> List[Dict]:
        """Gauna holder intelligence iš DB"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        results = []
        for address in holder_addresses:
            cursor.execute("SELECT * FROM top_holders WHERE address = ?", (address,))
            result = cursor.fetchone()
            
            if result:
                results.append({
                    'address': result[0],
                    'total_appearances': result[1],
                    'average_gain': result[2],
                    'max_gain': result[3],
                    'success_rate_2x': result[4],
                    'success_rate_5x': result[5],
                    'success_rate_10x': result[6],
                    'success_rate_100x': result[7],
                    'profitable_rate': result[8],
                    'diamond_hands_score': result[9],
                    'last_activity': result[10],
                    'first_activity': result[11],
                    'intelligence_level': 'HIGH' if result[1] >= 10 else 'MEDIUM' if result[1] >= 3 else 'LOW'
                })
        
        conn.close()
        return results
    
    def calculate_signal_boost(self, deployer_address: str, holder_addresses: List[str]) -> Dict:
        """Skaičiuoja signal boost pagal wallet intelligence"""
        deployer_intel = self.get_deployer_intelligence(deployer_address)
        holder_intel = self.get_holder_intelligence(holder_addresses)
        
        boost_score = 0
        boost_factors = []
        
        # Deployer boost
        if deployer_intel:
            deployer_boost = deployer_intel['success_rate_5x'] * 2 - 1  # Scale to -1 to 1
            boost_score += deployer_boost * 0.6  # 60% weight
            boost_factors.append(f"Deployer: {deployer_boost:+.1%}")
        
        # Holder boost
        if holder_intel:
            avg_holder_success = np.mean([h['success_rate_5x'] for h in holder_intel])
            holder_boost = avg_holder_success * 2 - 1
            boost_score += holder_boost * 0.4  # 40% weight
            boost_factors.append(f"Holders: {holder_boost:+.1%}")
        
        return {
            'boost_score': boost_score,
            'boost_percentage': boost_score * 100,
            'deployer_intelligence': deployer_intel,
            'holder_intelligence': holder_intel,
            'boost_factors': boost_factors,
            'confidence_level': len(boost_factors) / 2  # 0-1 based on available data
        }

if __name__ == "__main__":
    print("🚀 Starting Wallet Intelligence Database Builder...")
    
    builder = WalletDatabaseBuilder()
    builder.build_complete_database()
    
    print("\n🧪 Testing database lookup...")
    lookup = WalletIntelligenceLookup()
    
    # Test with some sample addresses
    print("Testing deployer lookup...")
    # You can test with real addresses from your data

#!/usr/bin/env python3
"""
Telegram Raw Data Parser
Parses raw telegram messages and extracts structured data
"""

import pandas as pd
import re
import json
from datetime import datetime
import numpy as np

class TelegramDataParser:
    def __init__(self):
        self.df = None
        self.parsed_signals = []
        
    def load_raw_data(self):
        """Load raw telegram data"""
        try:
            self.df = pd.read_csv('telegram_chat_0xBot_AI_Agent___Solana_network.csv')
            print(f"✅ Loaded {len(self.df)} raw messages")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def parse_signals(self):
        """Parse signals from raw text"""
        print("\n🔧 PARSING SIGNALS FROM RAW DATA...")
        
        signals = []
        gains_updates = []
        
        for idx, row in self.df.iterrows():
            text = str(row['text'])
            date = row['date']
            
            # Check if it's a signal announcement
            if self.is_signal_announcement(text):
                signal_data = self.extract_signal_data(text, date)
                if signal_data:
                    signals.append(signal_data)
            
            # Check if it's a gains update
            elif self.is_gains_update(text):
                gains_data = self.extract_gains_data(text, date)
                if gains_data:
                    gains_updates.append(gains_data)
        
        print(f"✅ Parsed {len(signals)} signals and {len(gains_updates)} gains updates")
        
        # Merge signals with their gains
        merged_signals = self.merge_signals_with_gains(signals, gains_updates)
        
        self.parsed_signals = merged_signals
        return merged_signals
    
    def is_signal_announcement(self, text):
        """Check if text is a signal announcement"""
        signal_indicators = [
            'Token Address:',
            'Supply:',
            'Initial MC:',
            'LP Tokens:',
            'Top 10 holders:',
            'FREEZE:',
            'MINT:',
            'LP STATUS:'
        ]
        
        return any(indicator in text for indicator in signal_indicators)
    
    def is_gains_update(self, text):
        """Check if text is a gains update"""
        return 'gains 🚀' in text and 'Call MC:' in text and 'Current MC:' in text
    
    def extract_signal_data(self, text, date):
        """Extract structured data from signal text"""
        try:
            signal = {
                'date': date,
                'type': 'signal'
            }
            
            # Extract token name and symbol
            title_match = re.search(r'🏖 (.+?) \| (.+?) \|', text)
            if title_match:
                signal['token_name'] = title_match.group(1).strip()
                signal['token_symbol'] = title_match.group(2).strip()
            
            # Extract token address
            address_match = re.search(r'Token Address:\s*([A-Za-z0-9]+)', text)
            if address_match:
                signal['token_address'] = address_match.group(1)
            
            # Extract financial data
            supply_match = re.search(r'Supply: ([\d.]+[BMK]?) Tokens', text)
            if supply_match:
                signal['supply'] = supply_match.group(1)
            
            initial_mc_match = re.search(r'Initial MC: \$([0-9,.K]+)', text)
            if initial_mc_match:
                signal['initial_mc'] = initial_mc_match.group(1)
            
            call_mc_match = re.search(r'Call MC: \$([0-9,.K]+)', text)
            if call_mc_match:
                signal['call_mc'] = call_mc_match.group(1)
            
            # Extract LP data
            lp_sol_match = re.search(r'Initial LP: ([\d.]+) SOL', text)
            if lp_sol_match:
                signal['initial_lp_sol'] = float(lp_sol_match.group(1))
            
            lp_tokens_match = re.search(r'LP Tokens: (\d+)%', text)
            if lp_tokens_match:
                signal['lp_tokens_percent'] = int(lp_tokens_match.group(1))
            
            # Extract holder data
            holders_match = re.search(r'Top 10 holders:.*?(\d+\.?\d*)%', text)
            if holders_match:
                signal['top_holders_percent'] = float(holders_match.group(1))
            
            # Extract wallet percentages
            wallet_percentages = re.findall(r'(\d+\.?\d*)% \(https://solscan\.io/address/', text)
            signal['wallet_percentages'] = [float(p) for p in wallet_percentages]
            
            # Extract security features
            signal['freeze_disabled'] = '✅ Disabled' in text and 'FREEZE:' in text
            signal['mint_disabled'] = '✅ Disabled' in text and 'MINT:' in text
            signal['lp_burned'] = '✅' in text and 'LP STATUS:' in text and 'Burned' in text
            
            # Extract socials
            signal['has_website'] = 'WEB (' in text
            signal['has_twitter'] = 'X (' in text
            signal['has_telegram'] = 'TG (' in text
            
            # Extract strategy
            strategy_match = re.search(r'Strategy: (.+)', text)
            if strategy_match:
                signal['strategy'] = strategy_match.group(1).strip()
            
            # Extract time features
            dt = pd.to_datetime(date)
            signal['hour_of_day'] = dt.hour
            signal['day_of_week'] = dt.weekday()
            
            return signal
            
        except Exception as e:
            print(f"Error parsing signal: {e}")
            return None
    
    def extract_gains_data(self, text, date):
        """Extract gains data from update text"""
        try:
            gains_data = {
                'date': date,
                'type': 'gains_update'
            }
            
            # Extract token name
            token_match = re.search(r'([A-Za-z0-9$]+) gains 🚀', text)
            if token_match:
                gains_data['token_identifier'] = token_match.group(1)
            
            # Extract gain multiplier
            gain_match = re.search(r'(\d+\.?\d*)x 🚀', text)
            if gain_match:
                gains_data['gain_multiplier'] = float(gain_match.group(1))
            
            # Extract MCs
            call_mc_match = re.search(r'Call MC: \$([0-9,.K]+)', text)
            if call_mc_match:
                gains_data['call_mc'] = call_mc_match.group(1)
            
            current_mc_match = re.search(r'Current MC: \$([0-9,.KM]+)', text)
            if current_mc_match:
                gains_data['current_mc'] = current_mc_match.group(1)
            
            return gains_data
            
        except Exception as e:
            return None
    
    def merge_signals_with_gains(self, signals, gains_updates):
        """Merge signals with their gains updates"""
        print("\n🔗 MERGING SIGNALS WITH GAINS...")
        
        # Convert to DataFrames for easier manipulation
        signals_df = pd.DataFrame(signals)
        gains_df = pd.DataFrame(gains_updates)
        
        if len(gains_df) == 0:
            print("⚠️ No gains data found")
            return signals
        
        # For each signal, find the maximum gain achieved
        for idx, signal in enumerate(signals):
            if 'token_symbol' not in signal:
                continue
                
            token_symbol = signal['token_symbol']
            
            # Find matching gains updates (escape special regex characters)
            token_symbol_escaped = re.escape(token_symbol)
            token_name_escaped = re.escape(signal.get('token_name', ''))
            
            matching_gains = gains_df[
                gains_df['token_identifier'].str.contains(token_symbol_escaped, na=False, regex=True) |
                gains_df['token_identifier'].str.contains(token_name_escaped, na=False, regex=True)
            ]
            
            if len(matching_gains) > 0:
                max_gain = matching_gains['gain_multiplier'].max()
                signals[idx]['max_gain'] = max_gain
                signals[idx]['gains_count'] = len(matching_gains)
            else:
                signals[idx]['max_gain'] = 0
                signals[idx]['gains_count'] = 0
        
        return signals
    
    def analyze_parsed_data(self):
        """Analyze the parsed data"""
        if not self.parsed_signals:
            print("❌ No parsed signals to analyze")
            return
        
        df = pd.DataFrame(self.parsed_signals)
        
        print("\n📊 PARSED DATA ANALYSIS:")
        print(f"Total signals: {len(df)}")
        print(f"Signals with gains: {(df['max_gain'] > 0).sum()}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        
        # Gains analysis
        gains_signals = df[df['max_gain'] > 0]
        if len(gains_signals) > 0:
            print(f"\n💰 GAINS STATISTICS:")
            print(f"Average gain: {gains_signals['max_gain'].mean():.2f}x")
            print(f"Median gain: {gains_signals['max_gain'].median():.2f}x")
            print(f"Max gain: {gains_signals['max_gain'].max():.2f}x")
            print(f"Success rate (≥5x): {(gains_signals['max_gain'] >= 5).mean()*100:.1f}%")
            print(f"Success rate (≥10x): {(gains_signals['max_gain'] >= 10).mean()*100:.1f}%")
        
        # Security features analysis
        print(f"\n🔒 SECURITY FEATURES:")
        print(f"Freeze disabled: {df['freeze_disabled'].mean()*100:.1f}%")
        print(f"Mint disabled: {df['mint_disabled'].mean()*100:.1f}%")
        print(f"LP burned: {df['lp_burned'].mean()*100:.1f}%")
        
        # Social presence
        print(f"\n📱 SOCIAL PRESENCE:")
        print(f"Has website: {df['has_website'].mean()*100:.1f}%")
        print(f"Has Twitter: {df['has_twitter'].mean()*100:.1f}%")
        print(f"Has Telegram: {df['has_telegram'].mean()*100:.1f}%")
        
        # Strategy analysis
        if 'strategy' in df.columns:
            strategy_success = df[df['max_gain'] > 0].groupby('strategy')['max_gain'].agg(['count', 'mean']).round(2)
            print(f"\n📈 STRATEGY PERFORMANCE:")
            print(strategy_success)
        
        return df
    
    def save_parsed_data(self, filename='parsed_telegram_data.csv'):
        """Save parsed data to CSV"""
        if not self.parsed_signals:
            print("❌ No data to save")
            return
        
        df = pd.DataFrame(self.parsed_signals)
        df.to_csv(filename, index=False)
        print(f"✅ Saved parsed data to {filename}")
        
        # Also save as JSON for easier inspection
        with open(filename.replace('.csv', '.json'), 'w') as f:
            json.dump(self.parsed_signals, f, indent=2, default=str)
        
        return df

def main():
    """Main parsing function"""
    print("🚀 TELEGRAM DATA PARSER STARTING...")
    
    parser = TelegramDataParser()
    
    if not parser.load_raw_data():
        return
    
    parsed_signals = parser.parse_signals()
    df = parser.analyze_parsed_data()
    parser.save_parsed_data()
    
    print("\n🎉 PARSING COMPLETE!")
    
    # Show top performing signals
    if len(parsed_signals) > 0:
        df = pd.DataFrame(parsed_signals)
        top_gainers = df[df['max_gain'] > 0].nlargest(10, 'max_gain')
        
        print("\n🏆 TOP 10 PERFORMING SIGNALS:")
        for _, signal in top_gainers.iterrows():
            print(f"  {signal.get('token_name', 'Unknown')} ({signal.get('token_symbol', '')}) - {signal['max_gain']:.2f}x")

if __name__ == "__main__":
    main()

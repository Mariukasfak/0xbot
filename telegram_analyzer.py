#!/usr/bin/env python3
"""
Telegram Coin Calls Analyzer
Išanalizuoja Telegram chat CSV failus ir ištraukia visą svarbią informaciją apie coin'ų signalus
"""

import pandas as pd
import re
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
warnings.filterwarnings('ignore')

# Set style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TelegramCoinAnalyzer:
    def __init__(self):
        # Signalų žodžiai, kuriuos ieškome
        self.signal_keywords = [
            'MC', 'CALL MC', 'MARKET CAP', 'INITIAL MC', 'Call MC',
            'LP', 'LIQUIDITY', 'INITIAL LP', 'Call Liquidity', 'LP STATUS', 'LP TOKENS',
            'SUPPLY', 'TOKENS', 'WALLET', 'HOLDERS', 'Top 10 holders',
            'FREEZE', 'MINT', 'DISABLED', 'ENABLED',
            'DEPLOYER', 'BURNED', 'Not Burned',
            'STRATEGY', 'CALL', 'SIGNAL', 'VIP',
            'AUDIT', 'VERIFIED', 'SAFE', 'RUGCHECK',
            'SOCIALS', 'WEB', 'X', 'TWITTER', 'TELEGRAM',
            'PHOTON', 'BUNDLE', 'SCREEN', 'DEXT', 'BULLX',
            'Pump.Fun', 'pump', 'sol', 'SOL'
        ]
        
        # Regex patternai
        self.patterns = {
            'coin_gains': r'(\w+)\s+gains\s+🚀\s+([0-9]+\.?[0-9]*)x\s+🚀',
            'token_address': r'`([A-Za-z0-9]{40,50})`',
            'wallet_address': r'([A-Za-z0-9]{40,50})',
            'percentage': r'([0-9]+\.?[0-9]*%)',
            'sol_amount': r'([0-9]+\.?[0-9]*)\s+SOL',
            'dollar_amount': r'\$([0-9,]+\.?[0-9]*[KMB]?)',
            'mc_amount': r'MC:\s*\$([0-9,]+\.?[0-9]*[KMB]?)',
            'supply_amount': r'Supply:\s*([0-9,]+\.?[0-9]*[KMB]?)\s*Tokens',
            'web_link': r'https?://[^\s\]]+',
            'telegram_link': r'@\w+|t\.me/\w+'
        }
    
    def load_csv(self, file_path):
        """Užkrauna CSV failą"""
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Užkrautas CSV failas: {len(df)} eilučių")
            return df
        except Exception as e:
            print(f"❌ Klaida užkraunant failą: {e}")
            return None
    
    def extract_coin_gains(self, text):
        """Ištraukia coin pavadinimą ir gain multiplier"""
        if pd.isna(text):
            return None, None
        
        match = re.search(self.patterns['coin_gains'], text)
        if match:
            coin_name = match.group(1)
            gain_x = float(match.group(2))
            return coin_name, gain_x
        return None, None
    
    def extract_token_address(self, text):
        """Ištraukia token adresą"""
        if pd.isna(text):
            return None
        
        match = re.search(self.patterns['token_address'], text)
        return match.group(1) if match else None
    
    def extract_wallets_and_percentages(self, text):
        """Ištraukia wallet adresus ir jų procentus"""
        if pd.isna(text):
            return []
        
        wallets = []
        # Ieškome wallet adresų su procentais
        wallet_pattern = r'\[([0-9]+\.?[0-9]*%)\](https://solscan\.io/address/([A-Za-z0-9]{40,50}))'
        matches = re.findall(wallet_pattern, text)
        
        for percentage, wallet in matches:
            wallets.append({
                'wallet': wallet,
                'percentage': percentage,
                'percentage_float': float(percentage.replace('%', ''))
            })
        
        return wallets
    
    def extract_financial_data(self, text):
        """Ištraukia finansinius duomenis"""
        if pd.isna(text):
            return {}
        
        data = {}
        
        # Market Cap
        mc_match = re.search(r'(?:Initial MC|Call MC):\s*\$([0-9,]+\.?[0-9]*[KMB]?)', text)
        if mc_match:
            data['market_cap'] = mc_match.group(1)
        
        # Supply
        supply_match = re.search(r'Supply:\s*([0-9,]+\.?[0-9]*[KMB]?)\s*Tokens', text)
        if supply_match:
            data['supply'] = supply_match.group(1)
        
        # LP Amount
        lp_match = re.search(r'(?:Initial LP|Call Liquidity):\s*([0-9]+\.?[0-9]*)\s*SOL', text)
        if lp_match:
            data['lp_sol'] = float(lp_match.group(1))
        
        # LP Tokens percentage
        lp_tokens_match = re.search(r'LP Tokens:\s*([0-9]+\.?[0-9]*)%', text)
        if lp_tokens_match:
            data['lp_tokens_percent'] = float(lp_tokens_match.group(1))
        
        # Top holders percentage
        holders_match = re.search(r'Top 10 holders.*?([0-9]+\.?[0-9]*)%', text)
        if holders_match:
            data['top_holders_percent'] = float(holders_match.group(1))
        
        return data
    
    def extract_security_features(self, text):
        """Ištraukia saugumo funkcijas"""
        if pd.isna(text):
            return {}
        
        features = {}
        
        # Freeze status
        if 'FREEZE:' in text:
            features['freeze_disabled'] = '✅ Disabled' in text
        
        # Mint status
        if 'MINT:' in text:
            features['mint_disabled'] = '✅ Disabled' in text
        
        # LP Burned
        if 'LP STATUS:' in text:
            features['lp_burned'] = '✅ Burned' in text or 'Not Burned' not in text
        
        return features
    
    def extract_links(self, text):
        """Ištraukia nuorodas"""
        if pd.isna(text):
            return {}
        
        links = {}
        
        # Web links
        web_links = re.findall(self.patterns['web_link'], text)
        links['web_links'] = len(web_links)
        links['has_web'] = len(web_links) > 0
        
        # Telegram links
        tg_links = re.findall(self.patterns['telegram_link'], text)
        links['tg_links'] = len(tg_links)
        links['has_telegram'] = len(tg_links) > 0
        
        # Specific platforms
        links['has_dexscreener'] = 'dexscreener.com' in text
        links['has_photon'] = 'photon-sol' in text
        links['has_rugcheck'] = 'rugcheck.xyz' in text
        links['has_dextools'] = 'dextools.io' in text
        links['has_bullx'] = 'bullx.io' in text
        
        return links
    
    def count_signal_keywords(self, text):
        """Suskaičiuoja signalų žodžius"""
        if pd.isna(text):
            return {}
        
        text_upper = text.upper()
        signal_counts = {}
        
        for keyword in self.signal_keywords:
            count = text_upper.count(keyword.upper())
            if count > 0:
                signal_counts[keyword] = count
        
        return signal_counts
    
    def analyze_csv(self, file_path):
        """Pagrindinė analizės funkcija"""
        df = self.load_csv(file_path)
        if df is None:
            return None, None
        
        print("🔍 Pradedama analizė...")
        
        # Rezultatų saugojimas
        coin_data = defaultdict(lambda: {
            'messages': [],
            'gains': [],
            'max_gain': 0,
            'token_addresses': set(),
            'wallets': [],
            'financial_data': {},
            'security_features': {},
            'links': {},
            'signal_keywords': Counter(),
            'first_seen': None,
            'last_seen': None
        })
        
        all_wallets = []
        
        # Analizuojame kiekvieną eilutę
        for idx, row in df.iterrows():
            text = row.get('text', '')
            date = row.get('date', '')
            
            if pd.isna(text):
                continue
            
            # Ištraukiame coin gains
            coin_name, gain_x = self.extract_coin_gains(text)
            
            if coin_name and gain_x:
                # Coin'as su gain'u
                coin_data[coin_name]['gains'].append(gain_x)
                coin_data[coin_name]['max_gain'] = max(coin_data[coin_name]['max_gain'], gain_x)
                coin_data[coin_name]['messages'].append(text)
                
                # Datos
                if not coin_data[coin_name]['first_seen']:
                    coin_data[coin_name]['first_seen'] = date
                coin_data[coin_name]['last_seen'] = date
                
                print(f"🚀 {coin_name}: {gain_x}x gain")
            
            # Ieškome token adresų ir kitos informacijos visose žinutėse
            token_addr = self.extract_token_address(text)
            if token_addr:
                # Bandome susieti su coin'u pagal artumo principą
                for coin in coin_data.keys():
                    if coin.lower() in text.lower() or any(coin.lower() in msg.lower() for msg in coin_data[coin]['messages'][-5:]):
                        coin_data[coin]['token_addresses'].add(token_addr)
                        break
            
            # Wallet'ai ir procentai
            wallets = self.extract_wallets_and_percentages(text)
            for wallet_info in wallets:
                wallet_info['message_text'] = text[:200] + "..." if len(text) > 200 else text
                wallet_info['date'] = date
                
                # Bandome susieti su coin'u
                for coin in coin_data.keys():
                    if coin.lower() in text.lower():
                        wallet_info['coin'] = coin
                        coin_data[coin]['wallets'].append(wallet_info)
                        break
                
                all_wallets.append(wallet_info)
            
            # Finansiniai duomenys
            financial_data = self.extract_financial_data(text)
            if financial_data:
                for coin in coin_data.keys():
                    if coin.lower() in text.lower():
                        coin_data[coin]['financial_data'].update(financial_data)
                        break
            
            # Saugumo funkcijos
            security_features = self.extract_security_features(text)
            if security_features:
                for coin in coin_data.keys():
                    if coin.lower() in text.lower():
                        coin_data[coin]['security_features'].update(security_features)
                        break
            
            # Nuorodos
            links = self.extract_links(text)
            if any(links.values()):
                for coin in coin_data.keys():
                    if coin.lower() in text.lower():
                        for key, value in links.items():
                            coin_data[coin]['links'][key] = coin_data[coin]['links'].get(key, 0) + value
                        break
            
            # Signal keywords
            signals = self.count_signal_keywords(text)
            if signals:
                for coin in coin_data.keys():
                    if coin.lower() in text.lower():
                        coin_data[coin]['signal_keywords'].update(signals)
                        break
        
        print(f"✅ Analizė baigta! Rasta {len(coin_data)} coin'ų")
        
        return coin_data, all_wallets
    
    def create_features_dataframe(self, coin_data):
        """Sukuria features DataFrame"""
        features_list = []
        
        for coin_name, data in coin_data.items():
            feature_row = {
                'coin_name': coin_name,
                'message_count': len(data['messages']),
                'gain_count': len(data['gains']),
                'max_gain': data['max_gain'],
                'avg_gain': sum(data['gains']) / len(data['gains']) if data['gains'] else 0,
                'total_gain_volume': sum(data['gains']),
                'unique_wallets': len(data['wallets']),
                'token_addresses': ', '.join(data['token_addresses']),
                'first_seen': data['first_seen'],
                'last_seen': data['last_seen']
            }
            
            # Finansiniai duomenys
            financial = data['financial_data']
            feature_row.update({
                'market_cap': financial.get('market_cap', ''),
                'supply': financial.get('supply', ''),
                'lp_sol': financial.get('lp_sol', 0),
                'lp_tokens_percent': financial.get('lp_tokens_percent', 0),
                'top_holders_percent': financial.get('top_holders_percent', 0)
            })
            
            # Saugumo funkcijos
            security = data['security_features']
            feature_row.update({
                'freeze_disabled': security.get('freeze_disabled', False),
                'mint_disabled': security.get('mint_disabled', False),
                'lp_burned': security.get('lp_burned', False)
            })
            
            # Nuorodos
            links = data['links']
            feature_row.update({
                'has_web': links.get('has_web', False),
                'has_telegram': links.get('has_telegram', False),
                'has_dexscreener': links.get('has_dexscreener', False),
                'has_photon': links.get('has_photon', False),
                'has_rugcheck': links.get('has_rugcheck', False),
                'has_dextools': links.get('has_dextools', False),
                'has_bullx': links.get('has_bullx', False),
                'total_links': sum(links.values())
            })
            
            # Signal keywords
            signals = data['signal_keywords']
            feature_row['signal_keywords'] = ', '.join([f"{k}:{v}" for k, v in signals.items()])
            feature_row['total_signals'] = sum(signals.values())
            feature_row['unique_signals'] = len(signals)
            
            # Wallet statistikos
            if data['wallets']:
                wallet_percentages = [w['percentage_float'] for w in data['wallets']]
                feature_row.update({
                    'max_wallet_percent': max(wallet_percentages),
                    'avg_wallet_percent': sum(wallet_percentages) / len(wallet_percentages),
                    'total_wallet_percent': sum(wallet_percentages)
                })
            else:
                feature_row.update({
                    'max_wallet_percent': 0,
                    'avg_wallet_percent': 0,
                    'total_wallet_percent': 0
                })
            
            # Success score (paprastas algoritmas)
            success_score = 0
            success_score += data['max_gain'] * 10  # Max gain svoris
            success_score += len(data['gains']) * 5  # Gain frequency
            success_score += int(security.get('freeze_disabled', False)) * 20
            success_score += int(security.get('mint_disabled', False)) * 20
            success_score += int(security.get('lp_burned', False)) * 30
            success_score += sum(links.values()) * 5  # Links count
            success_score += sum(signals.values()) * 2  # Signals count
            
            feature_row['success_score'] = success_score
            
            features_list.append(feature_row)
        
        return pd.DataFrame(features_list)
    
    def create_wallets_dataframe(self, all_wallets):
        """Sukuria wallets DataFrame"""
        wallets_df = pd.DataFrame(all_wallets)
        
        if not wallets_df.empty:
            # Pridedame papildomą statistiką
            wallet_stats = wallets_df.groupby('wallet').agg({
                'percentage_float': ['count', 'mean', 'max', 'sum'],
                'coin': lambda x: ', '.join(x.dropna().unique()) if x.dropna().any() else 'Unknown'
            }).round(2)
            
            wallet_stats.columns = ['appearance_count', 'avg_percentage', 'max_percentage', 'total_percentage', 'coins']
            wallet_stats = wallet_stats.reset_index()
            
            # Merginam su originaliais duomenimis
            wallets_df = wallets_df.merge(wallet_stats, on='wallet', how='left')
        
        return wallets_df
    
    def generate_insights(self, features_df, wallets_df):
        """Generuoja insights ir rekomendacijas"""
        insights = {
            'top_performers': [],
            'success_patterns': {},
            'whale_wallets': [],
            'security_analysis': {},
            'recommendations': []
        }
        
        if not features_df.empty:
            # Top performers
            top_coins = features_df.nlargest(10, 'max_gain')[['coin_name', 'max_gain', 'success_score']].to_dict('records')
            insights['top_performers'] = top_coins
            
            # Success patterns
            high_performers = features_df[features_df['max_gain'] >= 5]  # 5x ir daugiau
            if not high_performers.empty:
                insights['success_patterns'] = {
                    'avg_signals': high_performers['total_signals'].mean(),
                    'freeze_disabled_rate': high_performers['freeze_disabled'].mean() * 100,
                    'mint_disabled_rate': high_performers['mint_disabled'].mean() * 100,
                    'lp_burned_rate': high_performers['lp_burned'].mean() * 100,
                    'avg_links': high_performers['total_links'].mean(),
                    'avg_wallet_concentration': high_performers['max_wallet_percent'].mean()
                }
            
            # Security analysis
            insights['security_analysis'] = {
                'freeze_disabled_coins': features_df['freeze_disabled'].sum(),
                'mint_disabled_coins': features_df['mint_disabled'].sum(),
                'lp_burned_coins': features_df['lp_burned'].sum(),
                'total_coins': len(features_df)
            }
        
        if not wallets_df.empty:
            # Whale wallets (appearing in multiple coins)
            whale_wallets = wallets_df[wallets_df['appearance_count'] > 1].nlargest(10, 'total_percentage')
            insights['whale_wallets'] = whale_wallets[['wallet', 'appearance_count', 'total_percentage', 'coins']].to_dict('records')
        
        # Recommendations
        insights['recommendations'] = [
            "🎯 Ieškokite coin'ų su freeze ir mint disabled",
            "🔥 LP burned statusas yra labai svarbus saugumo ženklas",
            "👥 Stebėkite wallet'us, kurie kartojasi keliuose projektuose",
            "📊 Coin'ai su daugiau signalų dažniau yra sėkmingi",
            "🔗 Projektai su daugiau nuorodų (dexscreener, rugcheck) yra patikimesni",
            "📈 Coin'ai su max gain >5x dažniau turi gerus saugumo rodiklius",
        ]
        
        return insights

    def plot_gain_distribution(self, features_df):
        """Pavaizduoja gain'ų pasiskirstymą"""
        plt.figure(figsize=(10, 6))
        sns.histplot(features_df['max_gain'], bins=30, kde=True)
        plt.title('Coin\'ų Gain Pasiskirstymas')
        plt.xlabel('Max Gain')
        plt.ylabel('Dažnis')
        plt.grid(True)
        plt.show()
    
    def plot_top_coins(self, features_df, n=10):
        """Pavaizduoja top n coin'ų max gain"""
        top_coins = features_df.nlargest(n, 'max_gain')
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x='max_gain', y='coin_name', data=top_coins, palette='viridis')
        plt.title(f'Top {n} Coin\'ų su Didžiausiu Max Gain')
        plt.xlabel('Max Gain')
        plt.ylabel('Coin\'ų Pavadinimai')
        plt.grid(True)
        plt.show()
    
    def plot_signal_keyword_trends(self, features_df, keyword):
        """Pavaizduoja signalų žodžių tendencijas laikui bėgant"""
        keyword = keyword.upper()
        filtered_df = features_df[features_df['signal_keywords'].str.contains(keyword, na=False)]
        
        if filtered_df.empty:
            print(f"Nerasta jokių signalų žodžių, atitinkančių: {keyword}")
            return
        
        # Laiko analizė
        filtered_df['first_seen'] = pd.to_datetime(filtered_df['first_seen'])
        time_series = filtered_df.set_index('first_seen').resample('W').count()['coin_name']
        
        plt.figure(figsize=(14, 7))
        time_series.plot(marker='o')
        plt.title(f'Signalų Žodžio "{keyword}" Tendencija Laikui Bėgant')
        plt.xlabel('Data')
        plt.ylabel('Coin\'ų Skaičius su Signalų Žodžiu')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        plt.show()
    
    def plot_wallet_concentration(self, features_df):
        """Pavaizduoja wallet'ų koncentraciją pagal coin'us"""
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='max_wallet_percent', data=features_df)
        plt.title('Wallet\'ų Koncentracija Pagal Coin\'us')
        plt.xlabel('Maksimalus Wallet\'o Procentas')
        plt.grid(True)
        plt.show()
    
    def plot_security_feature_correlation(self, features_df):
        """Pavaizduoja koreliaciją tarp saugumo funkcijų ir sėkmės rodiklių"""
        security_features = ['freeze_disabled', 'mint_disabled', 'lp_burned']
        correlation_data = features_df[['success_score'] + security_features]
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_data.corr(), annot=True, cmap='coolwarm')
        plt.title('Saugumo Funkcijų ir Sėkmės Rodiklių Koreliacija')
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        plt.grid(True)
        plt.show()
    
    def analyze_time_based_trends(self, df):
        """Atlieka laiko analizę ir pavaizduoja rezultatus"""
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.sort_values('date')
        
        # Signalų žodžių tendencijos
        signal_trends = {}
        for keyword in self.signal_keywords:
            keyword = keyword.upper()
            filtered_df = df[df['text'].str.contains(keyword, na=False, case=False)]
            
            if not filtered_df.empty:
                # Laiko analizė
                filtered_df['date'] = pd.to_datetime(filtered_df['date'])
                time_series = filtered_df.set_index('date').resample('W').count()['text']
                
                signal_trends[keyword] = time_series
        
        # Pavaizduojame tendencijas
        plt.figure(figsize=(14, 10))
        for keyword, time_series in signal_trends.items():
            plt.plot(time_series, label=keyword)
        
        plt.title('Signalų Žodžių Tendencijos Laikui Bėgant')
        plt.xlabel('Data')
        plt.ylabel('Žinučių Skaičius su Signalų Žodžiu')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def plot_top_wallets_time_series(self, all_wallets, top_n=10):
        """Pavaizduoja top wallet'ų laiką serijose"""
        wallets_df = pd.DataFrame(all_wallets)
        top_wallets = wallets_df.groupby('wallet').agg({'percentage_float': 'sum'}).nlargest(top_n, 'percentage_float').index
        
        plt.figure(figsize=(14, 7))
        for wallet in top_wallets:
            wallet_data = wallets_df[wallets_df['wallet'] == wallet]
            plt.plot(wallet_data['date'], wallet_data['percentage_float'], marker='o', label=wallet[:10] + '...')
        
        plt.title(f'Top {top_n} Wallet\'ų Laiko Serijos')
        plt.xlabel('Data')
        plt.ylabel('Procentinė Dalies Vertė')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def create_visualizations(self, features_df, wallets_df, coin_data):
        """Sukuria duomenų vizualizacijas"""
        print("\n📊 Kuriame vizualizacijas...")
        
        # Create output directory for plots
        import os
        os.makedirs('/workspaces/0xbot/plots', exist_ok=True)
        
        # 1. Top 15 coin gains bar chart
        plt.figure(figsize=(15, 8))
        top_coins = features_df.nlargest(15, 'max_gain')
        bars = plt.bar(range(len(top_coins)), top_coins['max_gain'], 
                      color=plt.cm.viridis(np.linspace(0, 1, len(top_coins))))
        plt.title('🚀 Top 15 Coins by Maximum Gain', fontsize=16, fontweight='bold')
        plt.xlabel('Coin', fontsize=12)
        plt.ylabel('Maximum Gain (x)', fontsize=12)
        plt.xticks(range(len(top_coins)), top_coins['coin_name'], rotation=45, ha='right')
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, top_coins['max_gain'])):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.1f}x', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/workspaces/0xbot/plots/top_coins_gains.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Gain distribution histogram
        plt.figure(figsize=(12, 6))
        all_gains = []
        for coin_name, data in coin_data.items():
            all_gains.extend(data['gains'])
        
        plt.hist(all_gains, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('📈 Distribution of All Gain Multipliers', fontsize=16, fontweight='bold')
        plt.xlabel('Gain Multiplier (x)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.axvline(np.mean(all_gains), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(all_gains):.1f}x')
        plt.axvline(np.median(all_gains), color='orange', linestyle='--', 
                   label=f'Median: {np.median(all_gains):.1f}x')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('/workspaces/0xbot/plots/gain_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Success score vs Max gain scatter plot
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(features_df['max_gain'], features_df['success_score'], 
                            c=features_df['total_signals'], cmap='viridis', 
                            alpha=0.7, s=60)
        plt.colorbar(scatter, label='Total Signals')
        plt.title('🎯 Success Score vs Maximum Gain', fontsize=16, fontweight='bold')
        plt.xlabel('Maximum Gain (x)', fontsize=12)
        plt.ylabel('Success Score', fontsize=12)
        
        # Add trend line
        z = np.polyfit(features_df['max_gain'], features_df['success_score'], 1)
        p = np.poly1d(z)
        plt.plot(features_df['max_gain'], p(features_df['max_gain']), "r--", alpha=0.8)
        
        # Annotate top performers
        top_5 = features_df.nlargest(5, 'max_gain')
        for _, row in top_5.iterrows():
            plt.annotate(row['coin_name'], 
                        (row['max_gain'], row['success_score']),
                        xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, alpha=0.8)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('/workspaces/0xbot/plots/success_vs_gain.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Security features analysis
        plt.figure(figsize=(12, 6))
        security_features = ['freeze_disabled', 'mint_disabled', 'lp_burned']
        security_counts = [features_df[feature].sum() for feature in security_features]
        security_labels = ['Freeze Disabled', 'Mint Disabled', 'LP Burned']
        
        bars = plt.bar(security_labels, security_counts, 
                      color=['#2E8B57', '#4169E1', '#DC143C'], alpha=0.8)
        plt.title('🔒 Security Features Distribution', fontsize=16, fontweight='bold')
        plt.ylabel('Number of Coins', fontsize=12)
        
        # Add percentage labels
        total_coins = len(features_df)
        for bar, count in zip(bars, security_counts):
            percentage = (count/total_coins)*100
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{count}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/workspaces/0xbot/plots/security_features.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Correlation heatmap
        plt.figure(figsize=(14, 10))
        numeric_columns = ['max_gain', 'avg_gain', 'total_gain_volume', 'message_count', 
                          'gain_count', 'unique_wallets', 'lp_sol', 'lp_tokens_percent',
                          'top_holders_percent', 'total_links', 'total_signals', 'success_score']
        
        correlation_data = features_df[numeric_columns].corr()
        
        mask = np.triu(np.ones_like(correlation_data, dtype=bool))
        sns.heatmap(correlation_data, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('🔗 Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('/workspaces/0xbot/plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 6. Wallet concentration analysis
        if not wallets_df.empty:
            plt.figure(figsize=(12, 8))
            whale_wallets = wallets_df[wallets_df['appearance_count'] > 1]
            if not whale_wallets.empty:
                plt.scatter(whale_wallets['appearance_count'], whale_wallets['max_percentage'],
                           s=whale_wallets['total_percentage']*2, alpha=0.6, c='coral')
                plt.title('🐋 Whale Wallet Analysis', fontsize=16, fontweight='bold')
                plt.xlabel('Number of Coins Appeared In', fontsize=12)
                plt.ylabel('Maximum Percentage Hold', fontsize=12)
                plt.grid(True, alpha=0.3)
                
                # Annotate top whales
                top_whales = whale_wallets.nlargest(3, 'total_percentage')
                for _, row in top_whales.iterrows():
                    plt.annotate(f"{row['wallet'][:8]}...", 
                               (row['appearance_count'], row['max_percentage']),
                               xytext=(5, 5), textcoords='offset points', 
                               fontsize=8, alpha=0.8)
                
                plt.tight_layout()
                plt.savefig('/workspaces/0xbot/plots/whale_analysis.png', dpi=300, bbox_inches='tight')
                plt.close()
        
        # 7. Signal keywords word cloud style analysis
        plt.figure(figsize=(15, 8))
        all_signals = Counter()
        for coin_name, data in coin_data.items():
            all_signals.update(data['signal_keywords'])
        
        if all_signals:
            top_signals = dict(all_signals.most_common(20))
            signal_names = list(top_signals.keys())
            signal_counts = list(top_signals.values())
            
            bars = plt.barh(range(len(signal_names)), signal_counts, 
                           color=plt.cm.plasma(np.linspace(0, 1, len(signal_names))))
            plt.title('📡 Most Common Signal Keywords', fontsize=16, fontweight='bold')
            plt.xlabel('Frequency', fontsize=12)
            plt.yticks(range(len(signal_names)), signal_names)
            
            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, signal_counts)):
                plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                        str(value), va='center', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig('/workspaces/0xbot/plots/signal_keywords.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print("✅ Vizualizacijos išsaugotos /workspaces/0xbot/plots/ kataloge")

    def analyze_time_patterns(self, features_df, coin_data):
        """Analizuoja laiko šablonus"""
        print("\n⏰ Analizuojame laiko šablonus...")
        
        time_analysis = {
            'daily_patterns': {},
            'hourly_patterns': {},
            'performance_by_time': {},
            'time_based_insights': []
        }
        
        # Convert dates and analyze
        time_data = []
        for coin_name, data in coin_data.items():
            if data['first_seen'] and data['gains']:
                try:
                    # Parse different date formats
                    date_str = data['first_seen']
                    if 'T' in date_str:
                        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    
                    time_data.append({
                        'coin': coin_name,
                        'datetime': dt,
                        'day_of_week': dt.strftime('%A'),
                        'hour': dt.hour,
                        'max_gain': data['max_gain'],
                        'avg_gain': sum(data['gains']) / len(data['gains']),
                        'gain_count': len(data['gains'])
                    })
                except Exception as e:
                    continue
        
        if time_data:
            time_df = pd.DataFrame(time_data)
            
            # Daily patterns
            daily_stats = time_df.groupby('day_of_week').agg({
                'max_gain': ['mean', 'max', 'count'],
                'avg_gain': 'mean'
            }).round(2)
            
            # Hourly patterns
            hourly_stats = time_df.groupby('hour').agg({
                'max_gain': ['mean', 'max', 'count'],
                'avg_gain': 'mean'
            }).round(2)
            
            time_analysis['daily_patterns'] = daily_stats.to_dict()
            time_analysis['hourly_patterns'] = hourly_stats.to_dict()
            
            # Create time-based visualizations
            plt.figure(figsize=(15, 10))
            
            # Daily patterns subplot
            plt.subplot(2, 2, 1)
            daily_avg = time_df.groupby('day_of_week')['max_gain'].mean()
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_avg = daily_avg.reindex(days_order, fill_value=0)
            
            bars = plt.bar(daily_avg.index, daily_avg.values, color='lightblue', alpha=0.8)
            plt.title('📅 Average Max Gain by Day of Week', fontsize=12, fontweight='bold')
            plt.ylabel('Average Max Gain (x)')
            plt.xticks(rotation=45)
            
            # Hourly patterns subplot
            plt.subplot(2, 2, 2)
            hourly_avg = time_df.groupby('hour')['max_gain'].mean()
            plt.plot(hourly_avg.index, hourly_avg.values, marker='o', linewidth=2, markersize=6)
            plt.title('🕐 Average Max Gain by Hour', fontsize=12, fontweight='bold')
            plt.xlabel('Hour of Day')
            plt.ylabel('Average Max Gain (x)')
            plt.grid(True, alpha=0.3)
            
            # Coin count by day
            plt.subplot(2, 2, 3)
            daily_count = time_df.groupby('day_of_week').size().reindex(days_order, fill_value=0)
            plt.bar(daily_count.index, daily_count.values, color='lightcoral', alpha=0.8)
            plt.title('📊 Number of Signals by Day', fontsize=12, fontweight='bold')
            plt.ylabel('Signal Count')
            plt.xticks(rotation=45)
            
            # Coin count by hour
            plt.subplot(2, 2, 4)
            hourly_count = time_df.groupby('hour').size()
            plt.bar(hourly_count.index, hourly_count.values, color='lightgreen', alpha=0.8)
            plt.title('📊 Number of Signals by Hour', fontsize=12, fontweight='bold')
            plt.xlabel('Hour of Day')
            plt.ylabel('Signal Count')
            
            plt.tight_layout()
            plt.savefig('/workspaces/0xbot/plots/time_patterns.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Generate time-based insights
            best_day = daily_avg.idxmax()
            best_hour = hourly_avg.idxmax()
            most_active_day = daily_count.idxmax()
            most_active_hour = hourly_count.idxmax()
            
            time_analysis['time_based_insights'] = [
                f"🏆 Best performing day: {best_day} (avg {daily_avg[best_day]:.1f}x gain)",
                f"🕐 Best performing hour: {best_hour}:00 (avg {hourly_avg[best_hour]:.1f}x gain)",
                f"📈 Most active day: {most_active_day} ({daily_count[most_active_day]} signals)",
                f"⏰ Most active hour: {most_active_hour}:00 ({hourly_count[most_active_hour]} signals)"
            ]
        
        return time_analysis

    def generate_comprehensive_report(self, features_df, wallets_df, coin_data, insights, time_analysis):
        """Generuoja išsamų ataskaitos failą"""
        print("\n📋 Generuojame išsamų ataskaitą...")
        
        report = []
        report.append("# 🤖 TELEGRAM COIN CALLS COMPREHENSIVE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("## 📊 EXECUTIVE SUMMARY")
        report.append("-" * 30)
        total_coins = len(features_df)
        total_gains = sum(len(data['gains']) for data in coin_data.values())
        avg_gain = np.mean([gain for data in coin_data.values() for gain in data['gains']])
        max_gain = features_df['max_gain'].max()
        
        report.append(f"• Total unique coins analyzed: **{total_coins}**")
        report.append(f"• Total gain signals detected: **{total_gains}**")
        report.append(f"• Average gain multiplier: **{avg_gain:.2f}x**")
        report.append(f"• Maximum gain achieved: **{max_gain:.2f}x**")
        report.append(f"• Total whale wallets identified: **{len(wallets_df[wallets_df['appearance_count'] > 1]) if not wallets_df.empty else 0}**")
        report.append("")
        
        # Top Performers
        report.append("## 🚀 TOP PERFORMING COINS")
        report.append("-" * 30)
        top_10 = features_df.nlargest(10, 'max_gain')
        for i, (_, coin) in enumerate(top_10.iterrows(), 1):
            report.append(f"{i:2d}. **{coin['coin_name']}** - {coin['max_gain']:.2f}x max gain, {coin['gain_count']} signals, Score: {coin['success_score']:.0f}")
        report.append("")
        
        # Success Patterns
        if insights['success_patterns']:
            report.append("## 📈 SUCCESS PATTERNS (5x+ performers)")
            report.append("-" * 30)
            patterns = insights['success_patterns']
            report.append(f"• Average signals per successful coin: **{patterns['avg_signals']:.1f}**")
            report.append(f"• Freeze disabled rate: **{patterns['freeze_disabled_rate']:.1f}%**")
            report.append(f"• Mint disabled rate: **{patterns['mint_disabled_rate']:.1f}%**")
            report.append(f"• LP burned rate: **{patterns['lp_burned_rate']:.1f}%**")
            report.append(f"• Average links per coin: **{patterns['avg_links']:.1f}**")
            report.append(f"• Average max wallet concentration: **{patterns['avg_wallet_concentration']:.1f}%**")
            report.append("")
        
        # Security Analysis
        security = insights['security_analysis']
        report.append("## 🔒 SECURITY ANALYSIS")
        report.append("-" * 30)
        report.append(f"• Coins with freeze disabled: **{security['freeze_disabled_coins']}/{security['total_coins']} ({(security['freeze_disabled_coins']/security['total_coins']*100):.1f}%)**")
        report.append(f"• Coins with mint disabled: **{security['mint_disabled_coins']}/{security['total_coins']} ({(security['mint_disabled_coins']/security['total_coins']*100):.1f}%)**")
        report.append(f"• Coins with LP burned: **{security['lp_burned_coins']}/{security['total_coins']} ({(security['lp_burned_coins']/security['total_coins']*100):.1f}%)**")
        report.append("")
        
        # Time Analysis
        if time_analysis['time_based_insights']:
            report.append("## ⏰ TIME-BASED ANALYSIS")
            report.append("-" * 30)
            for insight in time_analysis['time_based_insights']:
                report.append(f"• {insight}")
            report.append("")
        
        # Whale Analysis
        if insights['whale_wallets']:
            report.append("## 🐋 TOP WHALE WALLETS")
            report.append("-" * 30)
            for i, whale in enumerate(insights['whale_wallets'][:10], 1):
                report.append(f"{i:2d}. **{whale['wallet'][:20]}...** - {whale['appearance_count']} coins, {whale['total_percentage']:.1f}% total hold")
            report.append("")
        
        # Statistical Insights
        report.append("## 📊 STATISTICAL INSIGHTS")
        report.append("-" * 30)
        gains_data = [gain for data in coin_data.values() for gain in data['gains']]
        report.append(f"• Median gain: **{np.median(gains_data):.2f}x**")
        report.append(f"• 75th percentile gain: **{np.percentile(gains_data, 75):.2f}x**")
        report.append(f"• 90th percentile gain: **{np.percentile(gains_data, 90):.2f}x**")
        report.append(f"• Standard deviation: **{np.std(gains_data):.2f}**")
        report.append("")
        
        # Recommendations
        report.append("## 💡 STRATEGIC RECOMMENDATIONS")
        report.append("-" * 30)
        for rec in insights['recommendations']:
            report.append(f"• {rec}")
        report.append("")
        
        # Risk Factors
        report.append("## ⚠️ RISK FACTORS TO CONSIDER")
        report.append("-" * 30)
        risky_coins = features_df[
            (features_df['freeze_disabled'] == False) | 
            (features_df['mint_disabled'] == False) | 
            (features_df['lp_burned'] == False)
        ]
        report.append(f"• **{len(risky_coins)} coins ({(len(risky_coins)/len(features_df)*100):.1f}%)** have security concerns")
        
        high_concentration = features_df[features_df['max_wallet_percent'] > 20]
        report.append(f"• **{len(high_concentration)} coins** have high wallet concentration (>20%)")
        
        report.append("")
        
        # Files Generated
        report.append("## 📁 GENERATED FILES")
        report.append("-" * 30)
        report.append("• `coin_features_analysis.csv` - Detailed coin analysis")
        report.append("• `wallets_analysis.csv` - Wallet analysis")
        report.append("• `analysis_insights.json` - Machine-readable insights")
        report.append("• `plots/` - Data visualizations")
        report.append("• `comprehensive_report.md` - This report")
        report.append("")
        
        # Footer
        report.append("---")
        report.append("*Report generated by Telegram Coin Calls Analyzer*")
        report.append("*Use this analysis for educational purposes only. Always DYOR.*")
        
        # Save report
        with open('/workspaces/0xbot/comprehensive_report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("✅ Išsami ataskaita išsaugota: comprehensive_report.md")

    def export_to_excel(self, features_df, wallets_df, insights):
        """Eksportuoja duomenis į Excel failą"""
        print("\n📄 Eksportuojame duomenis į Excel...")
        
        try:
            with pd.ExcelWriter('/workspaces/0xbot/telegram_analysis_complete.xlsx', 
                              engine='openpyxl') as writer:
                
                # Main analysis
                features_df.to_excel(writer, sheet_name='Coin Analysis', index=False)
                
                # Wallet analysis
                if not wallets_df.empty:
                    wallets_df.to_excel(writer, sheet_name='Wallet Analysis', index=False)
                
                # Top performers
                top_performers_df = pd.DataFrame(insights['top_performers'])
                top_performers_df.to_excel(writer, sheet_name='Top Performers', index=False)
                
                # Security summary
                security_summary = []
                for coin_name, data in features_df.iterrows():
                    security_summary.append({
                        'coin_name': data['coin_name'],
                        'max_gain': data['max_gain'],
                        'freeze_disabled': data['freeze_disabled'],
                        'mint_disabled': data['mint_disabled'],
                        'lp_burned': data['lp_burned'],
                        'security_score': sum([data['freeze_disabled'], data['mint_disabled'], data['lp_burned']])
                    })
                
                security_df = pd.DataFrame(security_summary)
                security_df.to_excel(writer, sheet_name='Security Analysis', index=False)
            
            print("✅ Excel failas išsaugotas: telegram_analysis_complete.xlsx")
            
        except Exception as e:
            print(f"⚠️ Nepavyko sukurti Excel failo: {e}")

    def create_summary_dashboard(self, features_df, coin_data, insights):
        """Sukuria summary dashboard vizualizaciją"""
        print("\n🎛️ Kuriame summary dashboard...")
        
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Top 10 Coins Performance
        plt.subplot(3, 4, 1)
        top_10 = features_df.nlargest(10, 'max_gain')
        bars = plt.bar(range(len(top_10)), top_10['max_gain'], color='gold', alpha=0.8)
        plt.title('🏆 Top 10 Max Gains', fontweight='bold')
        plt.xticks(range(len(top_10)), top_10['coin_name'], rotation=45, ha='right', fontsize=8)
        plt.ylabel('Max Gain (x)')
        
        # 2. Gain Distribution
        plt.subplot(3, 4, 2)
        all_gains = [gain for data in coin_data.values() for gain in data['gains']]
        plt.hist(all_gains, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('📊 Gain Distribution', fontweight='bold')
        plt.xlabel('Gain (x)')
        plt.ylabel('Frequency')
        
        # 3. Security Features Pie Chart
        plt.subplot(3, 4, 3)
        security_counts = [
            features_df['freeze_disabled'].sum(),
            features_df['mint_disabled'].sum(),
            features_df['lp_burned'].sum()
        ]
        plt.pie(security_counts, labels=['Freeze Disabled', 'Mint Disabled', 'LP Burned'], 
               autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        plt.title('🔒 Security Features', fontweight='bold')
        
        # 4. Success Score Distribution
        plt.subplot(3, 4, 4)
        plt.scatter(features_df['max_gain'], features_df['success_score'], 
                   alpha=0.6, c=features_df['total_signals'], cmap='viridis')
        plt.title('🎯 Success Score vs Gain', fontweight='bold')
        plt.xlabel('Max Gain (x)')
        plt.ylabel('Success Score')
        plt.colorbar(label='Signals')
        
        # 5. Gain Categories
        plt.subplot(3, 4, 5)
        gain_categories = {
            '2-5x': len(features_df[(features_df['max_gain'] >= 2) & (features_df['max_gain'] < 5)]),
            '5-10x': len(features_df[(features_df['max_gain'] >= 5) & (features_df['max_gain'] < 10)]),
            '10-50x': len(features_df[(features_df['max_gain'] >= 10) & (features_df['max_gain'] < 50)]),
            '50x+': len(features_df[features_df['max_gain'] >= 50])
        }
        plt.bar(gain_categories.keys(), gain_categories.values(), 
               color=['lightgreen', 'orange', 'red', 'darkred'], alpha=0.8)
        plt.title('📈 Gain Categories', fontweight='bold')
        plt.ylabel('Number of Coins')
        
        # 6. Signal Frequency
        plt.subplot(3, 4, 6)
        signal_freq = features_df['total_signals'].value_counts().head(10)
        plt.bar(signal_freq.index, signal_freq.values, color='lightcoral', alpha=0.8)
        plt.title('📡 Signal Frequency', fontweight='bold')
        plt.xlabel('Total Signals')
        plt.ylabel('Number of Coins')
        
        # 7. Links Analysis
        plt.subplot(3, 4, 7)
        link_features = ['has_web', 'has_telegram', 'has_dexscreener', 'has_rugcheck']
        link_counts = [features_df[feature].sum() for feature in link_features]
        plt.bar(['Web', 'Telegram', 'DexScreener', 'RugCheck'], link_counts, 
               color='lightblue', alpha=0.8)
        plt.title('🔗 Link Presence', fontweight='bold')
        plt.ylabel('Number of Coins')
        plt.xticks(rotation=45)
        
        # 8. Average Gains by Security
        plt.subplot(3, 4, 8)
        secure_coins = features_df[
            (features_df['freeze_disabled']) & 
            (features_df['mint_disabled']) & 
            (features_df['lp_burned'])
        ]['max_gain'].mean()
        
        insecure_coins = features_df[
            (~features_df['freeze_disabled']) | 
            (~features_df['mint_disabled']) | 
            (~features_df['lp_burned'])
        ]['max_gain'].mean()
        
        plt.bar(['Secure Coins', 'Risky Coins'], [secure_coins, insecure_coins], 
               color=['green', 'red'], alpha=0.7)
        plt.title('🛡️ Security vs Performance', fontweight='bold')
        plt.ylabel('Average Max Gain (x)')
        
        # 9-12. Key Metrics Text Boxes
        metrics_data = [
            f"Total Coins\n{len(features_df)}",
            f"Avg Max Gain\n{features_df['max_gain'].mean():.1f}x",
            f"Best Performer\n{features_df.loc[features_df['max_gain'].idxmax(), 'coin_name']}\n{features_df['max_gain'].max():.1f}x",
            f"Success Rate\n{len(features_df[features_df['max_gain'] >= 5])/len(features_df)*100:.1f}%\n(5x+ gains)"
        ]
        
        for i, metric in enumerate(metrics_data, 9):
            plt.subplot(3, 4, i)
            plt.text(0.5, 0.5, metric, ha='center', va='center', 
                    fontsize=14, fontweight='bold', 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            plt.axis('off')
        
        plt.suptitle('🤖 TELEGRAM COIN CALLS - COMPREHENSIVE DASHBOARD', 
                    fontsize=20, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.subplots_adjust(top=0.94)
        plt.savefig('/workspaces/0xbot/plots/comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Comprehensive dashboard išsaugotas")

#!/usr/bin/env python3
"""
Enhanced Telegram Signal Analyzer with Machine Learning
Integrates new CSV data and provides ML-based predictions
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class EnhancedTelegramAnalyzer:
    def __init__(self):
        self.df = None
        self.ml_model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_data(self):
        """Load the new comprehensive dataset"""
        try:
            self.df = pd.read_csv('telegram_chat_0xBot_AI_Agent___Solana_network.csv')
            print(f"✅ Loaded {len(self.df)} signals from new dataset")
            print(f"📊 Columns: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def analyze_data_structure(self):
        """Analyze the structure of new data"""
        if self.df is None:
            print("❌ No data loaded")
            return
            
        print("\n📋 DATA STRUCTURE ANALYSIS:")
        print(f"Total signals: {len(self.df)}")
        print(f"Date range: {self.df['date'].min()} to {self.df['date'].max()}")
        print(f"Unique tokens: {self.df['token_name'].nunique()}")
        
        # Analyze message types
        print("\n📝 MESSAGE TYPES:")
        print(self.df['message_type'].value_counts().head())
        
        # Analyze gains data
        gains_data = self.df[self.df['gains'].notna()]
        if len(gains_data) > 0:
            print(f"\n💰 GAINS ANALYSIS ({len(gains_data)} signals with gains):")
            print(f"Average gain: {gains_data['gains'].mean():.2f}x")
            print(f"Median gain: {gains_data['gains'].median():.2f}x")
            print(f"Max gain: {gains_data['gains'].max():.2f}x")
            print(f"Success rate (>5x): {(gains_data['gains'] >= 5).mean()*100:.1f}%")
    
    def extract_enhanced_features(self):
        """Extract features for ML model"""
        print("\n🔧 EXTRACTING ENHANCED FEATURES...")
        
        # Filter to signals with complete data
        signals = self.df[
            (self.df['message_type'] == 'signal') & 
            (self.df['initial_mc'].notna()) &
            (self.df['token_address'].notna())
        ].copy()
        
        print(f"📊 Processing {len(signals)} complete signals...")
        
        # Extract numerical features
        features = []
        for idx, row in signals.iterrows():
            try:
                feature_dict = {
                    'initial_mc': self.parse_value(str(row['initial_mc'])),
                    'initial_lp_sol': self.parse_value(str(row['initial_lp_sol'])),
                    'lp_tokens_percent': self.parse_percentage(str(row['lp_tokens_percent'])),
                    'top_holders_percent': self.parse_percentage(str(row['top_holders_percent'])),
                    'freeze_disabled': 1 if 'Disabled' in str(row['freeze_status']) else 0,
                    'mint_disabled': 1 if 'Disabled' in str(row['mint_status']) else 0,
                    'lp_burned': 1 if 'Burned' in str(row['lp_status']) else 0,
                    'has_website': 1 if pd.notna(row['website']) else 0,
                    'has_twitter': 1 if pd.notna(row['twitter']) else 0,
                    'has_telegram': 1 if pd.notna(row['telegram_link']) else 0,
                    'hour_of_day': pd.to_datetime(row['date']).hour,
                    'day_of_week': pd.to_datetime(row['date']).weekday(),
                    'strategy': self.encode_strategy(str(row['strategy'])),
                    'max_gain': row['gains'] if pd.notna(row['gains']) else 0
                }
                
                # Add wallet concentration features
                wallet_percentages = self.extract_wallet_percentages(str(row['holders_info']))
                if wallet_percentages:
                    feature_dict['max_wallet_percent'] = max(wallet_percentages)
                    feature_dict['avg_wallet_percent'] = np.mean(wallet_percentages)
                    feature_dict['wallet_count'] = len(wallet_percentages)
                else:
                    feature_dict['max_wallet_percent'] = 0
                    feature_dict['avg_wallet_percent'] = 0
                    feature_dict['wallet_count'] = 0
                
                feature_dict['signal_id'] = idx
                feature_dict['token_name'] = row['token_name']
                feature_dict['token_address'] = row['token_address']
                
                features.append(feature_dict)
                
            except Exception as e:
                continue
        
        self.features_df = pd.DataFrame(features)
        print(f"✅ Extracted features for {len(self.features_df)} signals")
        return self.features_df
    
    def parse_value(self, value_str):
        """Parse K/M/B values to numbers"""
        if pd.isna(value_str) or value_str == 'nan':
            return 0
        
        value_str = str(value_str).replace('$', '').replace(',', '').strip()
        
        if 'K' in value_str:
            return float(re.sub(r'[^\d.]', '', value_str)) * 1000
        elif 'M' in value_str:
            return float(re.sub(r'[^\d.]', '', value_str)) * 1000000
        elif 'B' in value_str:
            return float(re.sub(r'[^\d.]', '', value_str)) * 1000000000
        else:
            try:
                return float(re.sub(r'[^\d.]', '', value_str))
            except:
                return 0
    
    def parse_percentage(self, percent_str):
        """Parse percentage values"""
        if pd.isna(percent_str) or percent_str == 'nan':
            return 0
        try:
            return float(re.sub(r'[^\d.]', '', str(percent_str)))
        except:
            return 0
    
    def encode_strategy(self, strategy_str):
        """Encode strategy types numerically"""
        strategy_map = {
            'Viper Vision': 1,
            'Cobra Scan': 2,
            'Eagle Eye': 3,
            'Hawk Hunter': 4
        }
        return strategy_map.get(str(strategy_str), 0)
    
    def extract_wallet_percentages(self, holders_info):
        """Extract wallet percentages from holders info"""
        if pd.isna(holders_info) or holders_info == 'nan':
            return []
        
        percentages = re.findall(r'(\d+\.?\d*)%', str(holders_info))
        return [float(p) for p in percentages if float(p) > 0]
    
    def train_ml_model(self):
        """Train ML model to predict success"""
        if not hasattr(self, 'features_df') or self.features_df is None:
            print("❌ No features extracted")
            return
        
        print("\n🤖 TRAINING ML MODEL...")
        
        # Prepare features and target
        feature_cols = [
            'initial_mc', 'initial_lp_sol', 'lp_tokens_percent', 'top_holders_percent',
            'freeze_disabled', 'mint_disabled', 'lp_burned', 'has_website', 'has_twitter',
            'has_telegram', 'hour_of_day', 'day_of_week', 'strategy', 'max_wallet_percent',
            'avg_wallet_percent', 'wallet_count'
        ]
        
        # Filter complete data
        complete_data = self.features_df[
            (self.features_df['max_gain'] > 0) &
            (self.features_df[feature_cols].notna().all(axis=1))
        ].copy()
        
        if len(complete_data) < 50:
            print(f"❌ Insufficient data for ML training: {len(complete_data)} samples")
            return
        
        X = complete_data[feature_cols]
        y = (complete_data['max_gain'] >= 5).astype(int)  # Success = 5x or more
        
        print(f"📊 Training data: {len(X)} samples, {y.sum()} successes ({y.mean()*100:.1f}%)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.ml_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        
        self.ml_model.fit(X_train_scaled, y_train)
        self.feature_columns = feature_cols
        
        # Evaluate
        y_pred = self.ml_model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Model trained with {accuracy*100:.1f}% accuracy")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': self.ml_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📊 TOP FEATURE IMPORTANCE:")
        print(feature_importance.head(10))
        
        return self.ml_model
    
    def analyze_dev_patterns(self):
        """Analyze developer wallet patterns"""
        print("\n👨‍💻 ANALYZING DEVELOPER PATTERNS...")
        
        if self.df is None:
            return
        
        # Extract deployer addresses
        deployers = self.df[self.df['deployer_address'].notna()]['deployer_address'].value_counts()
        repeat_deployers = deployers[deployers > 1]
        
        print(f"🔍 Found {len(repeat_deployers)} developers with multiple tokens:")
        
        dev_analysis = []
        for deployer, count in repeat_deployers.head(20).items():
            deployer_tokens = self.df[self.df['deployer_address'] == deployer]
            gains_data = deployer_tokens[deployer_tokens['gains'].notna()]
            
            if len(gains_data) > 0:
                avg_gain = gains_data['gains'].mean()
                success_rate = (gains_data['gains'] >= 5).mean()
                
                dev_analysis.append({
                    'deployer': deployer,
                    'token_count': count,
                    'avg_gain': avg_gain,
                    'success_rate': success_rate,
                    'max_gain': gains_data['gains'].max()
                })
        
        dev_df = pd.DataFrame(dev_analysis).sort_values('success_rate', ascending=False)
        
        print("\n🏆 TOP PERFORMING DEVELOPERS:")
        print(dev_df.head(10).to_string(index=False))
        
        return dev_df
    
    def analyze_time_patterns(self):
        """Analyze time-based patterns"""
        print("\n⏰ ANALYZING TIME PATTERNS...")
        
        if not hasattr(self, 'features_df'):
            return
        
        # Hour analysis
        hourly_success = self.features_df.groupby('hour_of_day').agg({
            'max_gain': ['count', 'mean'],
            'signal_id': lambda x: (self.features_df.loc[x.index, 'max_gain'] >= 5).mean()
        }).round(3)
        
        hourly_success.columns = ['signal_count', 'avg_gain', 'success_rate']
        
        print("\n📅 HOURLY ANALYSIS:")
        print(hourly_success.sort_values('success_rate', ascending=False).head(10))
        
        # Day of week analysis
        daily_success = self.features_df.groupby('day_of_week').agg({
            'max_gain': ['count', 'mean'],
            'signal_id': lambda x: (self.features_df.loc[x.index, 'max_gain'] >= 5).mean()
        }).round(3)
        
        daily_success.columns = ['signal_count', 'avg_gain', 'success_rate']
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_success.index = [day_names[i] for i in daily_success.index]
        
        print("\n📊 DAILY ANALYSIS:")
        print(daily_success.sort_values('success_rate', ascending=False))
        
        return hourly_success, daily_success
    
    def predict_new_signal(self, signal_data):
        """Predict success probability for new signal"""
        if self.ml_model is None:
            print("❌ ML model not trained")
            return None
        
        try:
            # Prepare features
            features = np.array([[
                signal_data.get('initial_mc', 0),
                signal_data.get('initial_lp_sol', 0),
                signal_data.get('lp_tokens_percent', 0),
                signal_data.get('top_holders_percent', 0),
                signal_data.get('freeze_disabled', 0),
                signal_data.get('mint_disabled', 0),
                signal_data.get('lp_burned', 0),
                signal_data.get('has_website', 0),
                signal_data.get('has_twitter', 0),
                signal_data.get('has_telegram', 0),
                signal_data.get('hour_of_day', 12),
                signal_data.get('day_of_week', 1),
                signal_data.get('strategy', 1),
                signal_data.get('max_wallet_percent', 0),
                signal_data.get('avg_wallet_percent', 0),
                signal_data.get('wallet_count', 0)
            ]])
            
            features_scaled = self.scaler.transform(features)
            
            # Get prediction and probability
            prediction = self.ml_model.predict(features_scaled)[0]
            probability = self.ml_model.predict_proba(features_scaled)[0][1]
            
            return {
                'prediction': 'SUCCESS' if prediction == 1 else 'RISK',
                'success_probability': probability * 100,
                'confidence': max(probability, 1-probability) * 100
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        print("\n📝 GENERATING COMPREHENSIVE REPORT...")
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'dataset_stats': {
                'total_signals': len(self.df),
                'unique_tokens': self.df['token_name'].nunique(),
                'date_range': f"{self.df['date'].min()} - {self.df['date'].max()}"
            },
            'performance_stats': {},
            'model_stats': {},
            'recommendations': []
        }
        
        # Add performance stats
        if hasattr(self, 'features_df'):
            gains_data = self.features_df[self.features_df['max_gain'] > 0]
            if len(gains_data) > 0:
                report['performance_stats'] = {
                    'total_analyzed': len(gains_data),
                    'avg_gain': float(gains_data['max_gain'].mean()),
                    'median_gain': float(gains_data['max_gain'].median()),
                    'max_gain': float(gains_data['max_gain'].max()),
                    'success_rate_5x': float((gains_data['max_gain'] >= 5).mean()),
                    'success_rate_10x': float((gains_data['max_gain'] >= 10).mean())
                }
        
        # Add model stats
        if self.ml_model is not None:
            report['model_stats'] = {
                'model_trained': True,
                'feature_count': len(self.feature_columns),
                'top_features': list(
                    pd.DataFrame({
                        'feature': self.feature_columns,
                        'importance': self.ml_model.feature_importances_
                    }).sort_values('importance', ascending=False)['feature'].head(5)
                )
            }
        
        # Save report
        with open('enhanced_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("✅ Report saved to enhanced_analysis_report.json")
        return report

def main():
    """Main analysis function"""
    print("🚀 ENHANCED TELEGRAM ANALYZER STARTING...")
    
    analyzer = EnhancedTelegramAnalyzer()
    
    # Load and analyze data
    if not analyzer.load_data():
        return
    
    analyzer.analyze_data_structure()
    analyzer.extract_enhanced_features()
    analyzer.train_ml_model()
    analyzer.analyze_dev_patterns()
    analyzer.analyze_time_patterns()
    analyzer.generate_comprehensive_report()
    
    print("\n🎉 ENHANCED ANALYSIS COMPLETE!")
    
    # Test prediction with sample data
    print("\n🧪 TESTING ML PREDICTION...")
    sample_signal = {
        'initial_mc': 75000,
        'initial_lp_sol': 85,
        'lp_tokens_percent': 20,
        'top_holders_percent': 22,
        'freeze_disabled': 1,
        'mint_disabled': 1,
        'lp_burned': 0,
        'has_website': 1,
        'has_twitter': 1,
        'has_telegram': 1,
        'hour_of_day': 23,
        'day_of_week': 6,
        'strategy': 2,
        'max_wallet_percent': 3.5,
        'avg_wallet_percent': 2.1,
        'wallet_count': 10
    }
    
    prediction = analyzer.predict_new_signal(sample_signal)
    if prediction:
        print(f"📊 Sample Prediction: {prediction}")

if __name__ == "__main__":
    main()
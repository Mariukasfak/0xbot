#!/usr/bin/env python3
"""
Advanced ML Signal Analyzer
Uses parsed telegram data to train ML models and predict signal success
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLAnalyzer:
    def __init__(self):
        self.df = None
        self.ml_model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_parsed_data(self):
        """Load parsed telegram data"""
        try:
            self.df = pd.read_csv('parsed_telegram_data.csv')
            print(f"✅ Loaded {len(self.df)} parsed signals")
            
            # Convert date column
            self.df['date'] = pd.to_datetime(self.df['date'])
            
            # Filter signals with complete data
            complete_signals = self.df[
                (self.df['initial_mc'].notna()) & 
                (self.df['max_gain'] >= 0)
            ].copy()
            
            print(f"📊 Complete signals for analysis: {len(complete_signals)}")
            print(f"🎯 Signals with gains: {(complete_signals['max_gain'] > 0).sum()}")
            
            self.df = complete_signals
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def engineer_features(self):
        """Engineer features for ML model"""
        print("\n🔧 ENGINEERING FEATURES...")
        
        # Parse market cap values
        self.df['initial_mc_value'] = self.df['initial_mc'].apply(self.parse_mc_value)
        self.df['call_mc_value'] = self.df['call_mc'].apply(self.parse_mc_value)
        
        # Calculate wallet concentration metrics
        self.df['max_wallet_percent'] = self.df['wallet_percentages'].apply(
            lambda x: max(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        self.df['avg_wallet_percent'] = self.df['wallet_percentages'].apply(
            lambda x: np.mean(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        self.df['wallet_count'] = self.df['wallet_percentages'].apply(
            lambda x: len(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        
        # Time-based features
        self.df['hour'] = self.df['date'].dt.hour
        self.df['day_of_week'] = self.df['date'].dt.dayofweek
        self.df['month'] = self.df['date'].dt.month
        
        # Binary features
        self.df['freeze_disabled_int'] = self.df['freeze_disabled'].astype(int)
        self.df['mint_disabled_int'] = self.df['mint_disabled'].astype(int)
        self.df['lp_burned_int'] = self.df['lp_burned'].astype(int)
        
        # Strategy encoding
        self.df['strategy_encoded'] = self.df['strategy'].map({
            'Viper Vision': 1,
            'Cobra Scan': 2,
            'Eagle Eye': 3,
            'Phoenix Sight': 4,
            'Pheonix Sight': 4,  # Same as Phoenix
            'Hydra Hunt': 5,
            'Dragon Detector': 6,
            'Wolf Watch': 7,
            'Tiger Trace': 8,
            'Tiger Trace 2': 8,
            'Scorpion Sweep': 9
        }).fillna(0)
        
        # Target variable
        self.df['success_5x'] = (self.df['max_gain'] >= 5).astype(int)
        self.df['success_10x'] = (self.df['max_gain'] >= 10).astype(int)
        
        print(f"✅ Feature engineering complete")
        return self.df
    
    def parse_mc_value(self, mc_str):
        """Parse market cap string to numeric value"""
        if pd.isna(mc_str):
            return 0
        
        mc_str = str(mc_str).replace('$', '').replace(',', '').strip()
        
        try:
            if 'K' in mc_str:
                return float(re.sub(r'[^\d.]', '', mc_str)) * 1000
            elif 'M' in mc_str:
                return float(re.sub(r'[^\d.]', '', mc_str)) * 1000000
            elif 'B' in mc_str:
                return float(re.sub(r'[^\d.]', '', mc_str)) * 1000000000
            else:
                return float(re.sub(r'[^\d.]', '', mc_str))
        except:
            return 0
    
    def train_ml_models(self, target='success_5x'):
        """Train multiple ML models"""
        print(f"\n🤖 TRAINING ML MODELS FOR {target.upper()}...")
        
        # Feature columns
        feature_cols = [
            'initial_mc_value', 'initial_lp_sol', 'lp_tokens_percent',
            'top_holders_percent', 'max_wallet_percent', 'avg_wallet_percent',
            'wallet_count', 'freeze_disabled_int', 'mint_disabled_int',
            'lp_burned_int', 'hour', 'day_of_week', 'month', 'strategy_encoded'
        ]
        
        # Filter complete data
        complete_data = self.df[
            self.df[feature_cols + [target]].notna().all(axis=1)
        ].copy()
        
        print(f"📊 Training samples: {len(complete_data)}")
        
        if len(complete_data) < 100:
            print("❌ Insufficient data for ML training")
            return None
        
        X = complete_data[feature_cols]
        y = complete_data[target]
        
        print(f"📈 Success rate: {y.mean()*100:.1f}%")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=10,
                random_state=42
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        best_model = None
        best_accuracy = 0
        
        for name, model in models.items():
            # Train model
            if name == 'Random Forest':
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            else:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            
            accuracy = accuracy_score(y_test, y_pred)
            print(f"📊 {name} Accuracy: {accuracy*100:.1f}%")
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                self.ml_model = model
                self.feature_columns = feature_cols
                self.model_name = name
        
        # Feature importance
        if hasattr(best_model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': feature_cols,
                'importance': best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n📊 TOP FEATURE IMPORTANCE ({self.model_name}):")
            print(feature_importance.head(10))
        
        return best_model
    
    def analyze_success_patterns(self):
        """Analyze patterns that lead to success"""
        print("\n📈 ANALYZING SUCCESS PATTERNS...")
        
        # Success by strategy
        strategy_analysis = self.df.groupby('strategy').agg({
            'max_gain': ['count', 'mean', 'median'],
            'success_5x': 'mean',
            'success_10x': 'mean'
        }).round(3)
        
        strategy_analysis.columns = ['Count', 'Avg_Gain', 'Median_Gain', 'Success_5x_Rate', 'Success_10x_Rate']
        strategy_analysis = strategy_analysis.sort_values('Success_5x_Rate', ascending=False)
        
        print("\n🎯 STRATEGY PERFORMANCE:")
        print(strategy_analysis)
        
        # Time analysis
        hourly_success = self.df.groupby('hour').agg({
            'max_gain': 'count',
            'success_5x': 'mean',
            'success_10x': 'mean'
        }).round(3)
        
        print(f"\n⏰ BEST HOURS FOR SIGNALS:")
        best_hours = hourly_success.sort_values('success_5x', ascending=False).head(5)
        print(best_hours)
        
        # Market cap analysis
        mc_bins = [0, 50000, 100000, 200000, 500000, float('inf')]
        mc_labels = ['<50K', '50K-100K', '100K-200K', '200K-500K', '>500K']
        
        self.df['mc_range'] = pd.cut(self.df['initial_mc_value'], bins=mc_bins, labels=mc_labels)
        mc_analysis = self.df.groupby('mc_range').agg({
            'max_gain': 'count',
            'success_5x': 'mean',
            'success_10x': 'mean'
        }).round(3)
        
        print(f"\n💰 SUCCESS BY MARKET CAP:")
        print(mc_analysis)
        
        # Security features impact
        security_features = ['freeze_disabled', 'mint_disabled', 'lp_burned']
        
        print(f"\n🔒 SECURITY FEATURES IMPACT:")
        for feature in security_features:
            impact = self.df.groupby(feature)['success_5x'].mean()
            print(f"{feature}: {impact.to_dict()}")
    
    def predict_signal_success(self, signal_data):
        """Predict success probability for a new signal"""
        if self.ml_model is None:
            print("❌ Model not trained")
            return None
        
        try:
            # Prepare features
            features = np.array([[
                signal_data.get('initial_mc_value', 0),
                signal_data.get('initial_lp_sol', 0),
                signal_data.get('lp_tokens_percent', 0),
                signal_data.get('top_holders_percent', 0),
                signal_data.get('max_wallet_percent', 0),
                signal_data.get('avg_wallet_percent', 0),
                signal_data.get('wallet_count', 0),
                signal_data.get('freeze_disabled_int', 0),
                signal_data.get('mint_disabled_int', 0),
                signal_data.get('lp_burned_int', 0),
                signal_data.get('hour', 12),
                signal_data.get('day_of_week', 1),
                signal_data.get('month', 1),
                signal_data.get('strategy_encoded', 1)
            ]])
            
            # Scale if needed
            if self.model_name == 'Gradient Boosting':
                features = self.scaler.transform(features)
            
            # Get prediction
            prediction = self.ml_model.predict(features)[0]
            probability = self.ml_model.predict_proba(features)[0][1]
            
            return {
                'prediction': 'SUCCESS' if prediction == 1 else 'RISK',
                'success_probability': probability * 100,
                'confidence': max(probability, 1-probability) * 100,
                'model_used': self.model_name
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None
    
    def create_visualizations(self):
        """Create analysis visualizations"""
        print("\n📊 CREATING VISUALIZATIONS...")
        
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Gains distribution
        axes[0,0].hist(self.df[self.df['max_gain'] > 0]['max_gain'], bins=50, alpha=0.7, color='green')
        axes[0,0].set_title('Gains Distribution')
        axes[0,0].set_xlabel('Gain Multiplier')
        axes[0,0].set_ylabel('Frequency')
        axes[0,0].set_xlim(0, 100)
        
        # 2. Success rate by hour
        hourly_success = self.df.groupby('hour')['success_5x'].mean()
        axes[0,1].bar(hourly_success.index, hourly_success.values, color='blue', alpha=0.7)
        axes[0,1].set_title('Success Rate by Hour')
        axes[0,1].set_xlabel('Hour of Day')
        axes[0,1].set_ylabel('Success Rate')
        
        # 3. Strategy performance
        strategy_success = self.df.groupby('strategy')['success_5x'].mean().sort_values(ascending=False)
        axes[0,2].barh(range(len(strategy_success)), strategy_success.values, color='orange', alpha=0.7)
        axes[0,2].set_yticks(range(len(strategy_success)))
        axes[0,2].set_yticklabels(strategy_success.index, fontsize=8)
        axes[0,2].set_title('Success Rate by Strategy')
        axes[0,2].set_xlabel('Success Rate')
        
        # 4. Market cap vs success
        axes[1,0].scatter(self.df['initial_mc_value'], self.df['max_gain'], alpha=0.5, s=10)
        axes[1,0].set_title('Market Cap vs Gains')
        axes[1,0].set_xlabel('Initial MC ($)')
        axes[1,0].set_ylabel('Max Gain')
        axes[1,0].set_xlim(0, 500000)
        axes[1,0].set_ylim(0, 100)
        
        # 5. Wallet concentration impact
        wallet_bins = [0, 2, 5, 10, float('inf')]
        wallet_labels = ['<2%', '2-5%', '5-10%', '>10%']
        self.df['wallet_concentration'] = pd.cut(self.df['max_wallet_percent'], bins=wallet_bins, labels=wallet_labels)
        wallet_success = self.df.groupby('wallet_concentration')['success_5x'].mean()
        axes[1,1].bar(range(len(wallet_success)), wallet_success.values, color='red', alpha=0.7)
        axes[1,1].set_xticks(range(len(wallet_success)))
        axes[1,1].set_xticklabels(wallet_labels)
        axes[1,1].set_title('Success Rate by Wallet Concentration')
        axes[1,1].set_ylabel('Success Rate')
        
        # 6. Security features
        security_data = [
            self.df.groupby('freeze_disabled')['success_5x'].mean(),
            self.df.groupby('mint_disabled')['success_5x'].mean(),
            self.df.groupby('lp_burned')['success_5x'].mean()
        ]
        
        features = ['Freeze Disabled', 'Mint Disabled', 'LP Burned']
        x_pos = np.arange(len(features))
        
        enabled_rates = [data[True] if True in data else 0 for data in security_data]
        disabled_rates = [data[False] if False in data else 0 for data in security_data]
        
        width = 0.35
        axes[1,2].bar(x_pos - width/2, enabled_rates, width, label='Enabled/True', color='green', alpha=0.7)
        axes[1,2].bar(x_pos + width/2, disabled_rates, width, label='Disabled/False', color='red', alpha=0.7)
        axes[1,2].set_xticks(x_pos)
        axes[1,2].set_xticklabels(features, rotation=45)
        axes[1,2].set_title('Security Features Impact')
        axes[1,2].set_ylabel('Success Rate')
        axes[1,2].legend()
        
        plt.tight_layout()
        plt.savefig('plots/advanced_ml_analysis.png', dpi=300, bbox_inches='tight')
        print("✅ Visualizations saved to plots/advanced_ml_analysis.png")
        
    def generate_ml_report(self):
        """Generate comprehensive ML analysis report"""
        print("\n📝 GENERATING ML REPORT...")
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'dataset_stats': {
                'total_signals': len(self.df),
                'signals_with_gains': (self.df['max_gain'] > 0).sum(),
                'avg_gain': float(self.df[self.df['max_gain'] > 0]['max_gain'].mean()),
                'success_rate_5x': float(self.df['success_5x'].mean()),
                'success_rate_10x': float(self.df['success_10x'].mean())
            },
            'ml_model': {
                'model_type': getattr(self, 'model_name', 'Unknown'),
                'feature_count': len(self.feature_columns),
                'top_features': []
            },
            'insights': {
                'best_strategies': [],
                'best_hours': [],
                'security_impact': {}
            }
        }
        
        # Add feature importance if available
        if hasattr(self.ml_model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.ml_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            report['ml_model']['top_features'] = feature_importance.head(5).to_dict('records')
        
        # Strategy insights
        strategy_success = self.df.groupby('strategy')['success_5x'].mean().sort_values(ascending=False)
        report['insights']['best_strategies'] = strategy_success.head(3).to_dict()
        
        # Time insights
        hourly_success = self.df.groupby('hour')['success_5x'].mean().sort_values(ascending=False)
        report['insights']['best_hours'] = hourly_success.head(3).to_dict()
        
        # Save report
        with open('advanced_ml_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print("✅ ML report saved to advanced_ml_report.json")
        return report

def main():
    """Main ML analysis function"""
    print("🚀 ADVANCED ML ANALYZER STARTING...")
    
    analyzer = AdvancedMLAnalyzer()
    
    if not analyzer.load_parsed_data():
        return
    
    analyzer.engineer_features()
    analyzer.train_ml_models('success_5x')
    analyzer.analyze_success_patterns()
    analyzer.create_visualizations()
    analyzer.generate_ml_report()
    
    print("\n🎉 ADVANCED ML ANALYSIS COMPLETE!")
    
    # Test prediction
    print("\n🧪 TESTING PREDICTION ON SAMPLE SIGNAL...")
    sample_signal = {
        'initial_mc_value': 75000,
        'initial_lp_sol': 85,
        'lp_tokens_percent': 20,
        'top_holders_percent': 22,
        'max_wallet_percent': 3.5,
        'avg_wallet_percent': 2.1,
        'wallet_count': 10,
        'freeze_disabled_int': 1,
        'mint_disabled_int': 1,
        'lp_burned_int': 0,
        'hour': 23,
        'day_of_week': 6,
        'month': 5,
        'strategy_encoded': 2
    }
    
    prediction = analyzer.predict_signal_success(sample_signal)
    if prediction:
        print(f"📊 Prediction: {prediction}")

if __name__ == "__main__":
    main()

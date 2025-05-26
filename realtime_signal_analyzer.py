#!/usr/bin/env python3
"""
Real-time Signal Analyzer with ML Predictions
Processes new Telegram signals and provides ML-based success predictions
"""

import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class RealtimeSignalAnalyzer:
    def __init__(self):
        self.ml_model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.insights = {}
        self.trained = False
        
    def load_model_and_insights(self):
        """Load pre-trained model and insights"""
        try:
            # Load insights from ML report
            with open('advanced_ml_report.json', 'r') as f:
                report = json.load(f)
                self.insights = report['insights']
            
            # Retrain the model using saved data
            df = pd.read_csv('parsed_telegram_data.csv')
            df['date'] = pd.to_datetime(df['date'])
            
            # Filter complete signals
            complete_signals = df[
                (df['initial_mc'].notna()) & 
                (df['max_gain'] >= 0)
            ].copy()
            
            # Engineer features
            complete_signals = self._engineer_features(complete_signals)
            
            # Prepare features for ML
            feature_cols = ['initial_mc_value', 'top_holders_percent', 'initial_lp_sol', 
                          'hour', 'day_of_week', 'strategy_encoded', 'freeze_disabled_int',
                          'mint_disabled_int', 'lp_burned_int', 'max_wallet_percent',
                          'avg_wallet_percent', 'wallet_count', 'month', 'call_mc_value']
            
            X = complete_signals[feature_cols].fillna(0)
            y = (complete_signals['max_gain'] >= 5).astype(int)
            
            # Train model
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.ml_model.fit(X, y)
            self.feature_columns = feature_cols
            self.trained = True
            
            print("✅ Model and insights loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def _engineer_features(self, df):
        """Engineer features for the dataframe"""
        # Parse market cap values
        df['initial_mc_value'] = df['initial_mc'].apply(self._parse_mc_value)
        df['call_mc_value'] = df['call_mc'].apply(self._parse_mc_value)
        
        # Calculate wallet concentration metrics
        df['max_wallet_percent'] = df['wallet_percentages'].apply(
            lambda x: max(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        df['avg_wallet_percent'] = df['wallet_percentages'].apply(
            lambda x: np.mean(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        df['wallet_count'] = df['wallet_percentages'].apply(
            lambda x: len(eval(x)) if isinstance(x, str) and x != '[]' else 0
        )
        
        # Time-based features
        df['hour'] = df['date'].dt.hour
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        
        # Binary features
        df['freeze_disabled_int'] = df['freeze_disabled'].astype(int)
        df['mint_disabled_int'] = df['mint_disabled'].astype(int)
        df['lp_burned_int'] = df['lp_burned'].astype(int)
        
        # Strategy encoding
        df['strategy_encoded'] = df['strategy'].map({
            'Viper Vision': 1, 'Cobra Scan': 2, 'Eagle Eye': 3,
            'Phoenix Sight': 4, 'Pheonix Sight': 4, 'Hydra Hunt': 5,
            'Dragon Detector': 6, 'Wolf Watch': 7, 'Tiger Trace': 8,
            'Tiger Trace 2': 8, 'Scorpion Sweep': 9
        }).fillna(0)
        
        return df
    
    def _parse_mc_value(self, mc_str):
        """Parse market cap string to numeric value"""
        if pd.isna(mc_str) or mc_str == '':
            return 0
        
        mc_str = str(mc_str).upper().replace('$', '').replace(',', '')
        
        if 'K' in mc_str:
            try:
                return float(mc_str.replace('K', '')) * 1000
            except:
                return 0
        elif 'M' in mc_str:
            try:
                return float(mc_str.replace('M', '')) * 1000000
            except:
                return 0
        else:
            try:
                return float(mc_str)
            except:
                return 0
    
    def parse_signal_message(self, message):
        """Parse a new signal message and extract features"""
        signal_data = {
            'token_name': '',
            'token_address': '',
            'strategy': '',
            'initial_mc': '',
            'call_mc': '',
            'initial_lp_sol': 0,
            'top_holders_percent': 0,
            'wallet_percentages': '[]',
            'freeze_disabled': False,
            'mint_disabled': False,
            'lp_burned': False,
            'date': datetime.now()
        }
        
        try:
            # Extract token name
            token_match = re.search(r'\$([A-Z]+)', message)
            if token_match:
                signal_data['token_name'] = token_match.group(1)
            
            # Extract token address
            address_match = re.search(r'([1-9A-HJ-NP-Za-km-z]{32,44})', message)
            if address_match:
                signal_data['token_address'] = address_match.group(1)
            
            # Extract strategy
            strategies = ['Viper Vision', 'Cobra Scan', 'Eagle Eye', 'Phoenix Sight', 
                         'Hydra Hunt', 'Dragon Detector', 'Wolf Watch', 'Tiger Trace', 'Scorpion Sweep']
            for strategy in strategies:
                if strategy.lower() in message.lower():
                    signal_data['strategy'] = strategy
                    break
            
            # Extract market cap
            mc_patterns = [
                r'MC:\s*\$?([0-9.]+[KM]?)',
                r'Market Cap:\s*\$?([0-9.]+[KM]?)',
                r'Initial MC:\s*\$?([0-9.]+[KM]?)'
            ]
            for pattern in mc_patterns:
                mc_match = re.search(pattern, message, re.IGNORECASE)
                if mc_match:
                    signal_data['initial_mc'] = mc_match.group(1)
                    break
            
            # Extract LP
            lp_match = re.search(r'LP:\s*([0-9.]+)', message)
            if lp_match:
                signal_data['initial_lp_sol'] = float(lp_match.group(1))
            
            # Extract top holders
            holders_match = re.search(r'Top ([0-9]+) holders:\s*([0-9.]+)%', message)
            if holders_match:
                signal_data['top_holders_percent'] = float(holders_match.group(2))
            
            # Extract security features
            signal_data['freeze_disabled'] = 'freeze disabled' in message.lower()
            signal_data['mint_disabled'] = 'mint disabled' in message.lower()
            signal_data['lp_burned'] = 'lp burned' in message.lower() or 'burned' in message.lower()
            
        except Exception as e:
            print(f"⚠️ Error parsing message: {e}")
        
        return signal_data
    
    def analyze_signal(self, message):
        """Analyze a new signal and provide ML prediction"""
        if not self.trained:
            print("❌ Model not loaded. Please run load_model_and_insights() first.")
            return None
        
        # Parse the signal
        signal_data = self.parse_signal_message(message)
        
        # Convert to DataFrame for processing
        df = pd.DataFrame([signal_data])
        df = self._engineer_features(df)
        
        # Prepare features for prediction
        X = df[self.feature_columns].fillna(0)
        
        # Get ML prediction
        success_prob = self.ml_model.predict_proba(X)[0][1]
        success_prediction = self.ml_model.predict(X)[0]
        
        # Get strategy-based insights
        strategy_success_rate = self.insights.get('best_strategies', {}).get(signal_data['strategy'], 0.27)
        
        # Get time-based insights
        current_hour = signal_data['date'].hour
        hour_success_rate = self.insights.get('best_hours', {}).get(str(current_hour), 0.27)
        
        # Generate comprehensive analysis
        analysis = {
            'signal_info': {
                'token_name': signal_data['token_name'],
                'token_address': signal_data['token_address'],
                'strategy': signal_data['strategy'],
                'timestamp': signal_data['date'].isoformat(),
                'initial_mc': signal_data['initial_mc'],
                'initial_lp_sol': signal_data['initial_lp_sol'],
                'top_holders_percent': signal_data['top_holders_percent']
            },
            'ml_prediction': {
                'success_probability': round(success_prob * 100, 1),
                'predicted_success': bool(success_prediction),
                'confidence': 'High' if abs(success_prob - 0.5) > 0.3 else 'Medium' if abs(success_prob - 0.5) > 0.15 else 'Low'
            },
            'historical_insights': {
                'strategy_success_rate': round(strategy_success_rate * 100, 1),
                'hour_success_rate': round(hour_success_rate * 100, 1),
                'overall_success_rate': 27.0
            },
            'security_features': {
                'freeze_disabled': signal_data['freeze_disabled'],
                'mint_disabled': signal_data['mint_disabled'],
                'lp_burned': signal_data['lp_burned']
            },
            'risk_assessment': self._assess_risk(signal_data, success_prob),
            'recommendation': self._generate_recommendation(signal_data, success_prob, strategy_success_rate)
        }
        
        return analysis
    
    def _assess_risk(self, signal_data, success_prob):
        """Assess risk level based on various factors"""
        risk_factors = []
        risk_score = 0
        
        # ML prediction risk
        if success_prob < 0.2:
            risk_factors.append("Low ML success probability")
            risk_score += 3
        elif success_prob < 0.4:
            risk_factors.append("Medium ML success probability")
            risk_score += 1
        
        # Market cap risk
        mc_value = self._parse_mc_value(signal_data['initial_mc'])
        if mc_value < 10000:
            risk_factors.append("Very low market cap")
            risk_score += 2
        elif mc_value > 1000000:
            risk_factors.append("High market cap")
            risk_score += 1
        
        # Liquidity risk
        if signal_data['initial_lp_sol'] < 5:
            risk_factors.append("Low liquidity")
            risk_score += 2
        
        # Whale concentration risk
        if signal_data['top_holders_percent'] > 50:
            risk_factors.append("High whale concentration")
            risk_score += 2
        
        # Security risk
        if not signal_data['freeze_disabled']:
            risk_factors.append("Freeze not disabled")
            risk_score += 1
        if not signal_data['mint_disabled']:
            risk_factors.append("Mint not disabled")
            risk_score += 1
        
        if risk_score >= 5:
            risk_level = "HIGH"
        elif risk_score >= 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors
        }
    
    def _generate_recommendation(self, signal_data, success_prob, strategy_success_rate):
        """Generate trading recommendation"""
        if success_prob >= 0.6 and strategy_success_rate >= 0.3:
            return {
                'action': 'STRONG BUY',
                'confidence': 'High',
                'reason': 'High ML probability + Strong strategy performance'
            }
        elif success_prob >= 0.4 and strategy_success_rate >= 0.25:
            return {
                'action': 'BUY',
                'confidence': 'Medium',
                'reason': 'Good ML probability + Decent strategy performance'
            }
        elif success_prob >= 0.3:
            return {
                'action': 'CONSIDER',
                'confidence': 'Low',
                'reason': 'Moderate ML probability'
            }
        else:
            return {
                'action': 'AVOID',
                'confidence': 'High',
                'reason': 'Low success probability'
            }
    
    def print_analysis(self, analysis):
        """Print formatted analysis results"""
        if not analysis:
            return
        
        print("\n" + "="*80)
        print("🚀 REAL-TIME SIGNAL ANALYSIS")
        print("="*80)
        
        # Signal Info
        info = analysis['signal_info']
        print(f"\n📊 SIGNAL INFORMATION:")
        print(f"   Token: ${info['token_name']}")
        print(f"   Address: {info['token_address']}")
        print(f"   Strategy: {info['strategy']}")
        print(f"   Time: {info['timestamp'][:19]}")
        print(f"   Initial MC: {info['initial_mc']}")
        print(f"   LP: {info['initial_lp_sol']} SOL")
        print(f"   Top Holders: {info['top_holders_percent']}%")
        
        # ML Prediction
        ml = analysis['ml_prediction']
        prob_color = "🟢" if ml['success_probability'] >= 60 else "🟡" if ml['success_probability'] >= 40 else "🔴"
        print(f"\n🤖 ML PREDICTION:")
        print(f"   Success Probability: {prob_color} {ml['success_probability']}%")
        print(f"   Predicted Success: {'✅ YES' if ml['predicted_success'] else '❌ NO'}")
        print(f"   Confidence: {ml['confidence']}")
        
        # Historical Insights
        hist = analysis['historical_insights']
        print(f"\n📈 HISTORICAL INSIGHTS:")
        print(f"   Strategy Success Rate: {hist['strategy_success_rate']}%")
        print(f"   Hour Success Rate: {hist['hour_success_rate']}%")
        print(f"   Overall Average: {hist['overall_success_rate']}%")
        
        # Security Features
        sec = analysis['security_features']
        print(f"\n🔒 SECURITY FEATURES:")
        print(f"   Freeze Disabled: {'✅' if sec['freeze_disabled'] else '❌'}")
        print(f"   Mint Disabled: {'✅' if sec['mint_disabled'] else '❌'}")
        print(f"   LP Burned: {'✅' if sec['lp_burned'] else '❌'}")
        
        # Risk Assessment
        risk = analysis['risk_assessment']
        risk_color = "🔴" if risk['risk_level'] == 'HIGH' else "🟡" if risk['risk_level'] == 'MEDIUM' else "🟢"
        print(f"\n⚠️ RISK ASSESSMENT:")
        print(f"   Risk Level: {risk_color} {risk['risk_level']}")
        print(f"   Risk Score: {risk['risk_score']}/10")
        if risk['risk_factors']:
            print(f"   Risk Factors:")
            for factor in risk['risk_factors']:
                print(f"     • {factor}")
        
        # Recommendation
        rec = analysis['recommendation']
        action_color = "🟢" if rec['action'] == 'STRONG BUY' else "🟡" if rec['action'] == 'BUY' else "🟠" if rec['action'] == 'CONSIDER' else "🔴"
        print(f"\n💡 RECOMMENDATION:")
        print(f"   Action: {action_color} {rec['action']}")
        print(f"   Confidence: {rec['confidence']}")
        print(f"   Reason: {rec['reason']}")
        
        print("\n" + "="*80)

def main():
    """Demo the real-time analyzer"""
    analyzer = RealtimeSignalAnalyzer()
    
    # Load model and insights
    if not analyzer.load_model_and_insights():
        return
    
    # Example signal message
    example_message = """
    🐅 Tiger Trace 2 Signal 🐅
    
    $EXAMPLE (Example Token)
    Address: 7xKXjT9Y8VdZ3mN5qR8wE2uA6bF4cG9hJ1kL3oP5sT7v
    
    MC: $75K
    LP: 8.5 SOL
    Top 10 holders: 35%
    
    ✅ Freeze disabled
    ✅ Mint disabled 
    ✅ LP burned
    
    This looks promising! 🚀
    """
    
    print("🔍 ANALYZING EXAMPLE SIGNAL...")
    analysis = analyzer.analyze_signal(example_message)
    analyzer.print_analysis(analysis)

if __name__ == "__main__":
    main()
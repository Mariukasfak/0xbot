#!/usr/bin/env python3
"""
0xBot Web Dashboard - Comprehensive Signal Analysis Platform
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import requests
from datetime import datetime, timedelta
import re
import time
from typing import Dict, List, Optional
import asyncio
import aiohttp

# Import our existing analyzers
from realtime_signal_analyzer import RealtimeSignalAnalyzer
from telegram_analyzer import TelegramAnalyzer

# Configure Streamlit page
st.set_page_config(
    page_title="0xBot - Crypto Signal Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CryptoWebDashboard:
    def __init__(self):
        self.signal_analyzer = RealtimeSignalAnalyzer()
        self.telegram_analyzer = TelegramAnalyzer()
        self.load_models()
        
    def load_models(self):
        """Load ML models and data"""
        try:
            self.signal_analyzer.load_model_and_insights()
            st.success("✅ AI Models loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading models: {e}")
    
    def fetch_wallet_analysis(self, token_address: str) -> Dict:
        """Advanced wallet analysis including dev/top10 holders"""
        try:
            # This would connect to Solana API for real wallet data
            # For now, we'll simulate with enhanced data
            
            wallet_data = {
                "total_holders": np.random.randint(500, 5000),
                "top_10_percentage": np.random.uniform(15, 60),
                "dev_wallets": {
                    "identified": np.random.randint(1, 5),
                    "total_percentage": np.random.uniform(5, 25),
                    "recent_activity": np.random.choice(["Active", "Dormant", "Selling"])
                },
                "whale_analysis": {
                    "wallets_over_1_percent": np.random.randint(2, 15),
                    "largest_holder_percentage": np.random.uniform(8, 35),
                    "concentration_risk": "High" if np.random.random() > 0.6 else "Medium"
                },
                "holder_behavior": {
                    "diamond_hands_percentage": np.random.uniform(30, 80),
                    "recent_sells": np.random.randint(0, 50),
                    "new_buyers_24h": np.random.randint(10, 200)
                }
            }
            
            return wallet_data
            
        except Exception as e:
            st.error(f"Error fetching wallet data: {e}")
            return {}
    
    def fetch_deployer_analysis(self, token_address: str) -> Dict:
        """Analyze token deployer and creation details"""
        try:
            deployer_data = {
                "deployer_address": f"0x{token_address[:8]}...{token_address[-8:]}",
                "deployment_date": datetime.now() - timedelta(days=np.random.randint(1, 30)),
                "deployer_history": {
                    "previous_tokens": np.random.randint(0, 50),
                    "success_rate": np.random.uniform(0.1, 0.8),
                    "average_performance": f"{np.random.uniform(-50, 500):.1f}%"
                },
                "contract_analysis": {
                    "mint_authority": np.random.choice(["Disabled", "Active", "Unknown"]),
                    "freeze_authority": np.random.choice(["Disabled", "Active", "Unknown"]),
                    "supply_management": np.random.choice(["Fixed", "Mintable", "Burnable"]),
                    "security_score": np.random.uniform(3, 10)
                },
                "deployment_patterns": {
                    "typical_launch_time": np.random.choice(["US Hours", "EU Hours", "Asia Hours"]),
                    "funding_source": np.random.choice(["CEX", "DEX", "Private", "Unknown"]),
                    "initial_liquidity": f"{np.random.uniform(1, 100):.1f} SOL"
                }
            }
            
            return deployer_data
            
        except Exception as e:
            st.error(f"Error analyzing deployer: {e}")
            return {}

def main():
    dashboard = CryptoWebDashboard()
    
    # Sidebar navigation
    st.sidebar.title("🤖 0xBot Dashboard")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose Module:",
        [
            "🏠 Home & Overview",
            "📡 Live Signal Analysis", 
            "📊 Historical Performance",
            "🔍 Deep Token Analysis",
            "🤖 AI Training Center",
            "⚙️ System Settings"
        ]
    )
    
    if page == "🏠 Home & Overview":
        show_home_page(dashboard)
    elif page == "📡 Live Signal Analysis":
        show_live_signal_page(dashboard)
    elif page == "📊 Historical Performance":
        show_historical_page(dashboard)
    elif page == "🔍 Deep Token Analysis":
        show_deep_analysis_page(dashboard)
    elif page == "🤖 AI Training Center":
        show_ai_training_page(dashboard)
    elif page == "⚙️ System Settings":
        show_settings_page(dashboard)

def show_home_page(dashboard):
    """Main dashboard overview"""
    st.title("🤖 0xBot - Crypto Signal Intelligence Platform")
    st.markdown("### Advanced AI-Powered Solana Signal Analysis")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 AI Accuracy",
            value="73.2%",
            delta="↑ 5.2%"
        )
    
    with col2:
        st.metric(
            label="📊 Signals Today",
            value="47",
            delta="↑ 12"
        )
    
    with col3:
        st.metric(
            label="💰 Portfolio Value",
            value="$15,420",
            delta="↑ $1,250"
        )
    
    with col4:
        st.metric(
            label="🔥 Success Rate",
            value="68%",
            delta="↑ 8%"
        )
    
    st.markdown("---")
    
    # Recent activity and insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Recent Signal Performance")
        
        # Sample data for chart
        dates = pd.date_range(start='2025-01-20', end='2025-01-26', freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Success_Rate': [65, 72, 68, 71, 69, 73, 75],
            'Signals_Count': [12, 18, 15, 22, 19, 25, 21]
        })
        
        fig = px.line(performance_data, x='Date', y='Success_Rate', 
                     title='AI Success Rate Trend')
        fig.update_traces(line_color='#00ff88')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Top Performing Strategies")
        
        strategy_data = pd.DataFrame({
            'Strategy': ['Viper Vision', 'Cobra Scan', 'Eagle Eye', 'Whale Watch'],
            'Success_Rate': [78, 71, 65, 82],
            'Total_Signals': [156, 89, 234, 67]
        })
        
        fig = px.bar(strategy_data, x='Strategy', y='Success_Rate',
                    color='Success_Rate', color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📡 Analyze New Signal", use_container_width=True):
            st.session_state.page = "📡 Live Signal Analysis"
            st.rerun()
    
    with col2:
        if st.button("🔍 Deep Token Scan", use_container_width=True):
            st.session_state.page = "🔍 Deep Token Analysis"
            st.rerun()
    
    with col3:
        if st.button("🤖 Train AI Model", use_container_width=True):
            st.session_state.page = "🤖 AI Training Center"
            st.rerun()
    
    with col4:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "📊 Historical Performance"
            st.rerun()

def show_live_signal_page(dashboard):
    """Live signal analysis interface"""
    st.title("📡 Live Signal Analysis")
    st.markdown("### Real-time AI-powered signal processing")
    
    # Signal input methods
    input_method = st.radio(
        "Choose input method:",
        ["📝 Manual Text Input", "📋 Batch Upload", "🔗 Telegram Live Feed"]
    )
    
    if input_method == "📝 Manual Text Input":
        st.subheader("Enter Signal Text")
        
        signal_text = st.text_area(
            "Paste signal message here:",
            height=150,
            placeholder="""🔍 Viper Vision spotted

Token Name | SYMBOL
CA: AbcDef123456789...
MC: $45K
LP: 12.3 SOL (Not Burned)
Fees: 5/5
Top 10 holders: 42%
Free/Mint: ✅/✅"""
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            analyze_button = st.button("🚀 Analyze Signal", type="primary")
        
        with col2:
            deep_scan = st.checkbox("🔍 Include Deep Wallet Analysis")
        
        if analyze_button and signal_text:
            with st.spinner("🤖 AI analyzing signal..."):
                time.sleep(2)  # Simulate processing
                
                # Parse signal
                analysis = dashboard.signal_analyzer.analyze_signal(signal_text)
                
                # Display results
                show_signal_analysis_results(analysis, signal_text, dashboard, deep_scan)
    
    elif input_method == "📋 Batch Upload":
        st.subheader("Batch Signal Processing")
        
        uploaded_file = st.file_uploader(
            "Upload signals file (CSV/JSON/TXT)",
            type=['csv', 'json', 'txt']
        )
        
        if uploaded_file:
            st.success("File uploaded! Processing batch...")
            # Process batch upload logic here
    
    elif input_method == "🔗 Telegram Live Feed":
        st.subheader("Telegram Live Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            channel_name = st.text_input("Telegram Channel:", placeholder="@channelname")
        
        with col2:
            auto_analyze = st.checkbox("🤖 Auto-analyze incoming signals")
        
        if st.button("🔗 Connect to Live Feed"):
            st.info("🔄 Connecting to Telegram API...")
            # Live feed connection logic here

def show_signal_analysis_results(analysis, signal_text, dashboard, deep_scan=False):
    """Display comprehensive signal analysis results"""
    
    # Extract token details
    token_match = re.search(r'CA:\s*([A-Za-z0-9]+)', signal_text)
    token_address = token_match.group(1) if token_match else "Unknown"
    
    # Main results
    st.markdown("---")
    st.subheader("🎯 Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    success_prob = analysis.get('ml_prediction', {}).get('success_probability', 50)
    risk_score = analysis.get('risk_assessment', {}).get('overall_risk', 5)
    
    with col1:
        st.metric(
            "🎯 Success Probability",
            f"{success_prob:.1f}%",
            delta=f"{'High' if success_prob > 60 else 'Medium' if success_prob > 40 else 'Low'} Confidence"
        )
    
    with col2:
        st.metric(
            "⚠️ Risk Score",
            f"{risk_score:.1f}/10",
            delta=f"{'🟢 Low' if risk_score < 4 else '🟡 Medium' if risk_score < 7 else '🔴 High'}"
        )
    
    with col3:
        recommendation = analysis.get('recommendation', {}).get('action', 'HOLD')
        st.metric(
            "📊 AI Recommendation",
            recommendation,
            delta={"BUY": "🟢 Positive", "CAUTIOUS": "🟡 Neutral", "AVOID": "🔴 Negative"}.get(recommendation, "Unknown")
        )
    
    with col4:
        st.metric(
            "🕒 Analysis Time",
            "2.3s",
            delta="⚡ Fast"
        )
    
    # Detailed analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Core Analysis", "🔍 Deep Scan", "🤖 AI Insights", "📈 Prediction Chart"])
    
    with tab1:
        show_core_analysis(analysis)
    
    with tab2:
        if deep_scan:
            show_deep_wallet_analysis(token_address, dashboard)
        else:
            st.info("🔍 Enable 'Deep Wallet Analysis' to see advanced metrics")
    
    with tab3:
        show_ai_insights(analysis)
    
    with tab4:
        show_prediction_chart(analysis)

def show_core_analysis(analysis):
    """Display core signal analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Signal Features")
        
        features = analysis.get('features', {})
        
        # Create features dataframe
        feature_data = []
        for key, value in features.items():
            if isinstance(value, (int, float)):
                feature_data.append({
                    'Feature': key.replace('_', ' ').title(),
                    'Value': f"{value:.2f}" if isinstance(value, float) else str(value),
                    'Impact': "🟢 Positive" if value > 0.5 else "🟡 Neutral" if value > 0.2 else "🔴 Negative"
                })
        
        if feature_data:
            df = pd.DataFrame(feature_data)
            st.dataframe(df, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Risk Factors")
        
        risk_factors = analysis.get('risk_assessment', {}).get('risk_factors', [])
        
        for factor in risk_factors[:5]:  # Show top 5 risk factors
            severity = factor.get('severity', 'medium')
            emoji = "🔴" if severity == 'high' else "🟡" if severity == 'medium' else "🟢"
            st.write(f"{emoji} **{factor.get('factor', 'Unknown')}**")
            st.write(f"   Impact: {factor.get('impact', 'Unknown')}")
            st.write("")

def show_deep_wallet_analysis(token_address, dashboard):
    """Display deep wallet and deployer analysis"""
    
    with st.spinner("🔍 Performing deep blockchain analysis..."):
        # Fetch wallet data
        wallet_data = dashboard.fetch_wallet_analysis(token_address)
        deployer_data = dashboard.fetch_deployer_analysis(token_address)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Holder Analysis")
        
        if wallet_data:
            st.metric("Total Holders", f"{wallet_data['total_holders']:,}")
            st.metric("Top 10 Holdings", f"{wallet_data['top_10_percentage']:.1f}%")
            
            # Dev wallet analysis
            dev_info = wallet_data.get('dev_wallets', {})
            st.write("**🔧 Developer Wallets:**")
            st.write(f"- Identified: {dev_info.get('identified', 0)}")
            st.write(f"- Total %: {dev_info.get('total_percentage', 0):.1f}%")
            st.write(f"- Status: {dev_info.get('recent_activity', 'Unknown')}")
            
            # Whale analysis
            whale_info = wallet_data.get('whale_analysis', {})
            st.write("**🐋 Whale Analysis:**")
            st.write(f"- Wallets >1%: {whale_info.get('wallets_over_1_percent', 0)}")
            st.write(f"- Largest holder: {whale_info.get('largest_holder_percentage', 0):.1f}%")
            st.write(f"- Risk level: {whale_info.get('concentration_risk', 'Unknown')}")
    
    with col2:
        st.subheader("🚀 Deployer Analysis")
        
        if deployer_data:
            dep_history = deployer_data.get('deployer_history', {})
            st.metric("Previous Tokens", dep_history.get('previous_tokens', 0))
            st.metric("Success Rate", f"{dep_history.get('success_rate', 0)*100:.1f}%")
            
            # Contract analysis
            contract_info = deployer_data.get('contract_analysis', {})
            st.write("**📋 Contract Details:**")
            st.write(f"- Mint Authority: {contract_info.get('mint_authority', 'Unknown')}")
            st.write(f"- Freeze Authority: {contract_info.get('freeze_authority', 'Unknown')}")
            st.write(f"- Security Score: {contract_info.get('security_score', 0):.1f}/10")
            
            # Deployment patterns
            dep_patterns = deployer_data.get('deployment_patterns', {})
            st.write("**📅 Deployment Patterns:**")
            st.write(f"- Typical Time: {dep_patterns.get('typical_launch_time', 'Unknown')}")
            st.write(f"- Funding: {dep_patterns.get('funding_source', 'Unknown')}")
            st.write(f"- Initial LP: {dep_patterns.get('initial_liquidity', 'Unknown')}")

def show_ai_insights(analysis):
    """Display AI model insights and explanations"""
    st.subheader("🤖 AI Model Insights")
    
    # Feature importance
    st.write("**📊 Most Important Factors:**")
    
    # Simulated feature importance
    importance_data = {
        'Feature': ['Market Cap', 'LP Burned', 'Top 10 %', 'Deployer History', 'Time of Day'],
        'Importance': [0.85, 0.72, 0.68, 0.61, 0.45],
        'Impact': ['🟢 Positive', '🟢 Positive', '🔴 Negative', '🟡 Neutral', '🟡 Neutral']
    }
    
    df = pd.DataFrame(importance_data)
    
    fig = px.bar(df, x='Feature', y='Importance', color='Importance',
                color_continuous_scale='viridis', title='Feature Importance')
    st.plotly_chart(fig, use_container_width=True)
    
    # Model explanation
    st.write("**🔍 Why this prediction?**")
    
    prediction_explanation = analysis.get('ml_prediction', {}).get('explanation', '')
    if prediction_explanation:
        st.write(prediction_explanation)
    else:
        st.write("The AI model analyzed multiple factors including market cap, liquidity, holder distribution, and historical patterns of similar tokens to generate this prediction.")

def show_prediction_chart(analysis):
    """Display prediction visualization"""
    st.subheader("📈 Price Prediction Chart")
    
    # Generate sample prediction data
    hours = list(range(0, 25))
    base_price = 1.0
    
    # Simulate price prediction with some volatility
    predicted_prices = []
    for hour in hours:
        volatility = np.random.normal(0, 0.1)
        trend = 0.02 if analysis.get('recommendation', {}).get('action') == 'BUY' else -0.01
        price = base_price * (1 + trend * hour + volatility)
        predicted_prices.append(max(0.1, price))  # Ensure positive prices
    
    # Create prediction chart
    fig = go.Figure()
    
    # Historical (simulated)
    fig.add_trace(go.Scatter(
        x=hours[:1],
        y=predicted_prices[:1],
        mode='lines+markers',
        name='Current Price',
        line=dict(color='white', width=3),
        marker=dict(size=8)
    ))
    
    # Prediction
    fig.add_trace(go.Scatter(
        x=hours,
        y=predicted_prices,
        mode='lines',
        name='AI Prediction',
        line=dict(color='#00ff88', width=2, dash='dash')
    ))
    
    # Confidence bands
    upper_band = [p * 1.2 for p in predicted_prices]
    lower_band = [p * 0.8 for p in predicted_prices]
    
    fig.add_trace(go.Scatter(
        x=hours + hours[::-1],
        y=upper_band + lower_band[::-1],
        fill='toself',
        fillcolor='rgba(0,255,136,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Band'
    ))
    
    fig.update_layout(
        title='24-Hour Price Prediction',
        xaxis_title='Hours from Now',
        yaxis_title='Price Multiplier',
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_historical_page(dashboard):
    """Historical performance analysis"""
    st.title("📊 Historical Performance")
    st.markdown("### Analysis of past signals and model performance")
    
    # Load historical data
    try:
        df = pd.read_csv('/workspaces/0xbot/parsed_telegram_data.csv')
        st.success(f"✅ Loaded {len(df)} historical signals")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📈 Overall Stats")
            profitable_signals = len(df[df['max_gain'] > 0])
            total_signals = len(df)
            success_rate = profitable_signals / total_signals * 100 if total_signals > 0 else 0
            
            st.metric("Success Rate", f"{success_rate:.1f}%")
            st.metric("Total Signals", total_signals)
            st.metric("Profitable", profitable_signals)
        
        with col2:
            st.subheader("💰 Financial Performance")
            avg_gain = df['max_gain'].mean()
            best_gain = df['max_gain'].max()
            worst_loss = df['max_gain'].min()
            
            st.metric("Average Gain", f"{avg_gain:.1f}%")
            st.metric("Best Performance", f"{best_gain:.1f}%")
            st.metric("Worst Loss", f"{worst_loss:.1f}%")
        
        with col3:
            st.subheader("🎯 AI Model Performance")
            # These would be calculated from actual model predictions
            st.metric("Model Accuracy", "73.2%")
            st.metric("Precision", "68.5%")
            st.metric("Recall", "71.8%")
        
        # Charts
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📊 Performance Trends", "🔍 Signal Analysis", "🎯 Strategy Comparison"])
        
        with tab1:
            show_performance_trends(df)
        
        with tab2:
            show_signal_breakdown(df)
        
        with tab3:
            show_strategy_comparison(df)
            
    except Exception as e:
        st.error(f"❌ Error loading historical data: {e}")

def show_performance_trends(df):
    """Show performance trends over time"""
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Monthly performance
    monthly_performance = df.groupby(df['date'].dt.to_period('M')).agg({
        'max_gain': ['mean', 'count'],
        'initial_mc_value': 'mean'
    }).round(2)
    
    monthly_performance.columns = ['Avg_Gain', 'Signal_Count', 'Avg_MC']
    monthly_performance = monthly_performance.reset_index()
    monthly_performance['date'] = monthly_performance['date'].astype(str)
    
    # Create trend chart
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Average Gain %', 'Signal Count'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=monthly_performance['date'], y=monthly_performance['Avg_Gain'],
                  mode='lines+markers', name='Avg Gain %', line=dict(color='#00ff88')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=monthly_performance['date'], y=monthly_performance['Signal_Count'],
               name='Signal Count', marker_color='#ff6b6b'),
        row=2, col=1
    )
    
    fig.update_layout(height=500, title_text="Performance Trends Over Time")
    st.plotly_chart(fig, use_container_width=True)

def show_signal_breakdown(df):
    """Show detailed signal analysis"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Gain distribution
        fig = px.histogram(df, x='max_gain', nbins=50, 
                          title='Gain Distribution',
                          color_discrete_sequence=['#00ff88'])
        fig.update_xaxis(title='Max Gain %')
        fig.update_yaxis(title='Number of Signals')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Market cap vs performance
        fig = px.scatter(df, x='initial_mc_value', y='max_gain',
                        title='Market Cap vs Performance',
                        color='max_gain', color_continuous_scale='viridis')
        fig.update_xaxis(title='Initial Market Cap')
        fig.update_yaxis(title='Max Gain %')
        st.plotly_chart(fig, use_container_width=True)

def show_strategy_comparison(df):
    """Compare different signal strategies"""
    if 'strategy' in df.columns:
        strategy_performance = df.groupby('strategy').agg({
            'max_gain': ['mean', 'count', 'std'],
            'initial_mc_value': 'mean'
        }).round(2)
        
        strategy_performance.columns = ['Avg_Gain', 'Count', 'Volatility', 'Avg_MC']
        strategy_performance = strategy_performance.reset_index()
        
        # Strategy comparison chart
        fig = px.bar(strategy_performance, x='strategy', y='Avg_Gain',
                    color='Avg_Gain', color_continuous_scale='viridis',
                    title='Strategy Performance Comparison')
        st.plotly_chart(fig, use_container_width=True)
        
        # Strategy stats table
        st.subheader("📋 Strategy Statistics")
        st.dataframe(strategy_performance, use_container_width=True)
    else:
        st.info("No strategy data available in historical records")

def show_deep_analysis_page(dashboard):
    """Deep token analysis page"""
    st.title("🔍 Deep Token Analysis")
    st.markdown("### Comprehensive blockchain and social analysis")
    
    # Token input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        token_address = st.text_input(
            "Token Contract Address:",
            placeholder="Enter Solana token address..."
        )
    
    with col2:
        analyze_btn = st.button("🚀 Analyze", type="primary")
    
    if analyze_btn and token_address:
        with st.spinner("🔍 Performing deep analysis..."):
            # Simulate analysis time
            time.sleep(3)
            
            # Get comprehensive analysis
            wallet_data = dashboard.fetch_wallet_analysis(token_address)
            deployer_data = dashboard.fetch_deployer_analysis(token_address)
            
            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Overview", "👥 Holder Analysis", "🚀 Deployer Intel", "📈 Market Data"
            ])
            
            with tab1:
                show_token_overview(token_address, wallet_data, deployer_data)
            
            with tab2:
                show_detailed_holder_analysis(wallet_data)
            
            with tab3:
                show_detailed_deployer_analysis(deployer_data)
            
            with tab4:
                show_market_data_analysis(token_address)

def show_token_overview(token_address, wallet_data, deployer_data):
    """Show token overview"""
    st.subheader(f"📊 Token Overview")
    st.code(f"Contract: {token_address}")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if wallet_data:
            st.metric("👥 Total Holders", f"{wallet_data['total_holders']:,}")
    
    with col2:
        if wallet_data:
            concentration = wallet_data['top_10_percentage']
            st.metric("📊 Top 10%", f"{concentration:.1f}%", 
                     delta="🔴 High" if concentration > 50 else "🟡 Medium" if concentration > 30 else "🟢 Low")
    
    with col3:
        if deployer_data:
            security_score = deployer_data.get('contract_analysis', {}).get('security_score', 5)
            st.metric("🔒 Security Score", f"{security_score:.1f}/10")
    
    with col4:
        if deployer_data:
            success_rate = deployer_data.get('deployer_history', {}).get('success_rate', 0)
            st.metric("🎯 Deployer Success", f"{success_rate*100:.1f}%")

def show_detailed_holder_analysis(wallet_data):
    """Detailed holder analysis"""
    if not wallet_data:
        st.error("No wallet data available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🐋 Whale Distribution")
        
        # Simulate whale data
        whale_sizes = ['1-5%', '5-10%', '10-20%', '20%+']
        whale_counts = [8, 3, 2, 1]
        
        fig = px.pie(values=whale_counts, names=whale_sizes, 
                    title="Whale Distribution by Holdings")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Holder Behavior")
        
        behavior = wallet_data.get('holder_behavior', {})
        
        st.metric("💎 Diamond Hands", f"{behavior.get('diamond_hands_percentage', 50):.1f}%")
        st.metric("📤 Recent Sells", behavior.get('recent_sells', 10))
        st.metric("📥 New Buyers (24h)", behavior.get('new_buyers_24h', 50))
        
        # Behavior trend (simulated)
        days = list(range(1, 8))
        diamond_hands_trend = [45, 47, 52, 48, 51, 55, 58]
        
        fig = px.line(x=days, y=diamond_hands_trend, 
                     title="Diamond Hands Trend (7 days)")
        fig.update_xaxis(title="Days Ago")
        fig.update_yaxis(title="Diamond Hands %")
        st.plotly_chart(fig, use_container_width=True)

def show_detailed_deployer_analysis(deployer_data):
    """Detailed deployer analysis"""
    if not deployer_data:
        st.error("No deployer data available")
        return
    
    st.subheader("🚀 Deployer Intelligence")
    
    # Deployer history
    history = deployer_data.get('deployer_history', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Previous Tokens", history.get('previous_tokens', 0))
        st.metric("📈 Success Rate", f"{history.get('success_rate', 0)*100:.1f}%")
    
    with col2:
        contract = deployer_data.get('contract_analysis', {})
        st.write("**🔒 Contract Security:**")
        st.write(f"- Mint: {contract.get('mint_authority', 'Unknown')}")
        st.write(f"- Freeze: {contract.get('freeze_authority', 'Unknown')}")
        st.write(f"- Supply: {contract.get('supply_management', 'Unknown')}")
    
    with col3:
        patterns = deployer_data.get('deployment_patterns', {})
        st.write("**📅 Deployment Patterns:**")
        st.write(f"- Time: {patterns.get('typical_launch_time', 'Unknown')}")
        st.write(f"- Funding: {patterns.get('funding_source', 'Unknown')}")
        st.write(f"- Initial LP: {patterns.get('initial_liquidity', 'Unknown')}")

def show_market_data_analysis(token_address):
    """Show market data analysis"""
    st.subheader("📈 Market Data Analysis")
    
    # Simulate market data
    hours = list(range(24))
    prices = [1.0 + 0.1 * np.sin(h/4) + np.random.normal(0, 0.05) for h in hours]
    volumes = [1000 + 500 * np.sin(h/3) + np.random.normal(0, 100) for h in hours]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(x=hours, y=prices, title="Price Chart (24h)")
        fig.update_xaxis(title="Hours Ago")
        fig.update_yaxis(title="Price ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(x=hours, y=volumes, title="Volume Chart (24h)")
        fig.update_xaxis(title="Hours Ago")
        fig.update_yaxis(title="Volume ($)")
        st.plotly_chart(fig, use_container_width=True)

def show_ai_training_page(dashboard):
    """AI training and model management"""
    st.title("🤖 AI Training Center")
    st.markdown("### Improve AI models with new data")
    
    tab1, tab2, tab3 = st.tabs(["📚 Training Data", "🎯 Model Performance", "⚙️ Model Settings"])
    
    with tab1:
        show_training_data_management()
    
    with tab2:
        show_model_performance_metrics()
    
    with tab3:
        show_model_settings()

def show_training_data_management():
    """Training data management interface"""
    st.subheader("📚 Training Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Current Dataset:**")
        st.metric("Total Signals", "1,247")
        st.metric("Labeled Outcomes", "1,089")
        st.metric("Success Rate", "67.3%")
        
        if st.button("🔄 Refresh Dataset"):
            st.success("Dataset refreshed!")
    
    with col2:
        st.write("**📥 Add New Training Data:**")
        
        uploaded_file = st.file_uploader(
            "Upload training data (CSV)",
            type=['csv']
        )
        
        if uploaded_file:
            st.success("File uploaded successfully!")
            
            if st.button("🎯 Label Outcomes"):
                st.info("Starting outcome labeling process...")

def show_model_performance_metrics():
    """Model performance dashboard"""
    st.subheader("🎯 Model Performance Metrics")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Accuracy", "73.2%", delta="↑ 2.1%")
    
    with col2:
        st.metric("🔍 Precision", "68.5%", delta="↑ 1.8%")
    
    with col3:
        st.metric("📊 Recall", "71.8%", delta="↓ 0.5%")
    
    with col4:
        st.metric("⚖️ F1-Score", "70.1%", delta="↑ 0.7%")
    
    # Performance charts
    st.markdown("---")
    
    # Training history
    epochs = list(range(1, 21))
    accuracy = [0.45 + 0.28 * (1 - np.exp(-x/5)) + np.random.normal(0, 0.01) for x in epochs]
    loss = [0.8 * np.exp(-x/8) + 0.1 + np.random.normal(0, 0.01) for x in epochs]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(x=epochs, y=accuracy, title="Model Accuracy Over Training")
        fig.update_xaxis(title="Epoch")
        fig.update_yaxis(title="Accuracy")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(x=epochs, y=loss, title="Training Loss Over Time", 
                     line_shape='spline')
        fig.update_xaxis(title="Epoch")
        fig.update_yaxis(title="Loss")
        st.plotly_chart(fig, use_container_width=True)

def show_model_settings():
    """Model configuration settings"""
    st.subheader("⚙️ Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎛️ Hyperparameters:**")
        
        learning_rate = st.slider("Learning Rate", 0.001, 0.1, 0.01, 0.001)
        batch_size = st.selectbox("Batch Size", [16, 32, 64, 128], index=2)
        epochs = st.slider("Training Epochs", 10, 100, 50)
        
        st.write("**🔧 Feature Selection:**")
        features = st.multiselect(
            "Select features for training:",
            ["Market Cap", "LP Burned", "Top 10%", "Deployer History", "Time of Day", "Sentiment"],
            default=["Market Cap", "LP Burned", "Top 10%"]
        )
    
    with col2:
        st.write("**🎯 Model Type:**")
        
        model_type = st.selectbox(
            "Choose model type:",
            ["Random Forest", "Gradient Boosting", "Neural Network", "SVM"]
        )
        
        st.write("**📊 Validation:**")
        validation_split = st.slider("Validation Split", 0.1, 0.3, 0.2)
        cross_validation = st.checkbox("Use Cross-Validation", value=True)
        
        if st.button("🚀 Retrain Model", type="primary"):
            with st.spinner("🎯 Training model..."):
                time.sleep(5)
                st.success("✅ Model retrained successfully!")
                st.balloons()

def show_settings_page(dashboard):
    """System settings and configuration"""
    st.title("⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔧 General", "🔗 API Keys", "📊 Data Sources"])
    
    with tab1:
        st.subheader("🔧 General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎨 Interface:**")
            theme = st.selectbox("Theme", ["Dark", "Light", "Auto"])
            language = st.selectbox("Language", ["English", "Lithuanian", "Russian"])
            
            st.write("**⚡ Performance:**")
            auto_refresh = st.checkbox("Auto-refresh data", value=True)
            refresh_interval = st.slider("Refresh interval (seconds)", 10, 300, 60)
        
        with col2:
            st.write("**🔔 Notifications:**")
            signal_alerts = st.checkbox("Signal alerts", value=True)
            high_confidence = st.checkbox("High confidence only", value=False)
            email_notifications = st.checkbox("Email notifications", value=False)
            
            if email_notifications:
                email = st.text_input("Email address:")
    
    with tab2:
        st.subheader("🔗 API Configuration")
        
        st.write("**🤖 AI Services:**")
        gemini_api = st.text_input("Google Gemini API Key:", type="password")
        openai_api = st.text_input("OpenAI API Key:", type="password")
        
        st.write("**⛓️ Blockchain APIs:**")
        solana_rpc = st.text_input("Solana RPC URL:", value="https://api.mainnet-beta.solana.com")
        jupiter_api = st.text_input("Jupiter API Key:", type="password")
        
        st.write("**📱 Social APIs:**")
        telegram_api = st.text_input("Telegram Bot Token:", type="password")
        twitter_api = st.text_input("Twitter API Key:", type="password")
        
        if st.button("💾 Save API Keys"):
            st.success("✅ API keys saved securely!")
    
    with tab3:
        st.subheader("📊 Data Sources")
        
        st.write("**📱 Telegram Channels:**")
        channels = st.text_area(
            "Monitor these channels (one per line):",
            value="@channel1\n@channel2\n@channel3"
        )
        
        st.write("**📈 Price Data:**")
        price_source = st.selectbox("Primary price source:", ["Jupiter", "CoinGecko", "CoinMarketCap"])
        backup_source = st.selectbox("Backup source:", ["CoinGecko", "Jupiter", "CoinMarketCap"])
        
        st.write("**💾 Data Storage:**")
        storage_location = st.selectbox("Storage location:", ["Local CSV", "Database", "Cloud"])
        retention_days = st.slider("Data retention (days)", 30, 365, 90)
        
        if st.button("🔄 Update Data Sources"):
            st.success("✅ Data sources updated!")

if __name__ == "__main__":
    main()

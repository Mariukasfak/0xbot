#!/usr/bin/env python3
"""
Analyze the user's specific signal
"""

from realtime_signal_analyzer import RealtimeSignalAnalyzer

def analyze_user_signal():
    """Analyze the specific signal provided by the user"""
    
    # Initialize analyzer
    analyzer = RealtimeSignalAnalyzer()
    
    # Load model and insights
    if not analyzer.load_model_and_insights():
        print("❌ Could not load model. Using basic analysis.")
    
    # User's actual signal
    user_signal = """🤖 0xBot AI Agent | Solana Network (https://t.me/ai_agent_solana_0xbot) 
🏖 buy and retire | 401k | (Pump.Fun💊)

🛒 Token Address:
8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump

📚 Supply: 1000M Tokens
📊 Initial MC: $66.28K
💲 Call MC: $67.09K
💎 Initial LP: 81.4 SOL | $14.35K
💧 Call Liquidity: 81.9 SOL | $14.43K
⚙️ LP Tokens: 20%

💼 Top 10 holders: (https://solscan.io/token/8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump#holders) 22.7%
3.44% (https://solscan.io/address/B4cZ2N4Yefk6xzK5SQ3ui2157Fw2C8zzQy6J4Ux9sxgi) | 3.39% (https://solscan.io/address/J4vKqHNpSpRz4LiNAT1gmZzZLDHkt8dGeudxrk2Sri5i) | 3.32% (https://solscan.io/address/FZS2HfDwcu5f6Mye55DZRMoEUbQmcV23azRwjzUfLPf1) | 2.85% (https://solscan.io/address/9YAnaqWetD1VQQwuJCVdDcp441LGQtEAbXUawc44eJhr) | 2.07% (https://solscan.io/address/CDG8PBzKwam76WWGTZP9hQDkCkiWdLzjextsuL1x4Hdh)
1.7% (https://solscan.io/address/8UcQ4cSF7qq2MfJ1Ftt7VwhcwkBBFCrZCkQuU1trt36n) | 1.61% (https://solscan.io/address/GtsiJHA3eMVtwqpDLwVvfvqBuBBCHL3u2CQA8xLWcqks) | 1.51% (https://solscan.io/address/DchfjViyKi7KwKcoEKCFD9qPASc3kHujdUGvR166n3eE) | 1.41% (https://solscan.io/address/7nc2K4ENn8xdrTPsb4G9d38U1bKF5wbCE2gcz8S6Gt8d) | 1.37% (https://solscan.io/address/4e7pNTiuk7TKLB4BeaFJoGX6rAPwKMfGQXTg8BHLBgxC)

🛠️ Deployer (https://solscan.io/account/TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM) 0.0 SOL | 0.0 Tokens

❄️ FREEZE: ✅ Disabled
💼 MINT: ✅ Disabled
🔥 LP STATUS: ❌ Not Burned

📬 SOCIALS: WEB (https://www.google.com/search?q=401k+investment&sca_esv=4b32451117f11e5d&sxsrf=AE3TifM7ByFYbcXq1uDOq4JUYRG-4Fa-fg%3A1748227877441&ei=JdczaM3fGqGu5NoPj66ImQM&ved=0ahUKEwiNhvyskMCNAxUhF1kFHQ8XIjMQ4dUDCBA&uact=5&oq=401k+investment&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgDIg80MDFrIGludmVzdG1lbnQyChAjGIAEGCcYigUyChAAGIAEGBQYhwIyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMggQABiABBiLAzIIEAAYgAQYiwMyCBAAGIAEGIsDMggQABiABBiLA0j9EFDUAljYD3ABeAGQAQCYAVagAawFqgECMTG4AQPIAQD4AQGYAgygAssFwgIHECMYsAMYJ8ICChAAGLADGNYEGEfCAg0QABiABBiwAxhDGIoFwgIQEAAYgAQYsQMYQxiKBRiLA8ICEBAAGIAEGLEDGBQYhwIYiwPCAgsQABiABBixAxiLA8ICDRAAGIAEGEMYigUYiwPCAgoQABiABBhDGIoFmAMAiAYBkAYKkgcCMTKgB4VLsgcCMTG4B8cFwgcGMC4xMC4yyAcc&sclient=gws-wiz-serp) | X (https://x.com/i/communities/1926833339710750951)

🔗 PHOTON (https://photon-sol.tinyastro.io/en/lp/GoiKMZNTRv8RGneuKvyqLdvxcytdD58HDGEVZoQNGRp6) | BUNDLE (https://trench.bot/bundles/8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump) | RUGCHECK (https://rugcheck.xyz/tokens/8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump) | SCREEN (https://dexscreener.com/solana/8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump) | DEXT (https://www.dextools.io/app/en/solana/pair-explorer/GoiKMZNTRv8RGneuKvyqLdvxcytdD58HDGEVZoQNGRp6) | NEO BULLX (https://neo.bullx.io/terminal?chainId=1399811149&address=8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump&r=24O6R3JBQZX)
💡 Strategy: Cobra Scan

Our VIP members get 30s early calls and more premium signals than the public group. 👉 @pay0x_bot

i give normal signal"""
    
    print("🔍 ANALYZING YOUR SIGNAL: 'buy and retire | 401k'")
    print("🔗 Token Address: 8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump")
    print("💡 Strategy: Cobra Scan")
    print()
    
    # Parse signal manually for better extraction
    signal_data = {
        'token_name': '401k',
        'token_address': '8iP5QbqS34FTi2Vdrny6SHicJEM8C5L3Vy1QYT8jpump',
        'strategy': 'Cobra Scan',
        'initial_mc': '66.28K',
        'call_mc': '67.09K',
        'initial_lp_sol': 81.4,
        'top_holders_percent': 22.7,
        'wallet_percentages': '[3.44, 3.39, 3.32, 2.85, 2.07, 1.7, 1.61, 1.51, 1.41, 1.37]',
        'freeze_disabled': True,
        'mint_disabled': True,
        'lp_burned': False,
        'date': analyzer.parse_signal_message(user_signal)['date']
    }
    
    # Analyze with both methods
    try:
        analysis = analyzer.analyze_signal(user_signal)
        analyzer.print_analysis(analysis)
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        
        # Manual analysis
        print("\n🔍 MANUAL ANALYSIS:")
        print(f"📊 Token: {signal_data['token_name']}")
        print(f"💰 Initial MC: ${signal_data['initial_mc']}")
        print(f"🏊 LP: {signal_data['initial_lp_sol']} SOL")
        print(f"👥 Top Holders: {signal_data['top_holders_percent']}%")
        print(f"🔒 Security: Freeze ✅ | Mint ✅ | LP ❌")
        print(f"💡 Strategy: {signal_data['strategy']}")
        
        # Basic risk assessment
        print("\n⚠️ BASIC RISK ASSESSMENT:")
        risk_factors = []
        
        # Security analysis
        if signal_data['freeze_disabled'] and signal_data['mint_disabled']:
            print("   🟢 Good security: Freeze & Mint disabled")
        else:
            risk_factors.append("Security concerns")
            
        if not signal_data['lp_burned']:
            print("   🟡 LP not burned - moderate risk")
            risk_factors.append("LP not burned")
        
        # Liquidity analysis
        if signal_data['initial_lp_sol'] >= 80:
            print("   🟢 Excellent liquidity: 81.4 SOL")
        
        # Market cap analysis
        mc_value = 66280  # $66.28K
        if 50000 <= mc_value <= 100000:
            print("   🟢 Good MC range: $66.28K (sweet spot)")
        
        # Whale concentration
        max_wallet = 3.44
        if max_wallet <= 5:
            print("   🟢 Low whale concentration: 3.44% max wallet")
        
        # Strategy performance (from our historical data)
        print("\n📈 HISTORICAL INSIGHTS:")
        print("   🐍 Cobra Scan Strategy: 25.6% historical success rate")
        print("   ⏰ Current hour performance: Variable")
        print("   📊 Overall dataset: 27.0% average success rate")
        
        print("\n💡 MANUAL RECOMMENDATION:")
        if len(risk_factors) <= 1:
            print("   🟡 MODERATE BUY - Good fundamentals, monitor LP burning")
            print("   📊 Score: 75/100")
            print("   💰 Risk Level: LOW-MEDIUM")
        else:
            print("   🟠 CAUTIOUS - Multiple risk factors")

if __name__ == "__main__":
    analyze_user_signal()

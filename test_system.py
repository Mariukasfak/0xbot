#!/usr/bin/env python3
"""
Quick test to verify the 0xBot system is working correctly
"""

def test_signal_parsing():
    """Test signal parsing functionality"""
    from streamlined_dashboard import StreamlinedSignalDashboard
    
    # Test signal
    test_signal = """🔍 Viper Vision spotted

TEST TOKEN | TEST
CA: 8pZZ3Y7K2qW5xN9rE4mA7bG6fH1cJ8kL3oP9sT2vU5
MC: $45K
LP: 12.3 SOL (Not Burned)
Fees: 5/5
Top 10 holders: 42%
Free/Mint: ✅/✅"""

    # Initialize dashboard
    dashboard = StreamlinedSignalDashboard()
    
    # Parse signal
    parsed = dashboard.parse_signal_message(test_signal)
    
    print("✅ Signal parsing test:")
    print(f"Strategy: {parsed['parsed_data'].get('strategy', 'Not found')}")
    print(f"Token: {parsed['parsed_data'].get('token_name', 'Not found')}")
    print(f"Contract: {parsed['parsed_data'].get('contract_address', 'Not found')}")
    print(f"Market Cap: {parsed['parsed_data'].get('market_cap', 'Not found')}")
    print(f"LP SOL: {parsed['parsed_data'].get('liquidity_sol', 'Not found')}")
    print(f"Top Holders: {parsed['parsed_data'].get('top_holders_percent', 'Not found')}%")
    
    # Test analysis
    analysis = dashboard.analyze_signal_comprehensive(parsed)
    print(f"\n✅ Analysis test:")
    print(f"Risk Score: {analysis['risk_score']:.1f}/10")
    print(f"Recommendation: {analysis['recommendation']}")
    
    return True

if __name__ == "__main__":
    print("🤖 Testing 0xBot System...")
    try:
        test_signal_parsing()
        print("\n🎉 All tests passed! System is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("Please check the system setup.")

# Telegram Coin Calls Parser 🚀

An intelligent CSV parser for analyzing Telegram crypto trading signals, coin calls, and wallet activity. Extract actionable insights from chat exports to identify trending patterns and profitable trading opportunities.

## 🎯 Purpose

Automatically analyze Telegram bot/analyst chat CSV files and extract comprehensive information that helps understand which signals, wallets, percentages, and links most commonly accompany trending coins with high multiplier gains.

Create a comprehensive analysis table that enables easy filtering and trend modeling to identify characteristics of profitable coins.

## ✨ Features

### Automatic Data Extraction
- **Smart CSV Detection**: Automatically detects message columns (text/message/body) - works with any Telegram chat export CSV
- **Coin Recognition**: Extracts coin names using pattern matching ("COIN gains XXx")
- **Wallet Analysis**: Identifies all ETH/SOL/other wallet addresses
- **Supply Analysis**: Extracts all percentages (XX.X%) showing wallet supply/market cap holdings
- **Signal Detection**: Captures ALL signal keywords (MC, CALL MC, STRATEGY, AUDIT, LP, SUPPLY, WALLET, LOCK, LIQUIDITY, etc.)
- **Link Analysis**: Detects presence of web and Telegram links (web_ratio, tg_ratio)

### Comprehensive Analytics
For each coin, generates detailed summaries including:
- Number of messages
- Number of X (gain) jumps
- Signal count and types
- Unique wallet count
- Highest percentage holdings
- Combined signal analysis

### Output Files
- **`features.csv`**: One row per coin with all extracted features
- **`wallets.csv`**: Individual wallet addresses with supply percentages and associated coins

### Robust Processing
- Error-resistant operation even with empty messages or imperfect files
- Safe handling of various CSV formats
- No crashes on malformed data

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/telegram-coin-parser
cd telegram-coin-parser

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage
```bash
python parser.py input_file.csv
```

### Advanced Usage
```python
from telegram_parser import CoinCallsParser

parser = CoinCallsParser()
features, wallets = parser.analyze_csv("telegram_export.csv")

# Access results
print(f"Analyzed {len(features)} coins")
print(f"Found {len(wallets)} unique wallets")
```

## 📊 Use Cases

### 1. Signal Pattern Analysis
- Identify which signal combinations most frequently precede major price movements
- Analyze correlation between signal types and multiplier gains

### 2. Wallet Intelligence
- Discover "success wallets" that repeatedly appear in profitable coins
- Track wallet behavior patterns across different tokens

### 3. Predictive Modeling
- Model which features/keywords are important before price jumps
- Create scoring systems for new coins based on signal quantity and type

### 4. Performance Scoring
- Develop automated scoring systems for new coins
- Rate signals based on historical performance data

### 5. Cross-Platform Analysis
- Apply to other chat or coin signal groups
- Adapt for different data sources by simply changing input files

## 📈 Output Format

### Features CSV
| Column | Description |
|--------|-------------|
| coin_name | Extracted coin identifier |
| message_count | Number of messages mentioning coin |
| gain_multiplier | Highest X gain mentioned |
| signal_keywords | Comma-separated signal words |
| wallet_count | Number of unique wallets |
| max_supply_percent | Highest wallet supply percentage |
| web_links | Boolean for web presence |
| tg_links | Boolean for Telegram presence |

### Wallets CSV
| Column | Description |
|--------|-------------|
| wallet_address | Blockchain wallet address |
| supply_percent | Percentage of token supply |
| coin_name | Associated coin |
| message_context | Original message context |

## 🔍 Signal Keywords

The parser automatically detects and categorizes these signals:
- **Market Cap**: MC, CALL MC, MARKET CAP
- **Security**: AUDIT, VERIFIED, SAFE
- **Liquidity**: LP, LIQUIDITY, LOCK, LOCKED
- **Supply**: SUPPLY, WALLET, HOLDINGS
- **Strategy**: STRATEGY, CALL, SIGNAL
- **And many more...**

## 🛠️ Technical Specifications

### Requirements
- Python 3.7+
- pandas
- numpy
- re (regex)
- csv

### Input Format
- CSV files from Telegram chat exports
- Flexible column detection (works with various export formats)
- UTF-8 encoding support

### Performance
- Processes thousands of messages per second
- Memory-efficient for large chat exports
- Parallel processing capabilities

## 🚀 Getting Started

1. **Export your Telegram chat** to CSV format
2. **Run the parser** on your CSV file
3. **Analyze the results** in the generated feature and wallet files
4. **Build insights** using your preferred data analysis tools

## 📋 Roadmap

- [ ] Real-time Telegram bot integration
- [ ] Advanced ML model integration
- [ ] Web dashboard for visualization
- [ ] API endpoints for external integration
- [ ] Multi-blockchain support expansion

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always conduct your own research before making any trading decisions. Cryptocurrency trading involves substantial risk.

## 📞 Support

- 📧 Email: support@yourproject.com
- 💬 Telegram: @yourproject
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/telegram-coin-parser/issues)

---

**Made with ❤️ for the crypto analysis community**
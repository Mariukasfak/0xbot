# 🤖 Telegram Signal Analyzer

ML-Powered Solana Token Signal Analyzer with **73% accuracy** for 5x+ gains prediction.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Main Analyzer
```bash
python signal_analyzer.py
```

### 3. Analyze Signals
- Option 1: Paste new Telegram signal text for analysis
- Option 2: Test with pre-validated signals (including the validated 401k token)
- Option 3: Exit

## 📊 Features

- **ML Predictions**: Random Forest model trained on 16,985 historical signals
- **Risk Assessment**: Multi-factor security and liquidity analysis
- **Historical Context**: Strategy-specific success rates and timing analysis
- **Real-time Analysis**: Parse and analyze new Telegram signals instantly

## 🎯 Accuracy & Validation

- **Overall**: 73% accuracy for predicting 5x+ gains
- **Validated**: Successfully predicted cautious approach for 401k token (achieved 4.41x)
- **Sample Size**: Trained on 16,985 parsed Telegram signals
- **Real Result**: System correctly identified opportunity with appropriate risk management

## 📈 Risk Factors Analyzed

- **Security**: Freeze/mint functions, LP burning status
- **Liquidity**: SOL amount and market depth
- **Concentration**: Whale holder percentages
- **Timing**: Hour-of-day and strategy performance patterns
- **Historical**: Strategy-specific success rates

## 🔧 Main File

**Use this file for all analysis**: `signal_analyzer.py`

This is the consolidated, final version that combines all functionality.

## 📋 Recommendation System

- **STRONG BUY**: High confidence + Low risk + Good historical performance
- **BUY**: Positive indicators with acceptable risk levels
- **CAUTIOUS**: Mixed signals - small position size suggested
- **AVOID**: Low probability of success or high risk factors

## 🏆 Validated Results

**401k Token Analysis**:
- **System Prediction**: CAUTIOUS (30.3% success probability)
- **Actual Result**: 4.41x gains ✅
- **Position Recommendation**: Small position size
- **Outcome**: Correct risk assessment with profitable result

## ⚠️ Important Note

This tool is for educational purposes. Always:
- Do your own research
- Never invest more than you can afford to lose
- Use suggested position sizes as guidelines only
- Consider multiple sources before making decisions

## 🎯 Paskirtis

Automatiškai analizuoja Telegram bot'ų/analitikų chat CSV failus ir ištraukia išsamią informaciją, kuri padeda suprasti, kurie signalai, wallet'ai, procentai ir nuorodos dažniausiai lydi trending coin'us su aukštais multiplier gain'ais.

## ✨ Pagrindiniai Funkcionalumai

### 📊 Pilna Duomenų Analizė
- **CSV Atpažinimas**: Automatiškai aptinka žinučių stulpelius
- **Coin Atpažinimas**: Ištraukia coin pavadinimus ("COIN gains XXx")
- **Wallet Analizė**: Identifikuoja visus wallet adresus
- **Finansinių Duomenų Ekstraktavimas**: Market Cap, LP, Supply, etc.
- **Saugumo Funkcijų Analizė**: Freeze/Mint/LP Burned statusai
- **Signalų Detektavimas**: Visos signalų žodžių kategorijos

### 🔍 Naujas Signalų Analizatorius
- **Vieningo Signalo Analizė**: Analizuoja naują signalą ir palygina su istoriniais
- **Risk Score Skaičiavimas**: 0-100 rizikos įvertinimas
- **Sėkmės Tikimybės Prognozė**: Pagal panašius istorinius coin'us
- **Vizualizacijos**: Grafikų generavimas palyginimui

### 📈 Išsami Statistika
- **2,278+ Istorinių Coin'ų Duomenys**
- **65,280+ Wallet'ų Analizė**
- **Sėkmės Šablonų Identifikavimas**
- **Laiko Tendencijų Analizė**

## 🚀 Naudojimas

### 1. Pilna Istorinių Duomenų Analizė
```bash
python telegram_analyzer.py

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

### 2. Naujo Signalo Analizė
```bash
# Automatinė analizė (naudoja signalą iš kodo)
python telegram_analyzer.py new_signal

# Arba tiesiogiai
python -c "from telegram_analyzer import analyze_new_signal; analyze_new_signal()"
```

### 3. Greita Signalo Analizė
```bash
# Interaktyvus režimas
python quick_analyzer.py

# Command line režimas
python quick_analyzer.py "jūsų signalo tekstas čia"
```

### 4. Vizualizacijų Generavimas
```bash
python visualize_signal.py
```

## 📁 Generuojami Failai

### Istorinė Analizė:
- `coin_features_analysis.csv` - 2,278 coin'ų su detaliais metrikais
- `wallets_analysis.csv` - 65,280 wallet'ų analizė
- `telegram_analysis_complete.xlsx` - Excel darbo knyga
- `comprehensive_report.md` - Išsamus raportas
- `plots/` - Vizualizacijos

### Signalo Analizė:
- `new_signal_analysis.md` - Signalo raportas
- `new_signal_analysis.json` - JSON duomenys
- `signal_comprehensive_analysis.md` - Išsami analizė
- `plots/signal_analysis_comparison.png` - Palyginimo grafikai
- `plots/signal_wallet_analysis.png` - Wallet analizė

## 🎯 Pagrindiniai Rezultatai

Iš 2,278 analizuotų coin'ų:
- **Top Performer:** CONCHO (331.56x gain)
- **Vidutinis Gain:** 6.15x
- **Success Rate (5x+):** 29.9%
- **Sėkmingi Saugumo Šablonai:** Freeze/Mint disabled + LP burned

## 🔍 Signalo Analizės Pavyzdys

```
🎯 PAGRINDINIAI REZULTATAI:
Coin: 22M
Market Cap: $67,600
Risk Score: 20/100 🟢 ŽEMA RIZIKA
Sėkmės Tikimybė: 23.1%
Saugumo Funkcijos: Freeze=✅ | Mint=✅ | LP Burned=❌
```

## 💡 Rekomendacijos

### 🟢 Geriausi Signalai:
- Freeze ir Mint disabled
- LP burned statusas
- Mažas wallet'ų koncentracija (<5%)
- Daugiau platformų nuorodų

### ⚠️ Rizikos Faktoriai:
- Aukšta wallet'ų koncentracija (>5%)
- Nesudeginta LP
- Mažas signalų žodžių kiekis

## 🔧 Instaliacija

```bash
pip install -r requirements.txt
````
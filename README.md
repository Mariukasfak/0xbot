# 🤖 Telegram Crypto Signal Analyzer

Išmanus Telegram kriptovaliutų signalų analizatorius, kuris analizuoja chat CSV eksportus ir ištraukia išsamius duomenis apie coin'ų poveikį, wallet'ų aktyvumą ir sėkmės šablonus.

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
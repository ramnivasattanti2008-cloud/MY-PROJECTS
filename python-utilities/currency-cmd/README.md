# Currency CMD

A colorful command-line currency converter using free exchange rate APIs.

## Features

- **Convert currencies**: Convert any amount between two currencies
- **Exchange rates**: View all rates for a base currency
- **Popular rates**: Quick view of common currency pairs
- **Compare**: Compare one currency against multiple others
- **List currencies**: See all supported currencies
- **Colorful output**: Colorama-styled terminal display

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Convert Currency
```bash
# Basic conversion
python currency-cmd.py convert 100 USD EUR

# Convert to INR
python currency-cmd.py convert 50 EUR INR

# Convert any amount
python currency-cmd.py convert 1000 GBP JPY
```

### View Exchange Rates
```bash
# All rates for USD
python currency-cmd.py rates USD

# All rates for EUR
python currency-cmd.py rates EUR

# All rates for INR
python currency-cmd.py rates INR
```

### Popular Rates
```bash
python currency-cmd.py popular
```

### Compare Currencies
```bash
python currency-cmd.py compare USD EUR GBP JPY INR
```

### List Supported Currencies
```bash
python currency-cmd.py list
```

## Supported Currencies

| Code | Currency | Symbol |
|------|----------|--------|
| USD | US Dollar | $ |
| EUR | Euro | € |
| GBP | British Pound | £ |
| JPY | Japanese Yen | ¥ |
| INR | Indian Rupee | ₹ |
| AUD | Australian Dollar | A$ |
| CAD | Canadian Dollar | C$ |
| CHF | Swiss Franc | CHF |
| CNY | Chinese Yuan | ¥ |
| SGD | Singapore Dollar | S$ |
| HKD | Hong Kong Dollar | HK$ |
| KRW | South Korean Won | ₩ |
| MXN | Mexican Peso | $ |
| BRL | Brazilian Real | R$ |
| AED | UAE Dirham | د.إ |
| THB | Thai Baht | ฿ |
| TRY | Turkish Lira | ₺ |
| ZAR | South African Rand | R |
| NZD | New Zealand Dollar | NZ$ |
| RUB | Russian Ruble | ₽ |

## Commands

| Command | Description |
|---------|-------------|
| `convert AMOUNT FROM TO` | Convert amount between currencies |
| `rates [BASE]` | Show all rates for base currency |
| `popular` | Show popular currency pairs |
| `compare FROM TO...` | Compare one currency to multiple |
| `list` | List all supported currencies |

## API

Uses the free exchangerate-api.com service:
- **Open tier**: No API key required
- **Rate limits**: Reasonable usage expected
- **Update frequency**: Updated daily

## Examples

### Travel Planning
```bash
# Check USD to EUR
python currency-cmd.py convert 500 USD EUR

# Check multiple European currencies
python currency-cmd.py compare USD EUR GBP CHF

# View INR rates
python currency-cmd.py rates INR
```

### Business
```bash
# Check exchange rates for trading
python currency-cmd.py rates EUR

# Compare major currencies
python currency-cmd.py compare USD EUR GBP JPY
```

### Daily Use
```bash
# Quick rate check
python currency-cmd.py popular

# Convert birthday money
python currency-cmd.py convert 100 GBP INR
```

## Output Example

```
════════════════════════════════════════════════════
  Currency Conversion
════════════════════════════════════════════════════

  From:
  €100.00
  EUR - Euro

        ↓
        ↓
        ↓

  To:
  ₹8,934.52
  INR - Indian Rupee

────────────────────────────────────────────────────
  1 EUR = 89.3452 INR
  Rates updated: 2024-01-15
```

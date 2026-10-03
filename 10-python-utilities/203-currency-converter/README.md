# Currency Converter

A Python CLI tool to convert between currencies using free exchange rate APIs.

## Features

- No API key required
- Convert between 20+ major currencies
- View exchange rates for any base currency
- List all supported currencies
- JSON output option
- Fallback API for reliability

## Installation

```bash
pip install -r requirements/currency-converter-requirements.txt
```

## Usage

### Convert currency

```bash
# Basic syntax
python currency-converter.py 100 USD to INR

# Using positional arguments
python currency-converter.py 50 EUR GBP
```

### List supported currencies

```bash
python currency-converter.py --list
```

### Show exchange rates

```bash
# Show all rates with USD as base
python currency-converter.py --rates USD

# Show all rates with EUR as base
python currency-converter.py --rates EUR
```

### JSON output

```bash
python currency-converter.py 100 USD to INR --json
```

### Options

| Option | Description |
|--------|-------------|
| `amount` | Amount to convert |
| `from_currency` | Source currency code |
| `to_currency` | Target currency code |
| `--list`, `-l` | List all supported currencies |
| `--rates`, `-r` | Show exchange rates for base currency |
| `--json` | Output result as JSON |
| `--no-rate` | Hide exchange rate in output |

## Supported Currencies

| Code | Currency |
|------|----------|
| USD | United States Dollar |
| EUR | Euro |
| GBP | British Pound Sterling |
| INR | Indian Rupee |
| JPY | Japanese Yen |
| AUD | Australian Dollar |
| CAD | Canadian Dollar |
| CHF | Swiss Franc |
| CNY | Chinese Yuan |
| RUB | Russian Ruble |
| BRL | Brazilian Real |
| MXN | Mexican Peso |
| SGD | Singapore Dollar |
| HKD | Hong Kong Dollar |
| KRW | South Korean Won |
| AED | United Arab Emirates Dirham |
| SAR | Saudi Riyal |
| NZD | New Zealand Dollar |
| ZAR | South African Rand |
| THB | Thai Baht |

## Example Output

### Conversion

```
Converting 100 USD to INR...
  Currency Conversion
  ────────────────────────────────────────
  100.00 USD
  (Rate: 1 USD = 83.1234 INR)
  equals
  8,312.34 INR
  As of: 2024-01-15 10:30:00
```

### Exchange Rates

```
  Exchange Rates (Base: USD)
  ───────────────────────────────────────────────────
  Currency  Name                           Rate
  ───────────────────────────────────────────────────
  AUD       Australian Dollar              1.5234
  CAD       Canadian Dollar               1.3421
  CHF       Swiss Franc                   0.8823
  CNY       Chinese Yuan                  7.1234
  EUR       Euro                          0.9123
  GBP       British Pound Sterling        0.7823
  INR       Indian Rupee                  83.1234
  JPY       Japanese Yen                  148.23
  ...
  ───────────────────────────────────────────────────
```

## APIs Used

- Primary: https://api.exchangerate.host
- Fallback: https://api.frankfurter.app

No API key or registration required.

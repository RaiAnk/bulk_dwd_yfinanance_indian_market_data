# Bulk YFinance Indian Market Data Downloader

A Python-based tool for downloading historical stock market data from NSE and BSE exchanges. Retrieves 10 years of daily OHLCV data for Nifty 50, Sensex 30 constituent stocks, and major market indices.

## Overview

This tool automates the process of downloading and organizing historical stock data from Yahoo Finance API for Indian equity markets. It's designed for data analysts, quantitative researchers, and developers building financial models or backtesting strategies.

## Features

- Downloads historical data for all Nifty 50 constituent stocks (NSE)
- Downloads historical data for all Sensex 30 constituent stocks (BSE)
- Includes major indices: Nifty 50, Sensex, Bank Nifty
- Automatic retry logic and error handling
- Organized directory structure for easy data access
- Comprehensive logging to file and console
- Rate limiting to prevent API throttling
- Auto-adjusted data for stock splits and dividends

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Dependencies

Install required packages:
```bash
pip install yfinance pandas
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
yfinance>=0.2.28
pandas>=1.5.0
```

## Usage

### Basic Usage

Run the script directly to download all data:
```bash
python bulk_download.py
```

This will download 10 years of historical data for all stocks and save to the `data/` directory.

### Advanced Usage

Import as a module for custom workflows:
```python
from bulk_download import StockDataDownloader

# Initialize downloader
downloader = StockDataDownloader(base_path="my_data")

# Download last 5 years of data
stats = downloader.run_full_download(years=5)

# Check download statistics
print(f"Downloaded {stats['nifty_success']} Nifty stocks")
print(f"Downloaded {stats['sensex_success']} Sensex stocks")
```

### Download Specific Components
```python
from datetime import datetime, timedelta
from bulk_download import StockDataDownloader

downloader = StockDataDownloader()

# Set custom date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365*3)  # 3 years

# Download only indices
downloader.download_market_indices(start_date, end_date)

# Download only Nifty 50 stocks
nifty_stocks = downloader.get_nifty50_stocks()
downloader.bulk_download_stocks(nifty_stocks, "data/nifty50", start_date, end_date)
```

## Output Structure

After execution, data is organized as follows:
```
data/
├── NIFTY50_index.csv       # Nifty 50 index historical data
├── SENSEX_index.csv        # Sensex index historical data
├── BANKNIFTY_index.csv     # Bank Nifty index historical data
├── nifty50/                # Individual Nifty 50 stocks
│   ├── RELIANCE.csv
│   ├── TCS.csv
│   ├── INFY.csv
│   └── ... (50 files)
└── sensex30/               # Individual Sensex 30 stocks
    ├── RELIANCE.csv
    ├── TCS.csv
    ├── HDFCBANK.csv
    └── ... (30 files)
```

### CSV Format

Each CSV file contains the following columns:
```
Date, Open, High, Low, Close, Volume
```

Example:
```csv
Date,Open,High,Low,Close,Volume
2020-01-01,1234.50,1245.00,1230.00,1240.00,5000000
2020-01-02,1241.00,1250.00,1238.00,1248.00,4800000
```

## Configuration

### Modify Historical Data Range

Edit the `years` parameter in the `main()` function:
```python
def main():
    downloader = StockDataDownloader(base_path="data")
    stats = downloader.run_full_download(years=15)  # Download 15 years
    return stats
```

### Change Output Directory

Specify custom path when initializing:
```python
downloader = StockDataDownloader(base_path="custom_folder")
```

### Adjust Rate Limiting

Modify the sleep delay in `bulk_download_stocks()`:
```python
time.sleep(0.5)  # Change to 1.0 for slower, safer requests
```

## Logging

The script generates two types of logs:

1. **Console output**: Real-time progress displayed in terminal
2. **Log file**: Detailed logs saved to `stock_downloader.log`

Log format:
```
2024-11-18 10:30:45 - INFO - Downloading data for RELIANCE.NS
2024-11-18 10:30:47 - INFO - Successfully saved: data/nifty50/RELIANCE.csv (2518 rows)
```

## Troubleshooting

### Connection Errors

If downloads fail due to network issues:
- Check internet connectivity
- Verify Yahoo Finance service status
- Increase rate limiting delay (change `time.sleep()` value)

### Missing Data

Some stocks may have limited historical data:
- Check if stock was recently listed
- Verify stock symbol is correct
- Review log file for specific error messages

### API Rate Limiting

If receiving HTTP 429 errors:
- Increase delay between requests in `bulk_download_stocks()`
- Run script during off-peak hours
- Download in smaller batches

## Notes

- Data is adjusted for stock splits and dividends automatically
- Nifty 50 constituent list is fetched dynamically from NSE
- If NSE API fails, fallback to hardcoded list (may be outdated)
- Downloads only trading day data (weekends/holidays excluded)
- First run may take 30-45 minutes depending on network speed

## Use Cases

- Building stock price prediction models (LSTM, ARIMA)
- Backtesting trading strategies
- Portfolio optimization research
- Statistical arbitrage analysis
- Market correlation studies
- Technical indicator development

## License

MIT License - Free for commercial and personal use

## Contributing

Contributions welcome. Please ensure code follows existing style and includes appropriate documentation.

## Disclaimer

This tool is for educational and research purposes. Market data accuracy depends on Yahoo Finance API. Always verify critical data from official sources. Not financial advice.

## Support

For issues or questions:
- Check the log file for detailed error messages
- Review Yahoo Finance API documentation
- Verify all dependencies are correctly installed

---

Last Updated: November 2024

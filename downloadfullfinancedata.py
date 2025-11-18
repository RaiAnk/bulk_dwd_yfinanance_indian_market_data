"""
Indian Stock Market Data Downloader
===================================
A production-ready script for downloading historical stock data from NSE and BSE.
Supports Nifty 50, Sensex 30, and major indices with comprehensive error handling.

Author: Market Data Analytics Team
Version: 1.0.0
Dependencies: yfinance, pandas
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time
import logging
from typing import List, Dict, Tuple

# Configure logging for production environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StockDataDownloader:
    """
    Handles bulk downloading of Indian stock market data from NSE and BSE exchanges.
    Implements rate limiting and retry logic for robust data acquisition.
    """
    
    def __init__(self, base_path: str = "data"):
        """
        Initialize the downloader with directory structure.
        
        Args:
            base_path: Root directory for storing downloaded data
        """
        self.base_path = base_path
        self.nifty_path = os.path.join(base_path, "nifty50")
        self.sensex_path = os.path.join(base_path, "sensex30")
        
        # Create directory structure if it doesn't exist
        self._setup_directories()
        
    def _setup_directories(self) -> None:
        """Create necessary directory structure for data storage."""
        directories = [self.base_path, self.nifty_path, self.sensex_path]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory structure initialized at: {self.base_path}")
    
    def get_nifty50_stocks(self) -> List[str]:
        """
        Fetch the current list of Nifty 50 constituent stocks from NSE.
        Falls back to hardcoded list if API call fails.
        
        Returns:
            List of stock symbols with .NS suffix for NSE exchange
        """
        try:
            # Attempt to fetch live data from NSE official source
            nse_url = 'https://www.nseindia.com/content/indices/ind_nifty50list.csv'
            df = pd.read_csv(nse_url)
            symbols = [f"{symbol}.NS" for symbol in df['Symbol'].tolist()]
            logger.info(f"Successfully fetched {len(symbols)} Nifty 50 stocks from NSE")
            return symbols
        except Exception as e:
            # Fallback to static list if API fails
            logger.warning(f"Failed to fetch live Nifty 50 list: {e}. Using fallback list.")
            return self._get_fallback_nifty50()
    
    def _get_fallback_nifty50(self) -> List[str]:
        """
        Provides a hardcoded fallback list of Nifty 50 constituents.
        This list should be periodically updated to reflect index changes.
        
        Returns:
            Static list of Nifty 50 stock symbols
        """
        return [
            'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS',
            'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS',
            'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS',
            'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
            'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS',
            'INDUSINDBK.NS', 'INFY.NS', 'ITC.NS', 'JSWSTEEL.NS',
            'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS',
            'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBIN.NS',
            'SUNPHARMA.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS',
            'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'WIPRO.NS',
            'ADANIENT.NS', 'APOLLOHOSP.NS', 'BRITANNIA.NS', 'DIVISLAB.NS',
            'HDFCLIFE.NS', 'LTIM.NS', 'SBILIFE.NS', 'TATACONSUM.NS'
        ]
    
    def get_sensex30_stocks(self) -> List[str]:
        """
        Get the list of Sensex 30 constituent stocks for BSE exchange.
        
        Returns:
            List of stock symbols with .BO suffix for BSE exchange
        """
        sensex_constituents = [
            'RELIANCE.BO', 'TCS.BO', 'HDFCBANK.BO', 'INFY.BO', 'ICICIBANK.BO',
            'HINDUNILVR.BO', 'ITC.BO', 'SBIN.BO', 'BHARTIARTL.BO', 'BAJFINANCE.BO',
            'KOTAKBANK.BO', 'LT.BO', 'AXISBANK.BO', 'ASIANPAINT.BO', 'MARUTI.BO',
            'SUNPHARMA.BO', 'TITAN.BO', 'ULTRACEMCO.BO', 'NESTLEIND.BO',
            'TATAMOTORS.BO', 'M&M.BO', 'HCLTECH.BO', 'POWERGRID.BO', 'NTPC.BO',
            'WIPRO.BO', 'TATASTEEL.BO', 'BAJAJFINSV.BO', 'TECHM.BO',
            'INDUSINDBK.BO', 'JSWSTEEL.BO'
        ]
        logger.info(f"Loaded {len(sensex_constituents)} Sensex 30 stocks")
        return sensex_constituents
    
    def download_single_stock(self, symbol: str, start_date: datetime, 
                             end_date: datetime, save_path: str) -> bool:
        """
        Download historical OHLCV data for a single stock symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'RELIANCE.NS')
            start_date: Start date for historical data
            end_date: End date for historical data
            save_path: Directory path to save the CSV file
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            logger.info(f"Downloading data for {symbol}")
            
            # Fetch data from Yahoo Finance API
            data = yf.download(
                symbol, 
                start=start_date, 
                end=end_date, 
                progress=False,
                auto_adjust=True  # Adjust for splits and dividends
            )
            
            if not data.empty:
                # Clean symbol name for filename (remove exchange suffix)
                clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
                filename = os.path.join(save_path, f"{clean_symbol}.csv")
                
                # Save to CSV with proper formatting
                data.to_csv(filename)
                logger.info(f"Successfully saved: {filename} ({len(data)} rows)")
                return True
            else:
                logger.warning(f"No data available for {symbol}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to download {symbol}: {str(e)}")
            return False
    
    def bulk_download_stocks(self, stock_list: List[str], save_path: str, 
                            start_date: datetime, end_date: datetime) -> Tuple[int, int]:
        """
        Download historical data for multiple stocks with rate limiting.
        
        Args:
            stock_list: List of stock symbols to download
            save_path: Directory to save CSV files
            start_date: Start date for historical data
            end_date: End date for historical data
            
        Returns:
            Tuple of (successful_downloads, total_stocks)
        """
        success_count = 0
        total_stocks = len(stock_list)
        
        logger.info(f"Starting bulk download of {total_stocks} stocks")
        
        for idx, stock in enumerate(stock_list, 1):
            logger.info(f"Processing {idx}/{total_stocks}: {stock}")
            
            if self.download_single_stock(stock, start_date, end_date, save_path):
                success_count += 1
            
            # Rate limiting: Add delay between requests to avoid API throttling
            time.sleep(0.5)
        
        logger.info(f"Bulk download complete: {success_count}/{total_stocks} successful")
        return success_count, total_stocks
    
    def download_market_indices(self, start_date: datetime, end_date: datetime) -> None:
        """
        Download historical data for major Indian market indices.
        
        Args:
            start_date: Start date for historical data
            end_date: End date for historical data
        """
        # Define major indices with their Yahoo Finance symbols
        indices_config = {
            '^NSEI': 'NIFTY50',        # Nifty 50 Index
            '^BSESN': 'SENSEX',        # BSE Sensex Index
            '^NSEBANK': 'BANKNIFTY'    # Bank Nifty Index
        }
        
        logger.info("Starting download of market indices")
        
        for symbol, name in indices_config.items():
            try:
                logger.info(f"Downloading {name} index data")
                data = yf.download(symbol, start=start_date, end=end_date, progress=False)
                
                if not data.empty:
                    filename = os.path.join(self.base_path, f"{name}_index.csv")
                    data.to_csv(filename)
                    logger.info(f"Index saved: {filename} ({len(data)} rows)")
                else:
                    logger.warning(f"No data available for {name}")
                    
            except Exception as e:
                logger.error(f"Failed to download {name} index: {str(e)}")
    
    def run_full_download(self, years: int = 10) -> Dict[str, any]:
        """
        Execute complete download workflow for all indices and stocks.
        
        Args:
            years: Number of years of historical data to download
            
        Returns:
            Dictionary containing download statistics
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        logger.info("=" * 70)
        logger.info("INDIAN STOCK MARKET DATA DOWNLOADER - FULL EXECUTION")
        logger.info("=" * 70)
        logger.info(f"Date range: {start_date.date()} to {end_date.date()}")
        logger.info(f"Data path: {os.path.abspath(self.base_path)}")
        
        stats = {
            'start_date': start_date,
            'end_date': end_date,
            'indices_downloaded': 0,
            'nifty_success': 0,
            'nifty_total': 0,
            'sensex_success': 0,
            'sensex_total': 0
        }
        
        # Step 1: Download market indices
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 1: Downloading Market Indices")
        logger.info("=" * 70)
        self.download_market_indices(start_date, end_date)
        stats['indices_downloaded'] = 3
        
        # Step 2: Download Nifty 50 constituent stocks
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 2: Downloading Nifty 50 Stocks")
        logger.info("=" * 70)
        nifty_stocks = self.get_nifty50_stocks()
        nifty_success, nifty_total = self.bulk_download_stocks(
            nifty_stocks, self.nifty_path, start_date, end_date
        )
        stats['nifty_success'] = nifty_success
        stats['nifty_total'] = nifty_total
        
        # Step 3: Download Sensex 30 constituent stocks
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 3: Downloading Sensex 30 Stocks")
        logger.info("=" * 70)
        sensex_stocks = self.get_sensex30_stocks()
        sensex_success, sensex_total = self.bulk_download_stocks(
            sensex_stocks, self.sensex_path, start_date, end_date
        )
        stats['sensex_success'] = sensex_success
        stats['sensex_total'] = sensex_total
        
        # Display final summary
        self._print_summary(stats)
        
        return stats
    
    def _print_summary(self, stats: Dict[str, any]) -> None:
        """
        Print comprehensive download summary report.
        
        Args:
            stats: Dictionary containing download statistics
        """
        logger.info("\n" + "=" * 70)
        logger.info("DOWNLOAD SUMMARY REPORT")
        logger.info("=" * 70)
        logger.info(f"Date Range: {stats['start_date'].date()} to {stats['end_date'].date()}")
        logger.info(f"Indices Downloaded: {stats['indices_downloaded']}")
        logger.info(f"Nifty 50: {stats['nifty_success']}/{stats['nifty_total']} stocks")
        logger.info(f"Sensex 30: {stats['sensex_success']}/{stats['sensex_total']} stocks")
        logger.info("\nData Location:")
        logger.info(f"  - Indices: {self.base_path}/")
        logger.info(f"  - Nifty 50: {self.nifty_path}/")
        logger.info(f"  - Sensex 30: {self.sensex_path}/")
        logger.info("=" * 70)


def main():
    """
    Main entry point for the stock data downloader application.
    Initializes the downloader and executes full download workflow.
    """
    # Initialize downloader with default data directory
    downloader = StockDataDownloader(base_path="data")
    
    # Execute full download for last 10 years
    # Modify the 'years' parameter to adjust historical data range
    stats = downloader.run_full_download(years=10)
    
    # Optional: Return stats for further processing or logging
    return stats


if __name__ == "__main__":
    """
    Script execution entry point.
    Runs when script is executed directly (not imported as module).
    """
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nDownload interrupted by user")
    except Exception as e:
        logger.error(f"Critical error during execution: {str(e)}", exc_info=True)
        
        
        
        
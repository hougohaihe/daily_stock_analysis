#!/usr/bin/env python3
"""
Daily Stock Analysis - Main Entry Point

This module serves as the main entry point for the daily stock analysis tool.
It orchestrates data fetching, analysis, and report generation.
"""

import os
import sys
import logging
import argparse
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"logs/stock_analysis_{date.today().strftime('%Y%m%d')}.log"),
    ],
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the stock analysis tool."""
    parser = argparse.ArgumentParser(
        description="Daily Stock Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbols AAPL MSFT GOOGL
  python main.py --symbols TSLA --date 2024-01-15
  python main.py --config config.yaml --output reports/
        """,
    )

    parser.add_argument(
        "--symbols",
        nargs="+",
        help="Stock symbols to analyze (e.g., AAPL MSFT TSLA)",
        default=None,
    )
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().strftime("%Y-%m-%d"),
        help="Analysis date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=os.getenv("OUTPUT_DIR", "reports"),
        help="Output directory for analysis reports",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv", "html", "all"],
        default="json",  # prefer json for personal use — easier to parse/script against
        help="Output format for the analysis report",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output",
    )

    return parser.parse_args()


def ensure_directories(output_dir: str) -> None:
    """Ensure required directories exist, creating them if necessary."""
    directories = [output_dir, "logs", "data/cache"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")


def get_symbols_from_env() -> list[str]:
    """Retrieve default stock symbols from environment variables."""
    symbols_env = os.getenv("DEFAULT_SYMBOLS", "")
    if symbols_env:
        return [s.strip().upper() for s in symbols_env.split(",") if s.strip()]
    return []


def main() -> int:
    """
    Main execution function for daily stock analysis.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    arg
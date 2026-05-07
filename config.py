"""Configuration management for daily stock analysis.

Loads and validates environment variables, providing a central
configuration object used throughout the application.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration loaded from environment variables."""

    # Stock data settings
    symbols: List[str] = field(default_factory=list)
    data_dir: str = "data"
    reports_dir: str = "reports"
    logs_dir: str = "logs"

    # Analysis settings
    lookback_days: int = 90  # extended to 90 days for better trend visibility
    moving_avg_short: int = 5
    moving_avg_long: int = 20
    rsi_period: int = 14
    volume_avg_period: int = 10

    # Data source settings
    data_source: str = "yfinance"  # yfinance or alphavantage
    api_key: Optional[str] = None
    request_timeout: int = 30
    max_retries: int = 3

    # Report settings
    report_format: str = "html"  # html, csv, or json
    send_email: bool = False
    email_recipient: Optional[str] = None
    email_sender: Optional[str] = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_password: Optional[str] = None

    # Notification thresholds
    price_change_threshold: float = 5.0   # percent
    volume_spike_threshold: float = 2.0   # multiplier vs average
    rsi_overbought: float = 70.0
    rsi_oversold: float = 30.0


def load_config() -> Config:
    """Load configuration from environment variables.

    Returns:
        Config: Populated configuration object.

    Raises:
        ValueError: If required configuration values are missing or invalid.
    """
    cfg = Config()

    # Directories
    cfg.data_dir = os.getenv("DATA_DIR", "data")
    cfg.reports_dir = os.getenv("REPORTS_DIR", "reports")
    cfg.logs_dir = os.getenv("LOGS_DIR", "logs")

    # Analysis parameters
    cfg.lookback_days = int(os.getenv("LOOKBACK_DAYS", "90"))  # default bumped to 90
    cfg.moving_avg_short = int(os.getenv("MOVING_AVG_SHORT", "5"))
    cfg.moving_avg_long = int(os.getenv("MOVING_AVG_LONG", "20"))
    cfg.rsi_period = int(os.getenv("RSI_PERIOD", "14"))
    cfg.volume_avg_period = int(os.getenv("VOLUME_AVG_PERIOD", "10"))

    # Data source
    cfg.data_source = os.getenv("DATA_SOURCE", "yfinance").lower()
    cfg.api_key = os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("API_KEY")
    cfg.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    cfg.max_retries = int(os.getenv("MAX_RETRIES", "3"))

    # Validate data source
    if cfg.data_source not in ("yfinance", "alphavantage"):
        raise ValueError(
            f"Unsupported DATA_SOURCE '{cfg.data_source}'. "
            "Choose 'yfinance' or 'alphavantage'."
        )
    if cfg.data_source == "alphavantage" and not cfg.api_key:
        raise ValueError(
            "API_KEY or ALPHA_VANTAGE_API_KEY is required when "
            "DATA_SOURCE is 'alphavantage'."
        )

    # Report settings
    cfg.report_format = os.getenv("

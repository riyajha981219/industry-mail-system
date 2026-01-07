"""
Helper Utilities
"""
from datetime import datetime, timedelta
from typing import Optional

def calculate_date_range(days: int) -> tuple:
    """
    Calculate date range based on number of days
    
    Args:
        days: Number of days (1, 7, or 30)
    
    Returns:
        tuple: (from_date, to_date)
    """
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days)
    return from_date, to_date

def validate_email_frequency(frequency: str) -> bool:
    """
    Validate email frequency value
    
    Args:
        frequency: Frequency value ('1', '7', or '30')
    
    Returns:
        bool: True if valid, False otherwise
    """
    return frequency in ['1', '7', '30']

def format_published_date(date_str: str) -> str:
    """
    Format published date string
    
    Args:
        date_str: ISO format date string
    
    Returns:
        str: Formatted date string
    """
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return date_str

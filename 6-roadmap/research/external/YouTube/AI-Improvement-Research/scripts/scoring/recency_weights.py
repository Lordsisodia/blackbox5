"""
Recency Scoring System for AI Training Videos

Boosts recent content, penalizes old content:
- Today/Yesterday: 2.5x
- This week: 2.0x
- Last 2 weeks: 1.5x
- Last month: 1.2x
- Last 2 months: 1.0x (baseline)
- Last 3 months: 0.9x (-10%)
- Last 6 months: 0.7x (-30%)
- Last year: 0.5x (-50%)
- Older: 0.3x (-70%)
"""

from datetime import datetime, timedelta


def get_recency_multiplier(upload_date_str: str) -> float:
    """
    Calculate recency multiplier based on upload date.

    Args:
        upload_date_str: Date in YYYYMMDD format

    Returns:
        float: Multiplier (0.3 to 2.5)
    """
    if not upload_date_str:
        return 0.3  # Unknown date = very old

    try:
        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
        now = datetime.now()
        days_ago = (now - upload_date).days

        # Today or yesterday (0-1 days)
        if days_ago <= 1:
            return 1.5

        # This week (2-7 days)
        elif days_ago <= 7:
            return 1.5

        # Last 2 weeks (8-14 days)
        elif days_ago <= 14:
            return 1.2

        # Last month (15-30 days)
        elif days_ago <= 30:
            return 1.2

        # Last 2 months (31-60 days) - baseline
        elif days_ago <= 60:
            return 1.0

        # Last 3 months (61-90 days) - 10% penalty
        elif days_ago <= 90:
            return 0.9

        # Last 6 months (91-180 days) - 30% penalty
        elif days_ago <= 180:
            return 0.7

        # Last year (181-365 days) - 50% penalty
        elif days_ago <= 365:
            return 0.5

        # Older than 1 year - 70% penalty
        else:
            return 0.3

    except Exception as e:
        print(f"Error parsing date {upload_date_str}: {e}")
        return 0.3


def get_recency_label(upload_date_str: str) -> str:
    """Get human-readable recency label."""
    if not upload_date_str:
        return "unknown"

    try:
        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
        now = datetime.now()
        days_ago = (now - upload_date).days

        if days_ago <= 1:
            return "today/yesterday"
        elif days_ago <= 7:
            return "this week"
        elif days_ago <= 14:
            return "last 2 weeks"
        elif days_ago <= 30:
            return "last month"
        elif days_ago <= 60:
            return "last 2 months"
        elif days_ago <= 90:
            return "last 3 months"
        elif days_ago <= 180:
            return "last 6 months"
        elif days_ago <= 365:
            return "last year"
        else:
            return "1+ year ago"

    except:
        return "unknown"


# For testing
if __name__ == '__main__':
    test_dates = [
        datetime.now().strftime('%Y%m%d'),  # Today
        (datetime.now() - timedelta(days=1)).strftime('%Y%m%d'),  # Yesterday
        (datetime.now() - timedelta(days=5)).strftime('%Y%m%d'),  # This week
        (datetime.now() - timedelta(days=10)).strftime('%Y%m%d'),  # Last 2 weeks
        (datetime.now() - timedelta(days=20)).strftime('%Y%m%d'),  # Last month
        (datetime.now() - timedelta(days=45)).strftime('%Y%m%d'),  # Last 2 months
        (datetime.now() - timedelta(days=75)).strftime('%Y%m%d'),  # Last 3 months
        (datetime.now() - timedelta(days=120)).strftime('%Y%m%d'),  # Last 6 months
        (datetime.now() - timedelta(days=250)).strftime('%Y%m%d'),  # Last year
        (datetime.now() - timedelta(days=400)).strftime('%Y%m%d'),  # 1+ year
    ]

    print("Recency Scoring Test:")
    print("-" * 50)
    for date_str in test_dates:
        mult = get_recency_multiplier(date_str)
        label = get_recency_label(date_str)
        print(f"{date_str} ({label:15}): {mult:.1f}x")

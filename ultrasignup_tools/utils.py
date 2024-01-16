from datetime import datetime

def is_future_date(date_str):
    """
    Check the status of the date.

    Args:
        date_str (str): The date string.

    Returns:
        bool: True if the date is in the future, False otherwise.
    """
    return datetime.strptime(date_str, '%b %d, %Y') >= datetime.today()

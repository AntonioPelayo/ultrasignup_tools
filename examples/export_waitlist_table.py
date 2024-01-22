import os
import sys

sys.path.append(os.path.abspath('../ultrasignup_tools'))

from ultrasignup_tools.event_waitlist import get_waitlist_table
from ultrasignup_tools.ultrasignup_endpoints import UltraSignupEndpoints
from ultrasignup_tools.web_scraping import get_webpage_soup

def main(event_url):
    event_id = UltraSignupEndpoints.event_id(event_url)
    waitlist_url = UltraSignupEndpoints.event_waitlist_url(event_id)
    waitlist_soup = get_webpage_soup(waitlist_url)
    table = get_waitlist_table(waitlist_soup, export=True, export_path='waitlist.csv')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        event_url = sys.argv[1]
        main(event_url)
    else:
        print("Usage: python examples/export_waitlist_table.py '<event_url>'")
        event_url = 'https://ultrasignup.com/register.aspx?did=106491'
        main(event_url)
        print("Example using 2024 Broken Arrow Skyrace saved in waitlist.csv.")
import os
import sys

sys.path.append(os.path.abspath('../ultrasignup_tools'))

import ultrasignup_tools as ust


def main(event, athlete):
    event_id = ust.UltraSignupEndpoints.event_id(event)
    waitlist_url = ust.UltraSignupEndpoints.event_waitlist_url(event_id)
    waitlist_soup = ust.get_webpage_soup(waitlist_url)
    table = ust.get_waitlist_table(waitlist_soup)
    matches = ust.find_athlete_in_table(table, athlete)
    print(matches)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python examples/waitlist_position.py '<event_url>' '<athlete>'")
        print("Example using 2024 Broken Arrow Skyrace 46k and 'Antonio Pelayo'")
        main(
            'https://ultrasignup.com/register.aspx?did=106491',
            'Antonio Pelayo'
        )

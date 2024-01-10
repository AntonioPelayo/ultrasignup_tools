import requests
from bs4 import BeautifulSoup

from ultrasignup_endpoints import UltraSignupEndpoints

HTML_TAGS = {
    'event_waitlist_table': {
        'type': 'table',
        'id': 'ContentPlaceHolder1_gvEntrants'
    },
}

def get_waitlist_table(event_id):
    event_waitlist_url = UltraSignupEndpoints.event_waitlist_url(event_id)

    response = requests.get(event_waitlist_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id=HTML_TAGS['event_waitlist_table']['id'])

    return table

def find_athlete_in_table(table, target_athlete):
    matches = []

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        order, _, name, home, rank = [
            cell.get_text(strip=True) for cell in cells
        ]

        if name == target_athlete:
            matches.append({
                'order': order,
                'name': name,
                'home': home,
                'rank': rank,
            })

    return matches

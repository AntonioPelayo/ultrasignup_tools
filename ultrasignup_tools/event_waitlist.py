HTML_TAGS = {
    'event_waitlist_count': {
        'type': 'span',
        'id': 'ContentPlaceHolder1_lblCount'
    },
    'event_waitlist_table': {
        'type': 'table',
        'id': 'ContentPlaceHolder1_gvEntrants'
    },
}

def get_waitlist_count(soup):
    """
    Get the number of athletes on the waitlist.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        int: The number of athletes on the waitlist.
    """
    count = soup.find(
        'span',
        id=HTML_TAGS['event_waitlist_count']['id']
    ).get_text(strip=True)

    return [int(s) for s in count.split() if s.isdigit()][0]

def get_waitlist_table(soup):
    """
    Get the waitlist table.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        bs4.element.Tag: The waitlist table.
    """
    table = soup.find('table', id=HTML_TAGS['event_waitlist_table']['id'])

    return table

def find_athlete_in_table(table, target_athlete):
    """
    Find the target athlete in the waitlist table.

    Args:
        table (bs4.element.Tag): The waitlist table.
        target_athlete (str): The target athlete.

    Returns:
        list: The list of matches and their information.
    """
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

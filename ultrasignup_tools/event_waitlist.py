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

def export_waitlist_table(table, export_path):
    """
    Export the waitlist table to a CSV file.

    Args:
        table (bs4.element.Tag): The waitlist table.
        export_path (str): The file name/export path.
    """
    with open(export_path, 'w') as f:
        f.write(','.join(['Name', 'Home City', 'Home State', 'Rank']))
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            data = [
                cell.text.strip().replace(', ', ',')
                for cell in cells[2:]
            ]
            f.write(','.join(data) + '\n')

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

def get_waitlist_table(soup, export=False, export_path='waitlist.csv'):
    """
    Get the waitlist table.

    Args:
        soup (BeautifulSoup): The soup object.
        export (bool): Whether or not to export the table as a CSV file.
        export_path (str): The export path.

    Returns:
        bs4.element.Tag or None: The waitlist table if not exporting.

    """
    table = soup.find('table', id=HTML_TAGS['event_waitlist_table']['id'])

    if export:
        export_waitlist_table(table, export_path)
        return None
    else:
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

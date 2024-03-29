HTML_TAGS = {
    'event waitlist count': {
        'tag': 'span',
        'attribute': 'id',
        'identifier': 'ContentPlaceHolder1_lblCount'
    },
    'event waitlist table': {
        'tag': 'table',
        'attribute': 'id',
        'identifier': 'ContentPlaceHolder1_gvEntrants'
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
        HTML_TAGS['event waitlist count']['tag'],
        attrs={
            HTML_TAGS['event waitlist count']['attribute']:
            HTML_TAGS['event waitlist count']['identifier']
        }
    ).get_text(strip=True)

    if "No Applicants Found" in count:
        return 0

    return [int(s) for s in count.split() if s.isdigit()][0]

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
    table = soup.find(
        HTML_TAGS['event waitlist table']['tag'],
        attrs={
            HTML_TAGS['event waitlist table']['attribute']:
            HTML_TAGS['event waitlist table']['identifier']
        }
    )

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
        dict or None: The athlete's information if found, otherwise None.
    """

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        order, _, name, home, rank = [
            cell.get_text(strip=True) for cell in cells
        ]

        if name == target_athlete:
            return {
                'order': order,
                'name': name,
                'home': home,
                'rank': rank,
            }

    return None

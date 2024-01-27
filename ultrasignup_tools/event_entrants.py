HTML_TAGS = {
    'entrants count': {
        'tag': 'span',
        'attribute': 'id',
        'identifier': 'ContentPlaceHolder1_lblCount'
    },
    'entrants table': {
        'tag': 'table',
        'attribute': 'class',
        'identifier': 'ultra_grid'
    }
}

def get_entrants_count(soup):
    """
    Get the number of event entrants.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        int: The number of event entrants.
    """
    count = soup.find(
        HTML_TAGS['entrants count']['tag'],
        attrs={
            HTML_TAGS['entrants count']['attribute'],
            HTML_TAGS['entrants count']['identifier']
        }
    ).text

    return [int(c) for c in count.split() if c.isdigit()][0]

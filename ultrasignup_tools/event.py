HTML_TAGS = {
    'event title': {
        'tag': 'h1',
        'attribute': 'class',
        'identifier': 'event-title'
    },
    'event address': {
        'tag': 'a',
        'attribute': 'class',
        'identifier': 'address_link'
    },
    'event subtitle': {
        'tag': 'h2',
        'attribute': 'class',
        'identifier': 'subtitle'
    },
    'event date': {
        'tag': 'span',
        'attribute': 'id',
        'identifier': 'lblDate'
    },
    'registration status': {
        'tag': 'span',
        'attribute': 'id',
        'identifier': 'ContentPlaceHolder1_EventInfoThin1_lblRegistrationStatus'
    },
}

def split_event_subtitle(subtitle):
    """
    Split the event subtitle into its components.

    Args:
        subtitle (str): The event subtitle.

    Returns:
        tuple: The event subtitle components.
    """
    city, events = subtitle.split('•')

    return city.strip(), events.strip()

def get_event_info(soup):
    """
    Get the event information from the soup object.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        dict: The event information.
    """
    event_info = {}

    for key, value in HTML_TAGS.items():
        try:
            if key == 'event subtitle':
                city, events = split_event_subtitle(
                    soup.find(
                        value['type'],
                        attrs={
                            value['attribute']:
                            value['identifier']
                        }
                    ).text
                )
                event_info['city'] = city
                event_info['events'] = [e.strip() for e in events.split(',')]
            else:
                event_info[key] = soup.find(
                    value['type'],
                    attrs={
                        value['attribute']:
                        value['identifier']
                    }
                ).text
        except Exception as e:
            print(e)
            event_info[key] = None

    return event_info

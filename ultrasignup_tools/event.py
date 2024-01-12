HTML_TAGS = {
    'event title': {
        'type': 'h1',
        'class': 'event-title'
    },
    'event address': {
        'type': 'a',
        'class': 'address_link'
    },
    'event subtitle': {
        'type': 'h2',
        'class': 'subtitle'
    },
    'event date': {
        'type': 'span',
        'id': 'lblDate'
    },
    'registration status': {
        'type': 'span',
        'id': 'ContentPlaceHolder1_EventInfoThin1_lblRegistrationStatus'
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
                    soup.find(value['type'],
                    class_=value['class']).text
                )
                event_info['city'] = city
                event_info['events'] = [e.strip() for e in events.split(',')]
            elif 'id' in value:
                event_info[key] = soup.find(value['type'], id=value['id']).text
            elif 'class' in value:
                event_info[key] = soup.find(value['type'], class_=value['class']).text
        except Exception as e:
            print(e)
            event_info[key] = None

    return event_info
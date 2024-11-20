from .ultrasignup_endpoints import UltraSignupEndpoints
from .web_scraping import find_item, get_webpage_soup

class UltraSignupEvent:
    HTML_TAGS = {
        'title': {
            'tag': 'h1',
            'attribute': 'class',
            'identifier': 'event-title'
        },
        'address': {
            'tag': 'a',
            'attribute': 'class',
            'identifier': 'address_link'
        },
        'subtitle': {
            'tag': 'h2',
            'attribute': 'class',
            'identifier': 'subtitle'
        },
        'date': {
            'tag': 'span',
            'attribute': 'id',
            'identifier': 'lblDate'
        },
        'registration_status': {
            'tag': 'span',
            'attribute': 'id',
            'identifier': 'ContentPlaceHolder1_EventInfoThin1_lblRegistrationStatus'
        },
        'event_years': {
            'tag': 'a',
            'attribute': 'class',
            'identifier': 'year_link'
        }
    }

    def __init__(self, url):
        self.id = UltraSignupEndpoints.event_id(url)
        self.event_url = UltraSignupEndpoints.event_url(self.id)
        self.results_url = UltraSignupEndpoints.event_results_url(self.id)
        self.waitlist_url = UltraSignupEndpoints.event_waitlist_url(self.id)
        self.soup = get_webpage_soup(self.event_url)
        self._set_attributes()
        self.event_years = self.get_event_years()
        self.event_years_urls = self.get_event_years(urls=True)

    def _set_attributes(self):
        """
        Set the attributes for the event object.
        """
        for key, tag_info in self.HTML_TAGS.items():
            if key == 'subtitle':
                self.city, self.events = self._split_event_subtitle(find_item(
                    self.soup,
                    tag_info['tag'],
                    tag_info['attribute'],
                    tag_info['identifier']
                ))
            else:
                setattr(
                    self,
                    key,
                    find_item(
                        self.soup,
                        tag_info['tag'],
                        tag_info['attribute'],
                        tag_info['identifier']
                    )
                )

    def _split_event_subtitle(self, subtitle):
        """
        Split the event subtitle into its components.

        Args:
            subtitle (str): The event subtitle.

        Returns:
            tuple: The event subtitle components.
        """
        city, events = subtitle.split('•')

        return city.strip(), events.strip()

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items()}
        attrs.pop('soup')
        return f'{self.__class__.__name__}({attrs})'

    def get_event_years(self, urls=False):
        """
        Get the event years from the soup object.

        Args:
            urls (bool): True if historical result URLs

        Returns:
            list: The event years or event results urls.
        """
        years = []

        for year in self.soup.find_all(
            self.HTML_TAGS['event_years']['tag'],
            attrs={
                self.HTML_TAGS['event_years']['attribute']:
                self.HTML_TAGS['event_years']['identifier']
            }
        ):
            if urls:
                years.append(f"{UltraSignupEndpoints.BASE_URL}{year['href']}")
            else:
                years.append(year.text)

        return years

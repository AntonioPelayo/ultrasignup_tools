import re

from .ultrasignup_endpoints import UltraSignupEndpoints
from .web_scraping import find_item, load_dynamic_page
from .ultrasignup_endpoints import UltraSignupEndpoints

class EventResults:
    HTML_TAGS = {
        'results_table': {
            'tag': 'table',
            'attribute': 'class',
            'identifier': 'ui-jqgrid-btable'
        },
        'results_table_row': {
            'tag': 'tr',
            'attribute': 'class',
            'identifier': re.compile(
                r"\bui-widget-content\b.*\bjqgrow\b.*\bui-row-ltr\b"
            )
        },
    }

    def __init__(self, url):
        self.event_id = UltraSignupEndpoints.event_id(url)
        self.results_url = UltraSignupEndpoints.event_results_url(self.event_id)
        self.event_url = UltraSignupEndpoints.event_url(self.event_id)
        self.soup = load_dynamic_page(url)
        self.winner_info = self.get_winner_results()

    def get_winner_results(self):
        """
        Find the first place result in the results table.

        Returns:
            dict: The first place result
        """
        tr = find_item(
            self.soup,
            self.HTML_TAGS['results_table_row']['tag'],
            self.HTML_TAGS['results_table_row']['attribute'],
            self.HTML_TAGS['results_table_row']['identifier'],
            text=False
        )

        table_data = tr.find_all('td')
        text_data = [item.text for item in table_data]
        base_url = UltraSignupEndpoints.BASE_URL
        return {
            'place': text_data[1],
            'first_name': text_data[2],
            'last_name': text_data[3],
            'city': text_data[4],
            'state': text_data[5],
            'age': text_data[6],
            'division': text_data[7],
            'division_place': text_data[8],
            'time': text_data[9],
            'runner_rank': text_data[10],
            'athlete_url':
                f"{base_url}/{table_data[0].find_all('a')[1]['href']}"
                if len(table_data[0].find_all('a')) > 1
                else None
        }

    def export_results(self):
        """
        Export the results table from the event results page.

        Returns:
            list: The results table data.
        """
        rows = self.soup.find_all(
            self.HTML_TAGS['results_table_row']['tag'],
            attrs={
                self.HTML_TAGS['results_table_row']['attribute']:
                    self.HTML_TAGS['results_table_row']['identifier']

            }
        )

        data = []

        for row in rows:
            table_data = row.find_all('td')
            text_data = [item.text for item in table_data]
            base_url = UltraSignupEndpoints.BASE_URL
            data.append({
                'place': text_data[1],
                'first_name': text_data[2],
                'last_name': text_data[3],
                'city': text_data[4],
                'state': text_data[5],
                'age': text_data[6],
                'division': text_data[7],
                'division_place': text_data[8],
                'time': text_data[9],
                'runner_rank': text_data[10],
                'athlete_url':
                    f"{base_url}/{table_data[0].find_all('a')[1]['href']}"
                    if len(table_data[0].find_all('a')) > 1
                    else None
            })

        return data

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items()}
        attrs.pop('soup')
        return f'{self.__class__.__name__}({attrs})'

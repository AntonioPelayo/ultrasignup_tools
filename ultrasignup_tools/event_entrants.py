class EventEntrants:
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

    def __init__(self, soup):
        self.entrants = self.get_entrants_table(soup)
        self.entrants_count = self.get_entrants_count(soup)

    def export_entrants_table(table, export_path):
        """
        Export the entrants table as a CSV file.

        Args:
            table (bs4.element.Tag): The entrants table.
            export_path (str): The export path.

        Returns:
            None
        """
        with open(export_path, 'w') as f:
            f.write(','.join([
                'Rank', 'Age Rank', 'Results', 'Target', 'Age', 'Has Trophy',
                'First', 'Last', 'City', 'State', 'Empty', 'Bib', 'Finishes'
            ]))

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                data = [
                    cell.text.strip().replace(', ', ',')
                    for cell in cells[:-1]
                ]
                f.write(','.join(data) + '\n')

    @classmethod
    def get_entrants_table(cls, soup, export=False, export_path='entrants.csv'):
        """
        Get the table of event entrants.

        Args:
            soup (BeautifulSoup): The soup object.
            export (bool): Whether to export the table.
            export_path (str): The export path.

        Returns:
            bs4.element.Tag or None: The entrants table if not exporting.
        """
        table = soup.find(
            cls.HTML_TAGS['entrants table']['tag'],
            attrs={
                cls.HTML_TAGS['entrants table']['attribute'],
                cls.HTML_TAGS['entrants table']['identifier']
            }
        )

        if export:
            cls.export_entrants_table(table, export_path)
            return None
        else:
            return table

    @classmethod
    def get_entrants_count(cls, soup):
        """
        Get the number of event entrants.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            int: The number of event entrants.
        """
        count = soup.find(
            cls.HTML_TAGS['entrants count']['tag'],
            attrs={
                cls.HTML_TAGS['entrants count']['attribute'],
                cls.HTML_TAGS['entrants count']['identifier']
            }
        ).text

        return [int(c) for c in count.split() if c.isdigit()][0]

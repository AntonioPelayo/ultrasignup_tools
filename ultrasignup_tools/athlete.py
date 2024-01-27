import re

from .web_scraping import get_webpage_soup
from .utils import is_future_date

age_division_pattern = re.compile(r'[MF]\d+')

HTML_TAGS = {
    'age': {
        'tag': 'span',
        'attribute': 'string',
        'identifier': age_division_pattern
    },
    'division': {
        'tag': 'span',
        'attribute': 'string',
        'identifier': age_division_pattern
    },
    'rank': {
        'tag': 'div',
        'attribute': 'class',
        'identifier': 'pull-right noMargin fake_link'
    },
    'age rank': {
        'tag': 'div',
        'attribute': 'class',
        'identifier': 'pull-right noMargin fake_link'
    },
    'number of races': {
        'tag': 'div',
        'attribute': 'style',
        'identifier': 'font-size:18px;color:#c0c0c0;'
    },
    'races': {
        'tag': 'div',
        'attribute': 'class',
        'identifier': 'rowlines'
    }
}

def get_race_data(race_soup):
    """
    Extracts race results data from race history table rows.

    Args:
        race_soup (BeautifulSoup): The race row soup object.

    Returns:
        str: race title string
        dict: race data dictionary
    """
    rows = [
        row.text.split('\n') for row in race_soup.find_all('div', class_='row')
    ]
    rows = [[s for s in row if s] for row in rows]

    if is_future_date(rows[0][1]):
        return rows[0][0], {'date': rows[0][1]}

    return rows[0][0], {
        'date': rows[0][1],
        'overall place': rows[1][0].split(':')[1].split(' ')[0],
        'division place': rows[1][0].split(':')[2],
        'time': rows[1][1],
        'age': rows[2][0].split(' ')[1],
        'rank': rows[2][1].split(' ')[1]
    }

class UltraSignupAthlete:
    def __init__(self, athlete_url):
        self.url = athlete_url
        self.soup = get_webpage_soup(athlete_url)
        self.name = self.get_athlete_name(athlete_url)
        self.age = self.get_age(self.soup)
        self.division = self.get_division(self.soup)
        self.rank = self.get_rank(self.soup)
        self.age_rank = self.get_age_rank(self.soup)
        self.num_races = self.get_num_races(self.soup)
        self.races = self.get_races(self.soup)

    @classmethod
    def get_athlete_name(cls, athlete_url):
        """
        Get the athlete name from the athlete URL.

        Args:
            athlete_url (str): The athlete URL.

        Returns:
            dict: The athlete name.
        """
        athlete_name = athlete_url.split('=')[1:3]
        athlete_name = [name.replace('%20', ' ') for name in athlete_name]
        athlete_name = {
            'first name': athlete_name[0].split('&')[0],
            'last name': athlete_name[1].split('&')[0]
        }

        return athlete_name

    @classmethod
    def get_age(cls, soup):
        """
        Get the athlete age.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            str: The athlete age.
        """
        return soup.find(
            HTML_TAGS['age']['tag'],
            attrs={
                HTML_TAGS['age']['attribute']:
                HTML_TAGS['age']['identifier']
            }
        ).text[1:]

    @classmethod
    def get_division(cls, soup):
        """
        Get the athlete division.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            str: The athlete division.
        """
        return soup.find(
            HTML_TAGS['division']['tag'],
            attrs={
                HTML_TAGS['division']['attribute']:
                HTML_TAGS['division']['identifier']
            }
        ).text[0]

    @classmethod
    def get_rank(cls, soup):
        """
        Get the athlete rank.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            str: The athlete rank.
        """
        return soup.find(
            HTML_TAGS['rank']['tag'],
            attrs={
                HTML_TAGS['rank']['attribute']:
                HTML_TAGS['rank']['identifier']
            }
        ).text.split('\n')[2].split(':')[1].strip()

    @classmethod
    def get_age_rank(cls, soup):
        """
        Get the athlete age rank.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            str: The athlete age rank.
        """
        return soup.find(
            HTML_TAGS['age rank']['tag'],
            attrs={
                HTML_TAGS['age rank']['attribute']:
                HTML_TAGS['age rank']['identifier']
            }
        ).text.split('\n')[4].split(':')[1].strip()

    @classmethod
    def get_num_races(cls, soup):
        """
        Get the number of races the athlete has signed up for.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            int: Number of races.
        """
        return int(soup.find(
            HTML_TAGS['number of races']['tag'],
            attrs={
                HTML_TAGS['number of races']['attribute']:
                HTML_TAGS['number of races']['identifier']
            }
        ).text.split()[0])

    @classmethod
    def get_races(cls, soup):
        """
        Get race information for the athlete.

        Args:
            soup (BeautifulSoup): The soup object.

        Returns:
            dict: Race history with results
        """
        races = soup.find_all(
            HTML_TAGS['races']['tag'],
            attrs={
                HTML_TAGS['races']['attribute']:
                HTML_TAGS['races']['identifier']
            }
        )
        d = {}

        # TODO: Races with the same name will overwrite each other
        for r in races:
            k, v = get_race_data(r)
            d[k] = v

        return d

    def athlete_info(self):
        """
        Get the athlete information.

        Returns:
            dict: The athlete information.
        """
        return {
            'url': self.url,
            'name': self.name,
            'age': self.age,
            'division': self.division,
            'rank': self.rank,
            'age rank': self.age_rank,
            'number of races': self.num_races,
            'races': self.races
        }

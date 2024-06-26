import re

from .ultrasignup_endpoints import UltraSignupEndpoints
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

def athlete_exists(url):
    """
    Check if athlete url returns valid athlete based on the existence of the
    header row in user table using <div class="groupheader panel row">.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        bool: True if the athlete exists, False otherwise.
    """
    soup = get_webpage_soup(url)

    if soup.find('div', class_='groupheader panel row'):
        return True

    return False

def parse_upcoming_race_data(soup):
    """
    Extracts upcoming registered event information from athlete webpage soup.

    Args:
        athlete_soup (BeautifulSoup): The athlete soup object.

    Returns:
        dict: upcoming registered events
    """
    rows = [row.text.split('\n') for row in soup.select('div.row')]
    rows = [[s for s in row if s] for row in rows]

    name = rows[0][0].split(' - ')[0]
    date = rows[0][1]
    distance = rows[0][0].split(' - ')[1]
    location = rows[0][0].split(' - ')[2]

    try:
        url = soup.find('a')['href']
    except:
        url = ''

    return {
        'name': name,
        'url': UltraSignupEndpoints.BASE_URL + url,
        'date': date,
        'distance': distance,
        'location': location,
    }

def parse_race_data(soup):
    """
    Extracts race results data from race history table rows.

    Args:
        race_soup (BeautifulSoup): The race row soup object.

    Returns:
        dict: race data dictionary
    """
    rows = [row.text.split('\n') for row in soup.select('div.row')]
    rows = [[s for s in row if s] for row in rows]

    name = rows[0][0].split(' - ')[0]
    date = rows[0][1]
    distance = rows[0][0].split(' - ')[1]
    location = rows[0][0].split(' - ')[2]

    try:
        url = soup.find('a')['href']
    except:
        url = ''

    if 'DNF' in rows[0][0]:
        overall_place = 'DNF'
        division_place = 'DNF'
        time = 'DNF'
        age = None
        rank = 'DNF'
    else:
        overall_place = rows[1][0].split(':')[1].split(' ')[0]
        division_place = rows[1][0].split(':')[2]
        time = rows[1][1]
        age = rows[2][0].split(' ')[1]
        rank = rows[2][1].split(' ')[1]

    return {
        'name': name,
        'url': UltraSignupEndpoints.BASE_URL + url,
        'date': date,
        'distance': distance,
        'location': location,
        'overall place': overall_place,
        'division place': division_place,
        'time': time,
        'age': age,
        'rank': rank
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
        self.race_history = self.get_race_history(self.soup)
        self.upcoming_races = self.get_upcoming_races(self.soup)

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
            text=HTML_TAGS['age']['identifier']

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
            text=HTML_TAGS['division']['identifier']
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
    def get_race_history(cls, soup):
        """
        Get race history for the athlete.

        Args:
            soup (BeautifulSoup): The athlete webpage soup object.

        Returns:
            list: Race history with results
        """
        races = soup.select(
            f'{HTML_TAGS["races"]["tag"]}.{HTML_TAGS["races"]["identifier"]}:not(.upcoming)'
        )

        return [parse_race_data(r) for r in races]

    @classmethod
    def get_upcoming_races(cls, soup):
        """
        Get the upcoming registered races for the athlete.

        Args:
            soup (BeautifulSoup): The athlete webpage soup object.

        Returns:
            list: Upcoming registered races
        """
        races = soup.select(
            f'{HTML_TAGS["races"]["tag"]}.{HTML_TAGS["races"]["identifier"]}.upcoming'
        )

        return [parse_upcoming_race_data(r) for r in races]

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
            'race_history': self.race_history,
            'upcoming_races': self.upcoming_races
        }

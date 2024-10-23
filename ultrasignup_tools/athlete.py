from .ultrasignup_endpoints import UltraSignupEndpoints
from .web_scraping import find_item, get_webpage_soup
from .utils import is_future_date

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
    age_division_pattern = r'[MF]\d+'

    HTML_TAGS = {
        'age': {
            'tag': 'span',
            'attribute': 'regex',
            'identifier': age_division_pattern
        },
        'division': {
            'tag': 'span',
            'attribute': 'regex',
            'identifier': age_division_pattern
        },
        'exists': {
            'tag': 'div',
            'attribute': 'class',
            'identifier': 'groupheader panel row'
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

    def __init__(self, athlete_url):
        self.url = athlete_url
        self.soup = get_webpage_soup(athlete_url)
        self.name = self._get_name()
        self.age = self._get_age()
        self.division = self._get_division()
        self.rank = self._get_rank()
        self.age_rank = self._get_age_rank()
        self.num_races = self._get_num_races()
        self.race_history = self._get_race_history()
        self.upcoming_races = self._get_upcoming_races()

    @classmethod
    def athlete_exists(self, url=None):
        """
        Check if athlete url returns valid athlete based on the existence of the
        header row in user table using <div class="groupheader panel row">.

        Optional Args:
            url (str): The athlete URL.

        Returns:
            bool: True if the athlete exists, False otherwise.
        """
        soup = get_webpage_soup(url if url else self.url)

        if find_item(
            soup,
            self.HTML_TAGS['exists']['tag'],
            self.HTML_TAGS['exists']['attribute'],
            self.HTML_TAGS['exists']['identifier'],
            text=False
        ):
            return True

        return False

    def _get_name(self):
        """
        Get the athlete name from the athlete URL.

        Args:
            athlete_url (str): The athlete URL.

        Returns:
            dict: The athlete name.
        """
        athlete_name = self.url.split('=')[1:3]
        athlete_name = [name.replace('%20', ' ') for name in athlete_name]
        athlete_name = {
            'first_name': athlete_name[0].split('&')[0],
            'last_name': athlete_name[1].split('&')[0]
        }

        return athlete_name

    def _get_age(self):
        """
        Get the athlete age.

        Returns:
            str: The athlete age.
        """
        return int(find_item(
            self.soup,
            self.HTML_TAGS['age']['tag'],
            self.HTML_TAGS['age']['attribute'],
            self.HTML_TAGS['age']['identifier']
        )[1:])

    def _get_division(self):
        """
        Get the athlete division.

        Returns:
            str: The athlete division.
        """
        return find_item(
            self.soup,
            self.HTML_TAGS['division']['tag'],
            self.HTML_TAGS['division']['attribute'],
            self.HTML_TAGS['division']['identifier']
        )[0]

    def _get_rank(self):
        """
        Get the athlete rank.

        Returns:
            str: The athlete rank.
        """
        return find_item(
            self.soup,
            self.HTML_TAGS['rank']['tag'],
            self.HTML_TAGS['rank']['attribute'],
            self.HTML_TAGS['rank']['identifier']
        ).split('\n')[2].split(':')[1].strip()

    def _get_age_rank(self):
        """
        Get the athlete age rank.

        Returns:
            str: The athlete age rank.
        """
        return find_item(
            self.soup,
            self.HTML_TAGS['age rank']['tag'],
            self.HTML_TAGS['age rank']['attribute'],
            self.HTML_TAGS['age rank']['identifier']
        ).split('\n')[4].split(':')[1].strip()

    def _get_num_races(self):
        """
        Get the number of races the athlete has signed up for.

        Returns:
            int: Number of races.
        """
        return int(find_item(
            self.soup,
            self.HTML_TAGS['number of races']['tag'],
            self.HTML_TAGS['number of races']['attribute'],
            self.HTML_TAGS['number of races']['identifier']
        ).split()[0])

    def _get_race_history(self):
        """
        Get race history for the athlete.

        Returns:
            list: Race history with results
        """
        races = self.soup.select(
            f'{self.HTML_TAGS["races"]["tag"]}.{self.HTML_TAGS["races"]["identifier"]}:not(.upcoming)'
        )

        return [parse_race_data(r) for r in races]

    def _get_upcoming_races(self):
        """
        Get the upcoming registered races for the athlete.

        Returns:
            list: Upcoming registered races
        """
        races = self.soup.select(
            f'{self.HTML_TAGS["races"]["tag"]}.{self.HTML_TAGS["races"]["identifier"]}.upcoming'
        )

        return [parse_upcoming_race_data(r) for r in races]

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items()}
        attrs.pop('soup')
        return f'{self.__class__.__name__}({attrs})'

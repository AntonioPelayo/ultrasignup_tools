import re
import unittest

from ultrasignup_tools.athlete import UltraSignupAthlete
from ultrasignup_tools.ultrasignup_endpoints import UltraSignupEndpoints

import tests.config as cfg

athlete = UltraSignupAthlete(cfg.TEST_ATHLETE_URL)

class TestAthlete(unittest.TestCase):
    def test_athlete_exists(self):
        self.assertTrue(UltraSignupAthlete.athlete_exists(cfg.TEST_ATHLETE_URL))

    def test_athlete_get_name(self):
        self.assertEqual(
            athlete.name,
            {
                'first_name': cfg.TEST_ATHLETE_FIRST_NAME,
                'last_name': cfg.TEST_ATHLETE_LAST_NAME
            }
        )

    def test_athlete_get_age(self):
        self.assertEqual(athlete.age, cfg.TEST_ATHLETE_AGE)

    def test_athlete_get_rank(self):
        self.assertIsNotNone(re.match(r'\d{2}\.\d{2}', athlete.rank))

    def test_athlete_get_age_rank(self):
        self.assertIsNotNone(re.match(r'\d{2}\.\d{2}', athlete.age_rank))

    def test_athlete_get_num_races(self):
        self.assertEqual(athlete.num_races, 5)

    # TODO: Test race history and upcoming_races

if __name__ == '__main__':
    unittest.main()

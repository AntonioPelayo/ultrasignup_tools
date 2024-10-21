import unittest

from ultrasignup_tools.ultrasignup_endpoints import UltraSignupEndpoints
import tests.config as cfg

class TestUltraSignupEndpoints(unittest.TestCase):
    def test_athlete_url(self):
        athlete_url = UltraSignupEndpoints.athlete_url(
            cfg.TEST_ATHLETE_FIRST_NAME, cfg.TEST_ATHLETE_LAST_NAME
        )
        self.assertEqual(athlete_url,cfg.TEST_ATHLETE_URL)

    def test_event_id(self):
        event_id = UltraSignupEndpoints.event_id(cfg.TEST_EVENT_URL)
        self.assertEqual(event_id, cfg.TEST_EVENT_ID)

    def test_event_url(self):
        event_url = UltraSignupEndpoints.event_url(cfg.TEST_EVENT_ID)
        self.assertEqual(event_url, cfg.TEST_EVENT_URL)

    def test_event_entrants_url(self):
        event_entrants_url = UltraSignupEndpoints.event_entrants_url(
            cfg.TEST_EVENT_ID
        )
        self.assertEqual(
            event_entrants_url,
            f'https://ultrasignup.com/entrants_event.aspx?did={cfg.TEST_EVENT_ID}'
        )

    def test_event_waitlist_url(self):
        event_waitlist_url = UltraSignupEndpoints.event_waitlist_url(
            cfg.TEST_EVENT_ID
        )
        self.assertEqual(
            event_waitlist_url,
            f'https://ultrasignup.com/event_waitlist.aspx?did={cfg.TEST_EVENT_ID}'
        )

if __name__ == '__main__':
    unittest.main()

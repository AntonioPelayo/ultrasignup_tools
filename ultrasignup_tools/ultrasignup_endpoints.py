class UltraSignupEndpoints:
    BASE_URL = 'https://ultrasignup.com'

    @classmethod
    def athlete_url(cls, first_name, last_name):
        return f'{cls.BASE_URL}/results_participant.aspx?fname={first_name}&lname={last_name}'

    @classmethod
    def event_id(cls, event_url):
        return int(event_url.split('=')[-1])

    @classmethod
    def event_url(cls, event_id):
        return f'{cls.BASE_URL}/register.aspx?did={event_id}'

    @classmethod
    def event_entrants_url(cls, event_id):
        return f'{cls.BASE_URL}/entrants_event.aspx?did={event_id}'

    @classmethod
    def event_waitlist_url(cls, event_id):
        return f'{cls.BASE_URL}/event_waitlist.aspx?did={event_id}'

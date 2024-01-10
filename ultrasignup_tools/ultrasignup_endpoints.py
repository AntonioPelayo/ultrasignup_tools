class UltraSignupEndpoints:
    BASE_URL = 'https://ultrasignup.com'

    @classmethod
    def event_url(cls, event_id):
        return f'{cls.BASE_URL}/register.aspx?did={event_id}'

    @classmethod
    def event_waitlist_url(cls, event_id):
        return f'{cls.BASE_URL}/event_waitlist.aspx?did={event_id}'

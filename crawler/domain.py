from datetime import datetime
from threading import Timer


class Domain():
    def __init__(self, nam_domain, int_time_limit_between_requests):
        self.time_last_access = datetime(1970, 1, 1)
        self.nam_domain = nam_domain
        self.int_time_limit_seconds = int_time_limit_between_requests
        self._is_accessible = True

    @property
    def time_since_last_access(self):
        timedelta = datetime.now() - self.time_last_access
        return timedelta

    def turn_server_accessible(self):
        self._is_accessible = True

    def accessed_now(self):
        self._is_accessible = False

        r = Timer(self.int_time_limit_seconds, self.turn_server_accessible)
        r.start()

        self.time_last_access = datetime.now()

    def is_accessible(self):
        return self._is_accessible

    def __hash__(self):
        return None

    def __eq__(self, domain):
        return None

    def __str__(self):
        return self.nam_domain

    def __repr__(self):
        return str(self)

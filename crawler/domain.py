from datetime import datetime
import sched
import time


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

    def accessed_now(self):
        def turn_server_accessible(self):
            self._is_accessible = True

        s = sched.scheduler(time.time, time.sleep)
        self._is_accessible = False

        s.enter(self.int_time_limit_seconds, 1,
                turn_server_accessible, argument={self})
        s.run()
        self.time_last_access = datetime.now()

    def is_accessible(self):
        return self._is_accessible

    def __hash__(self):
        return 5

    def __eq__(self, domain):
        return None

    def __str__(self):
        return self.nam_domain

    def __repr__(self):
        return str(self)

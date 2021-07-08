from datetime import datetime, timedelta
from threading import Timer


class Domain:
    def __init__(self, nam_domain, int_time_limit_between_requests):
        self.time_last_access = datetime(1970, 1, 1)
        self.nam_domain = nam_domain
        self.int_time_limit_seconds = int_time_limit_between_requests
        self.__accessible = True

    @property
    def time_since_last_access(self) -> timedelta:
        return datetime.now() - self.time_last_access

    def __turn_server_accessible(self) -> None:
        self.__accessible = True

    def accessed_now(self) -> None:
        self.__accessible = False
        self.time_last_access = datetime.now()
        Timer(interval=1.1 * self.int_time_limit_seconds, function=self.__turn_server_accessible).start()

    def is_accessible(self) -> bool:
        return self.__accessible

    def __hash__(self):
        return hash(self.nam_domain)

    def __eq__(self, domain):
        return self.nam_domain == domain

    def __str__(self):
        return self.nam_domain

    def __repr__(self):
        return str(self)

class CancleCurrentSiteException(Exception):
    pass


class NoLoginCandidatesFoundException(Exception):
    pass


class ConfigInvalidException(Exception):
    pass


class ManualAnalysisNeededException(Exception):
    pass


class ParameterException(Exception):
    def __init__(self, msg):
        self.msg = msg


class RenewalRequestNeededException(Exception):
    pass


class ResetProcessException(Exception):
    pass


class RetryException(Exception):
    pass


class SiteNotResolvableException(Exception):
    pass


class DuckDuckGoHasChangedException(Exception):
    pass


class StartPageHasChangedException(Exception):
    pass


class BingHasChangedException(Exception):
    pass


class IdpPageOpenedOnClick(Exception):
    def __init__(self, opened_url, starting_point_next_try):
        self.opened_url = opened_url
        self.starting_point_next_try = starting_point_next_try


class WebDriverInitialisationException(Exception):
    def __init__(self, e):
        self.thrown_exception = e

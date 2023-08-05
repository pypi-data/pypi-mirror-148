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


class WebDriverInitialisationException(Exception):
    def __init__(self, e):
        self.thrown_exception = e

    pass

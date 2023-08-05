from polly.session import PollySession
from requests.adapters import HTTPAdapter, Retry

link_doc = "https://docs.elucidata.io/OmixAtlas/Polly%20Python.html"
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])


class UnauthorizedException(Exception):
    def __str__(self):
        return f"Authorization failed as credentials not found. Please use Polly.auth(token) as shown here  ---- {link_doc}"


class Polly:
    default_session = None

    @classmethod
    def auth(cls, token, env="polly"):
        cls.default_session = PollySession(token, env=env)
        cls.default_session.mount(
            "https://",
            HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retries),
        )

    @classmethod
    def get_session(cls, token=None, env="polly"):
        if not token:
            if not cls.default_session:
                raise UnauthorizedException
            else:
                return cls.default_session
        else:
            cls.auth(token, env=env)
            return cls.default_session

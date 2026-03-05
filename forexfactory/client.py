from pathlib import Path
from typing import Dict

from curl_cffi import requests

from .utils.cookie_manager import load_cookies, save_cookies
from .api.calendar import CalendarAPI


DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)


class ForexFactoryClient:
    """
    Main API Client to interface with ForexFactory endpoints.
    Instantiates underlying route handlers and manages session/cookies.
    """
    
    BASE_URL = "https://www.forexfactory.com"
    IMPERSONATE = "chrome"

    def __init__(self, cookie_file: Path, user_agent: str = DEFAULT_USER_AGENT):
        self.cookie_file = cookie_file
        self.user_agent = user_agent
        self.cookies: Dict[str, str] = load_cookies(cookie_file)
        
        # Route instances
        self.calendar = CalendarAPI(self)

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Executes a signed HTTP request with required headers and managed cookies.
        """
        url = self.BASE_URL + endpoint
        headers = kwargs.pop("headers", {})
        merged_headers = {
            "accept-language": "en-US,en;q=0.9",
            "user-agent": self.user_agent,
            **headers,
        }
        
        r = requests.request(
            method=method,
            url=url,
            headers=merged_headers,
            cookies=self.cookies,
            impersonate=self.IMPERSONATE,
            timeout=120,
            **kwargs,
        )
        # Update cookies map continuously based on response
        self.cookies.update(r.cookies.get_dict())
        return r

    def persist_cookies(self) -> None:
        """Save the current managed cookies to the configured cookie_file."""
        save_cookies(self.cookie_file, self.cookies)

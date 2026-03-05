from typing import Dict, Any, List, Optional
from ..utils.html_parser import extract_csrf_token

DEFAULT_IMPACTS = [3, 2, 1, 0]
DEFAULT_EVENT_TYPES = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
DEFAULT_CURRENCIES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class CalendarAPI:
    """Handles ForexFactory calendar-specific capabilities."""

    def __init__(self, client):
        self.client = client

    def warmup(self) -> str:
        """
        Performs a warmup request to grab the CRSF token needed for post actions.
        """
        r = self.client.request(
            "GET",
            "/calendar",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "referer": f"{self.client.BASE_URL}/",
            },
        )
        if r.status_code != 200:
            raise RuntimeError(f"Warmup failed with status {r.status_code}")
        
        csrf = extract_csrf_token(r.text)
        if not csrf:
            raise RuntimeError("CSRF token not found from /calendar")
        return csrf

    def apply_settings(
        self,
        begin_date: str,
        end_date: str,
        default_view: str = "this_week",
        impacts: Optional[List[int]] = None,
        event_types: Optional[List[int]] = None,
        currencies: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Applies settings and fetches the raw JSON calendar payload from ForexFactory.
        """
        csrf = self.warmup()
        payload = {
            "begin_date": begin_date,
            "end_date": end_date,
            "default_view": default_view,
            "impacts": impacts or DEFAULT_IMPACTS,
            "event_types": event_types or DEFAULT_EVENT_TYPES,
            "currencies": currencies or DEFAULT_CURRENCIES,
        }
        r = self.client.request(
            "POST",
            "/calendar/apply-settings/100000?navigation=1",
            headers={
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "origin": self.client.BASE_URL,
                "referer": f"{self.client.BASE_URL}/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-csrf-token": csrf,
            },
            json=payload,
        )
        if r.status_code != 200:
            raise RuntimeError(f"apply-settings failed with status {r.status_code}: {r.text[:300]}")
        return r.json()

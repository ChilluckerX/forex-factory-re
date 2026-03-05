# ForexFactory Calendar SDK

A pure API client for retrieving up-to-date and historical calendar data from ForexFactory. This tool is built specifically for **educational purposes**, demonstrating how to structure an Object-Oriented wrapper around web APIs, manipulate state (cookies), and sanitize incoming JSON responses.

## Disclaimer
This project is for educational use only. Scraping data may be against the terms of service of many websites. Please act responsibly and consult the target site's Terms of Service before putting a bot in production.

## Features
- **Intelligent Requests**: Bypasses typical Cloudflare restrictions by impersonating browsers via `curl_cffi` backend.
- **Cookie Management**: Manages and persists cookies automatically for optimal session safety.
- **CSRF Token Handling**: Makes warmup requests automatically to gather and distribute CSRF tokens across POST endpoints.
- **Clean Output Data**: Provides a normalization utility to sanitize complex API data structures into a simple, predictable schema.

---

## Installation

This project relies on `curl_cffi` to send fast and robust HTTP requests with proper browser TLS/JA3 fingerprints.

1. **Clone the repository** or download the package directory.
2. **Install dependencies**.

```bash
pip install curl_cffi
```

---

## Usage Example

We provide a functional example under the `examples/` directory (`example_sdk_call.py`). 

Below is a minimal representation of how the `ForexFactoryClient` can be used. For complete results and a beautiful logging table, examine the example script.

### 1. Initialize the Client

```python
from pathlib import Path
from forexfactory import ForexFactoryClient

# Provide an absolute or relative path to a cookies JSON file to save session data
cookie_file = Path("cookies.json")
client = ForexFactoryClient(cookie_file=cookie_file)
```

### 2. Make an API Call

```python
# Pass target date ranges to pull records from
raw_calendar_response = client.calendar.apply_settings(
    begin_date="Mar 05, 2026",
    end_date="Mar 11, 2026",
    default_view="this_week",
)
```

### 3. Normalize the Outputs
ForexFactory's native JSON consists of heavily nested HTML strings, metadata wrappers, and configuration hashes. Use the `normalize_calendar` utility for straightforward arrays mapping daily events:

```python
from forexfactory.utils.data_parser import normalize_calendar

# Sanitize and strictly map raw objects
normalized_data = normalize_calendar(raw_calendar_response)

# Optionally persist cookies at the end to keep the flow alive
client.persist_cookies()
```

---

## Result Structure

The normalized data dictionary provides a concise and strongly typed output. For standard calendar parsing you can expect lists of `days` containing nested `events`.

```json
{
  "meta": {
    "title": "Mar 5, 2026 - Mar 11, 2026",
    "url": "/calendar?range=mar5.2026-mar11.2026",
    ...
  },
  "days": [
    {
       "date": "Thu Mar 5"
    }
  ],
  "events": [
    {
      "date": "Mar 5, 2026",
      "time": "8:30am",
      "currency": "USD",
      "impact": "high",
      "actual": "224K",
      "forecast": "215K",
      "previous": "218K"
    }
  ]
}
```

When you execute `python examples/example_sdk_call.py`, you will see a command-line interface table directly emitting all tracked events with their respective currency pairing and expected impacts.

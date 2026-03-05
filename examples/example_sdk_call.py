import sys
from pathlib import Path

# Add project root to sys path so we can import our package
sys.path.append(str(Path(__file__).parent.parent))

from forexfactory import ForexFactoryClient
from forexfactory.utils.data_parser import normalize_calendar

def main() -> int:
    """
    Main demonstration code. Initializes the client, requests the calendar events 
    for a given date range, then logs out all events with details.
    """
    cookie_file = Path(__file__).parent.with_name("cookies.json")
    client = ForexFactoryClient(cookie_file=cookie_file)

    # Fetch raw settings
    raw = client.calendar.apply_settings(
        begin_date="Mar 05, 2026",
        end_date="Mar 11, 2026",
        default_view="this_week",
    )
    
    # Normalize the data and persist cookies
    data = normalize_calendar(raw)
    client.persist_cookies()

    print(f"Range: {data['meta']['title']}")
    print(f"Days: {len(data['days'])}")
    print(f"Events: {len(data['events'])}\n")

    print(f"{'Date':<15} | {'Currency':<10} | {'Impact':<10} | {'Actual':<10} | {'Forecast':<10} | {'Previous':<10}")
    print("-" * 80)
    
    for ev in data["events"]:
        date = ev.get("date") or ""
        currency = ev.get("currency") or ""
        impact = ev.get("impact") or ""
        actual = ev.get("actual") or ""
        forecast = ev.get("forecast") or ""
        previous = ev.get("previous") or ""
        
        print(f"{date:<15} | {currency:<10} | {impact:<10} | {actual:<10} | {forecast:<10} | {previous:<10}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

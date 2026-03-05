from typing import Dict, Any
from .html_parser import strip_html

def normalize_calendar(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given the raw JSON calendar payload from ForexFactory,
    normalizes it into a strictly typed and easily parseable dictionary.
    """
    navigation = raw.get("navigation", {})
    current = navigation.get("current", {})
    result = {
        "meta": {
            "title": current.get("title"),
            "url": current.get("url"),
            "more": bool(raw.get("more")),
            "append": bool(raw.get("append")),
            "upnext": bool(raw.get("upnext")),
        },
        "days": [],
        "events": [],
    }

    for day in raw.get("days", []):
        day_date = strip_html(day.get("date", ""))
        day_dateline = day.get("dateline")
        result["days"].append(
            {
                "date": day_date,
                "dateline": day_dateline,
                "count": len(day.get("events", [])),
            }
        )

        for ev in day.get("events", []):
            result["events"].append(
                {
                    "id": ev.get("id"),
                    "date": day_date,
                    "day_dateline": day_dateline,
                    "time": ev.get("timeLabel"),
                    "time_masked": bool(ev.get("timeMasked")),
                    "currency": ev.get("currency"),
                    "impact": ev.get("impactName"),
                    "impact_class": ev.get("impactClass"),
                    "title": ev.get("trimmedPrefixedName") or ev.get("prefixedName") or ev.get("name"),
                    "actual": ev.get("actual"),
                    "forecast": ev.get("forecast"),
                    "previous": ev.get("previous"),
                    "actual_better_worse": ev.get("actualBetterWorse"),
                    "revision_better_worse": ev.get("revisionBetterWorse"),
                    "has_graph": bool(ev.get("hasGraph")),
                    "is_subscribed": bool(ev.get("isSubscribed")),
                    "detail_url": ev.get("url"),
                    "solo_url": ev.get("soloUrl"),
                    "country": ev.get("country"),
                    "dateline": ev.get("dateline"),
                }
            )

    return result

import json
from pathlib import Path
from typing import Dict, Any

def safe_json_loads(raw: str) -> Any:
    """Attempts to strip common invisible encoding bits and parse to JSON."""
    return json.loads(raw.lstrip('\ufeff').strip())

def load_cookies(cookie_file: Path) -> Dict[str, str]:
    """Reads saved cookies from a file into a usable dictionary formatted for Requests."""
    if not cookie_file.exists():
        return {}

    try:
        parsed = safe_json_loads(cookie_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
        
    result: Dict[str, str] = {}

    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict):
                name = item.get("name")
                value = item.get("value")
                if name and value is not None:
                    result[str(name)] = str(value)
    elif isinstance(parsed, dict):
        nested = parsed.get("cookies")
        if isinstance(nested, dict):
            for k, v in nested.items():
                if k and v is not None:
                    result[str(k)] = str(v)

    return result

def save_cookies(cookie_file: Path, cookie_map: Dict[str, str]) -> None:
    """Saves live dictionary of cookies out into disk structure."""
    as_list = [
        {"name": k, "value": v, "domain": ".forexfactory.com", "path": "/"}
        for k, v in sorted(cookie_map.items())
    ]
    cookie_file.write_text(json.dumps(as_list, indent=2), encoding="utf-8")

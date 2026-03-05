import re

def extract_csrf_token(html: str) -> str:
    """Attempts to scrape a CSRF token from the text of the webpage."""
    patterns = [
        r'name="csrf-token"\s+content="([^"]+)"',
        r"name='csrf-token'\s+content='([^']+)'",
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return ""

def strip_html(value: str) -> str:
    """Safely extracts inner text out of simple html blocks."""
    return re.sub(r"<[^>]+>", "", value or "").strip()

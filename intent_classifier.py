import re
from typing import Literal

def classify_intent(query: str) -> Literal["short", "detailed", "list"]:
    q = query.lower()

    if any(x in q for x in ["brief", "summary", "short version", "quickly"]):
        return "short"
    elif any(x in q for x in ["details", "deep dive", "elaborate", "how exactly", "explain thoroughly"]):
        return "detailed"
    elif any(x in q for x in ["list", "steps", "points", "key takeaways", "bullet"]):
        return "list"
    elif re.search(r"what.*(is|are).*", q):
        return "short"
    elif re.search(r"(how|why|explain|describe)", q):
        return "detailed"
    else:
        return "detailed"

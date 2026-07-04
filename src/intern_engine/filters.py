"""All the text classification: is it an internship? is it tech? which season?

These are deliberately simple, central, and easy to tune. As we see real data
we widen/narrow these patterns here, in one place.
"""

from __future__ import annotations

import re

# --- internship detection (whole words, never substrings) --------------------
_INTERN_RE = re.compile(r"\b(intern|interns|internship|co[\s-]?op)\b", re.IGNORECASE)
_SENIOR_RE = re.compile(
    r"\b(senior|sr|staff|principal|manager|director|\blead\b|vp|head)\b",
    re.IGNORECASE,
)

# --- tech-role detection -----------------------------------------------------
# We keep ONLY software / data / ML / security roles. A role must match an
# INCLUDE term and must NOT match an EXCLUDE term. The exclude list removes
# non-software engineering (mechanical, aerospace, electrical/hardware, etc.)
# and non-technical roles (recruiting, sales, marketing, ...). Note we do NOT
# treat a bare "engineer" as tech — that word alone lets in mech/aero/civil.
_INCLUDE_RE = re.compile(
    r"\b("
    r"software|developer|swe|full[\s-]?stack|front[\s-]?end|back[\s-]?end|"
    r"web developer|web engineer|mobile|ios|android|devops|sre|site reliability|"
    r"infrastructure|platform engineer|platform engineering|distributed systems|"
    r"operating system|compiler|embedded|firmware|"
    r"cyber|cybersecurity|appsec|application security|information security|infosec|"
    r"security engineer|"
    r"data science|data scientist|data engineer|data analyst|analytics engineer|"
    r"machine learning|ml|deep learning|ai|artificial intelligence|nlp|computer vision|"
    r"research scientist|applied scientist|research engineer|ml engineer|ai engineer|"
    r"quantitative developer|quant developer|computer science|programming"
    r")\b",
    re.IGNORECASE,
)
_EXCLUDE_RE = re.compile(
    r"\b("
    r"mechanical|aerospace|aeronautical|astrodynamics|aerodynamic|propulsion|avionics|"
    r"guidance|navigation|gnc|naval|civil engineer|chemical|chemistry|chemist|"
    r"biology|biological|materials|structural|thermal|fluid|manufacturing|"
    r"industrial engineer|electrical|fpga|asic|pcb|analog|photonics|optical|"
    r"hardware|physical design|silicon|semiconductor|vlsi|rtl|"
    r"recruit|recruiting|recruiter|sales|account executive|account manager|marketing|"
    r"legal|counsel|accounting|human resources|people operations|people team|talent|"
    r"communications|supply chain|business development|product design|product designer|"
    r"product manager|product management|ux design|graphic design|industrial design|"
    r"phd|ph\.d|doctoral"
    r")\b",
    re.IGNORECASE,
)

# --- season detection --------------------------------------------------------
_YEAR_RE = re.compile(r"\b(20\d\d)\b")


def is_internship(title: str) -> bool:
    return bool(_INTERN_RE.search(title)) and not _SENIOR_RE.search(title)


def is_tech(title: str) -> bool:
    """Keep software/data/ML/security roles; reject hardware/mech/non-tech."""
    if _EXCLUDE_RE.search(title):
        return False
    return bool(_INCLUDE_RE.search(title))


_CYCLE_RE = re.compile(r"(Summer|Fall|Spring|Winter)\s+(\d{4})", re.IGNORECASE)


def detect_season(title: str, cycles=("Summer 2027", "Fall 2026"), *_ignored) -> str | None:
    """Bucket a title into a cycle ONLY if the year is explicit in the title.

    This is strict on purpose: a role must actually state its year (e.g. "2027"
    or "Fall 2026"). Roles with no year, or a year/term we don't track, are
    dropped — so the list contains only genuine, dated postings (like the
    reference repos), never undated roles defaulted into a cycle.

    Examples (cycles = Summer 2027, Fall 2026):
      "Software Engineer Intern, Summer 2027"  -> "Summer 2027"
      "2027 Software Engineer Intern"          -> "Summer 2027"  (year explicit)
      "Fall 2026 Data Science Intern"          -> "Fall 2026"
      "Software Engineer Intern"               -> None  (no year -> drop)
      "Summer 2026 Intern"                     -> None  (past -> drop)
      "Fall 2027 Intern"                       -> None  (cycle not tracked)
    """
    parsed = []  # (term, year, label)
    for label in cycles:
        m = _CYCLE_RE.match(label.strip())
        if m:
            parsed.append((m.group(1).capitalize(), m.group(2), label))

    years = set(_YEAR_RE.findall(title))
    if not years:
        return None  # no explicit year in the title -> drop

    t = title.lower()
    if "summer" in t:
        term = "Summer"
    elif "fall" in t or "autumn" in t:
        term = "Fall"
    elif "spring" in t:
        term = "Spring"
    elif "winter" in t:
        term = "Winter"
    else:
        term = None

    # 1) exact term + year match (e.g. "Summer 2027")
    for cterm, cyear, label in parsed:
        if cyear in years and term == cterm:
            return label
    # 2) year matches a tracked cycle and the title has no conflicting term
    #    (e.g. "2027 Software Engineer Intern" -> the 2027 cycle)
    for _cterm, cyear, label in parsed:
        if cyear in years and term is None:
            return label
    # year stated but term conflicts (e.g. "Fall 2027") -> not a tracked cycle
    return None


# --- location: US / Canada detection -----------------------------------------
# Full state/province names are matched case-insensitively; the 2-letter codes
# are matched case-SENSITIVELY (uppercase) so "OR"/"IN" don't match the words
# "or"/"in" inside a city name.
_US_STATES = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine",
    "maryland", "massachusetts", "michigan", "minnesota", "mississippi",
    "missouri", "montana", "nebraska", "nevada", "new hampshire", "new jersey",
    "new mexico", "new york", "north carolina", "north dakota", "ohio",
    "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont", "virginia",
    "washington", "west virginia", "wisconsin", "wyoming",
    "district of columbia",
]
_CA_PROVINCES = [
    "ontario", "quebec", "british columbia", "alberta", "manitoba",
    "saskatchewan", "nova scotia", "new brunswick", "newfoundland", "labrador",
    "prince edward island", "yukon", "northwest territories", "nunavut",
]
_US_CODES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "US", "USA",
]
_CA_CODES = ["ON", "QC", "BC", "AB", "MB", "SK", "NS", "NB", "NL", "PE", "YT", "NT", "NU"]

_US_COUNTRY = ("united states", "u.s.a", "u.s.", "u.s", "usa", "america")
_CA_COUNTRY = ("canada", "canadian")

_US_NAME_RE = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in _US_STATES) + r")\b", re.IGNORECASE
)
_CA_NAME_RE = re.compile(
    r"\b(" + "|".join(re.escape(n) for n in _CA_PROVINCES) + r")\b", re.IGNORECASE
)
# case-sensitive; (?!-) avoids matching country-style prefixes like "DE-Berlin"
# (Germany) as the US state code DE (Delaware).
_US_CODE_RE = re.compile(r"\b(" + "|".join(_US_CODES) + r")\b(?!-)")
_CA_CODE_RE = re.compile(r"\b(" + "|".join(_CA_CODES) + r")\b(?!-)")


def is_united_states(location: str) -> bool:
    if not location:
        return False
    low = location.lower()
    if any(token in low for token in _US_COUNTRY):
        return True
    if _US_NAME_RE.search(low):
        return True
    if _US_CODE_RE.search(location):
        return True
    return False


def is_canada(location: str) -> bool:
    if not location:
        return False
    low = location.lower()
    if any(token in low for token in _CA_COUNTRY):
        return True
    if _CA_NAME_RE.search(low):
        return True
    if _CA_CODE_RE.search(location):
        return True
    return False


def is_us_or_canada(location: str) -> bool:
    return is_united_states(location) or is_canada(location)


def region_ok(location: str, want_us: bool, want_canada: bool) -> bool:
    """True if the location matches one of the wanted regions.

    Conservative: a bare "Remote" with no country mentioned matches nothing.
    """
    if want_us and is_united_states(location):
        return True
    if want_canada and is_canada(location):
        return True
    return False


# --- category tagging (first match wins; order = specific before generic) -----
_CATEGORY_PATTERNS = [
    ("Quant", re.compile(r"\b(quant|quantitative|trading|trader)\b", re.IGNORECASE)),
    (
        "Data & ML/AI",
        re.compile(
            r"\b(data|machine learning|\bml\b|\bai\b|artificial intelligence|"
            r"deep learning|nlp|computer vision|research scientist|"
            r"applied scientist|analytics)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Hardware",
        re.compile(
            r"\b(hardware|electrical|firmware|asic|fpga|robotics|mechanical|"
            r"chip|silicon|manufacturing|industrial|analog|photonics|optical)\b",
            re.IGNORECASE,
        ),
    ),
    ("Security", re.compile(r"\b(cyber|infosec|appsec|security)", re.IGNORECASE)),
    (
        "Software",
        re.compile(
            r"\b(software|developer|swe|backend|frontend|full[\s-]?stack|"
            r"mobile|ios|android|devops|sre|infrastructure|platform|systems|"
            r"cloud|web|compiler|embedded|firmware|engineer|engineering|"
            r"programming|computer science)\b",
            re.IGNORECASE,
        ),
    ),
]


def categorize(title: str) -> str:
    for name, pattern in _CATEGORY_PATTERNS:
        if pattern.search(title):
            return name
    return "Other"


# ==============================================================================
# FORK ADDITIONS: non-technical AI roles + Triangle/remote location tiers
# ==============================================================================

# --- AI signal in a title ------------------------------------------------------
_AI_SIGNAL_RE = re.compile(
    r"\b(ai|a\.i\.|artificial intelligence|gen\s?ai|generative ai|genai|"
    r"machine learning|\bml\b|llm|large language model|chatbot|copilot|"
    r"conversational ai|responsible ai|ai/ml)\b",
    re.IGNORECASE,
)

# --- roles that are inherently AI even without "AI" in the title ---------------
# (prompt work, human feedback / RLHF, model evaluation, trust & safety)
_AI_NATIVE_RE = re.compile(
    r"\b(prompt(?:\s+(?:engineer(?:ing)?|specialist|writer|designer))?|"
    r"ai\s+trainer|model\s+train(?:er|ing)|rlhf|human\s+feedback|"
    r"model\s+evaluat(?:ion|or)|(?:llm|ai|model)\s+red\s+team(?:ing)?|"
    r"trust\s*(?:&|and)\s*safety|content\s+moderat(?:ion|or)|"
    r"data\s+annotat(?:ion|or)|ai\s+content|conversation\s+design)\b",
    re.IGNORECASE,
)

# --- business functions (the 8 target archetypes) -------------------------------
_BUSINESS_FN_RE = re.compile(
    r"\b(product\s+manage(?:r|ment)|\bapm\b|product\s+intern|product\s+strategy|"
    r"business\s+analyst|business\s+analytics|business\s+operations|biz\s?ops|"
    r"strategy|strategic|operations|chief\s+of\s+staff|program\s+manage(?:r|ment)|"
    r"project\s+manage(?:r|ment)|"
    r"marketing|growth|demand\s+gen(?:eration)?|brand|communications|"
    r"content\s+(?:marketing|strategy|specialist|writer)|social\s+media|"
    r"product\s+marketing|"
    r"policy|ethics|governance|compliance|regulatory|risk|legal\s+(?:intern|analyst)|"
    r"public\s+affairs|government\s+affairs|"
    r"sales|account\s+manage(?:r|ment)|account\s+executive|business\s+development|"
    r"partnerships?|customer\s+success|client\s+(?:success|services)|"
    r"go[\s-]to[\s-]market|gtm|revenue|sales\s+development|\bsdr\b|\bbdr\b|"
    r"research\s+analyst|market\s+research|insights?\s+(?:analyst|intern)|"
    r"consult(?:ing|ant))\b",
    re.IGNORECASE,
)

# --- engineering roles to hard-exclude ------------------------------------------
# Careful carve-outs: "prompt engineer" must survive (non-coding), so "engineer"
# is excluded only when NOT preceded by "prompt". "solutions engineer" and
# "sales engineer" are excluded (they normally require coding).
_ENG_EXCLUDE_RE = re.compile(
    r"\b(software|developer|swe|full[\s-]?stack|front[\s-]?end|back[\s-]?end|"
    r"devops|sre|site\s+reliability|infrastructure|"
    r"(?<!prompt\s)engineer(?:ing)?(?!\s*(?:manager\s+intern))|"
    r"(?:data|research|applied)\s+scien(?:ce|tist)|"
    r"machine\s+learning\s+(?:engineer|scientist|research)|ml\s+engineer|"
    r"ai\s+(?:engineer|researcher|scientist)|research\s+intern(?:ship)?\b.*\b(?:ml|ai)|"
    r"data\s+engineer|analytics\s+engineer|quantitative|quant\b|"
    r"cyber|security\s+(?:analyst|intern)|hardware|firmware|embedded|robotics|"
    r"mechanical|electrical|aerospace|civil|chemical|biomedical|"
    r"phd|ph\.d|doctoral)\b",
    re.IGNORECASE,
)


def is_ai_business(title: str) -> bool:
    """Keep only NON-ENGINEERING roles with a real AI angle.

    Two ways in:
      1. business function + explicit AI signal in the title
         ("AI Product Management Intern", "Marketing Intern, Generative AI")
      2. inherently-AI non-coding role, no AI word needed
         ("Prompt Engineer Intern", "Trust & Safety Intern", "AI Trainer")
    Either way, engineering-shaped titles are rejected first.
    """
    if _ENG_EXCLUDE_RE.search(title):
        # inherently-AI roles like "Prompt Engineer" survive the eng gate
        if not _AI_NATIVE_RE.search(title):
            return False
    if _AI_NATIVE_RE.search(title):
        return True
    return bool(_AI_SIGNAL_RE.search(title) and _BUSINESS_FN_RE.search(title))


# --- category tagging for the 8 archetypes (first match wins) --------------------
_AI_BIZ_CATEGORIES = [
    ("Trust & Safety", re.compile(
        r"\b(trust\s*(?:&|and)\s*safety|content\s+moderat\w*|rlhf|human\s+feedback|"
        r"ai\s+trainer|model\s+train\w*|red\s+team\w*|data\s+annotat\w*)\b", re.IGNORECASE)),
    ("Content & Prompt", re.compile(
        r"\b(prompt|ai\s+content|content\s+(?:specialist|writer|strategy)|"
        r"model\s+evaluat\w*|conversation\s+design)\b", re.IGNORECASE)),
    ("Policy & Ethics", re.compile(
        r"\b(policy|ethics|governance|compliance|regulatory|responsible\s+ai|"
        r"risk|public\s+affairs|government\s+affairs|legal)\b", re.IGNORECASE)),
    ("Product", re.compile(
        r"\b(product\s+manag\w*|apm|product\s+intern|product\s+strategy|"
        r"product\s+operations)\b", re.IGNORECASE)),
    ("Business Analysis", re.compile(
        r"\b(business\s+analy\w*|research\s+analyst|market\s+research|insights?|"
        r"reporting|metrics|roi)\b", re.IGNORECASE)),
    ("Marketing & Growth", re.compile(
        r"\b(marketing|growth|demand\s+gen|brand|communications|social\s+media|"
        r"content\s+marketing|gtm|go[\s-]to[\s-]market)\b", re.IGNORECASE)),
    ("Sales & Accounts", re.compile(
        r"\b(sales|account\s+manage|account\s+executive|business\s+development|"
        r"partnerships?|customer\s+success|client\s+success|revenue|sdr|bdr)\b",
        re.IGNORECASE)),
    ("Strategy & Ops", re.compile(
        r"\b(strategy|strategic|operations|biz\s?ops|chief\s+of\s+staff|"
        r"program\s+manage|project\s+manage|consult)\b", re.IGNORECASE)),
]


def categorize_ai_business(title: str) -> str:
    for name, pattern in _AI_BIZ_CATEGORIES:
        if pattern.search(title):
            return name
    return "Other"


# --- location tiers: Triangle > US remote > drop ---------------------------------
# Triangle cities need NC context only where the city name is ambiguous
# ("Durham" alone could be Durham UK; "Cary" and "Apex" exist elsewhere too),
# so we accept a Triangle city when NC / North Carolina also appears, OR when
# the city is distinctive enough on its own (Chapel Hill, RTP, Morrisville NC...).
_TRIANGLE_STRONG_RE = re.compile(
    r"\b(chapel\s+hill|research\s+triangle(?:\s+park)?|\brtp\b|carrboro|"
    r"raleigh[\s/-]durham|raleigh)\b",
    re.IGNORECASE,
)
_TRIANGLE_CITY_RE = re.compile(
    r"\b(durham|cary|morrisville|apex|hillsborough|garner|wake\s+forest)\b",
    re.IGNORECASE,
)
_NC_RE = re.compile(r"(?i:\bnorth\s+carolina\b)|\bNC\b")

_REMOTE_RE = re.compile(
    r"\b(remote|work\s+from\s+home|wfh|anywhere|distributed|virtual|"
    r"telecommute|home[\s-]based)\b",
    re.IGNORECASE,
)


def is_triangle(location: str) -> bool:
    if not location:
        return False
    if _TRIANGLE_STRONG_RE.search(location):
        return True
    return bool(_TRIANGLE_CITY_RE.search(location) and _NC_RE.search(location))


def is_remote_us(location: str) -> bool:
    """Remote roles count when US-scoped or location-agnostic.

    A bare "Remote" with no country is ACCEPTED here (unlike the original's
    conservative region gate) because dropping it loses too many legitimately
    US-open roles; anything explicitly foreign-scoped won't match the US gate
    upstream anyway.
    """
    if not location:
        return False
    return bool(_REMOTE_RE.search(location))


def loc_tier(location: str) -> str:
    """"triangle" | "remote" | "" (drop). Triangle wins over remote-hybrid."""
    if is_triangle(location):
        return "triangle"
    if is_remote_us(location):
        return "remote"
    return ""

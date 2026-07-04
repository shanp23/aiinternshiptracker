"""Coding-requirement classification from real posting text (the no-code edge).

This fork tracks NON-TECHNICAL AI roles, so the enrichment question is no longer
"does this employer sponsor visas?" but "does this role secretly require you to
already know how to code?". Same technique as the original sponsorship module:
phrase-anchored regex over the full posting body (whole expressions employers
actually write, never keyword soup), because a wrong verdict either hides a
great role or wastes an application.

Verdicts (checked in this order; strictest wins):
  coding-required — the posting demands prior programming / query-language
                    skill. These roles are DROPPED by the pipeline (the user
                    is strict: no prior coding, period).
  will-train      — the employer explicitly says no experience is needed or
                    that they'll teach the tools on the job. Badge: 📚
  tools-preferred — a data tool (SQL/Tableau/Power BI/...) is mentioned only
                    as a plus / nice-to-have, never required. Badge: 🧪
  unknown         — the text says nothing conclusive (kept, no badge).

Precision notes baked into the patterns:
  - "Excel" alone is NOT coding; it never triggers coding-required.
  - "prompt engineering" is NOT coding; a lookahead keeps it out of the
    programming-language trap.
  - "AI/ML" mentioned as subject matter isn't a requirement; only
    requirement-shaped phrases ("proficiency in", "experience with",
    "must know", "required: ...") trigger the drop.
"""

from __future__ import annotations

import re
from html import unescape

# Languages / query tools that mean "you must already code".
# NOTE: no bare "R" (matches initials everywhere); we require "R programming"
# or "R/Python"-style adjacency to count R.
_LANGS = (
    r"(?:python|sql|java(?:script)?|c\+\+|c#|typescript|scala|golang|\bgo\b|"
    r"ruby|matlab|sas\s+programming|r\s+programming|pyspark|spark|"
    r"pandas|numpy|scikit|tensorflow|pytorch)"
)

# Requirement-shaped lead-ins. These must be CLOSE to a language mention
# (within ~60 chars) so "our platform is built in Python" never triggers.
_REQ_LEAD = (
    r"(?:proficien\w+\s+(?:in|with)|fluen\w+\s+(?:in|with)|"
    r"experience\s+(?:in|with|using)|skilled\s+(?:in|with)|"
    r"expertise\s+(?:in|with)|strong\s+(?:knowledge|command|background)\s+(?:of|in)|"
    r"working\s+knowledge\s+of|hands[\s-]?on\s+experience\s+(?:in|with)|"
    r"must\s+(?:know|have|be\s+able\s+to\s+(?:code|program|write))|"
    r"required\s*:?\s*|ability\s+to\s+(?:code|program|write\s+code|write\s+queries)\s+(?:in|with|using)|"
    r"\d\+?\s+years?\s+(?:of\s+)?(?:experience\s+)?(?:in|with|using)?)"
)

_CODING_REQUIRED_RE = re.compile(
    r"("
    # requirement lead-in ... language, close together
    + _REQ_LEAD + r"[^.;\n]{0,60}?" + _LANGS +
    # or unmistakable standalone demands
    r"|coding\s+(?:skills?\s+)?(?:is\s+|are\s+)?required"
    r"|programming\s+(?:skills?\s+|experience\s+)?(?:is\s+|are\s+)?required"
    r"|must\s+be\s+able\s+to\s+(?:code|program)"
    r"|(?:cs|computer\s+science)\s+(?:degree|major)\s+(?:is\s+)?required"
    r"|pursuing\s+a\s+degree\s+in\s+computer\s+science(?!\s*(?:,|or\b|/|and\b))"  # CS-only, no "or business"
    r"|write\s+(?:production\s+)?code"
    r"|software\s+development\s+experience\s+(?:is\s+)?required"
    r")",
    re.IGNORECASE,
)

# Softeners: if a language appears ONLY inside one of these, it's not required.
_PREFERRED_RE = re.compile(
    r"(?:"
    r"(?:is|are)?\s*a\s+plus|nice[\s-]?to[\s-]?have|preferred(?:\s+but\s+not\s+required)?|"
    r"bonus(?:\s+points?)?|helpful\s+but\s+not\s+required|not\s+required|"
    r"a\s+bonus|desirable|advantageous"
    r")",
    re.IGNORECASE,
)

_TOOL_MENTION_RE = re.compile(
    r"\b(?:sql|tableau|power\s?bi|looker|python|excel|alteryx|snowflake|"
    r"salesforce|hubspot|jira|figma|" + "r\\s+programming" + r")\b",
    re.IGNORECASE,
)

_WILL_TRAIN_RE = re.compile(
    r"("
    r"no\s+(?:prior\s+|previous\s+)?(?:coding|programming|technical)\s+(?:experience|background|skills?)\s+(?:is\s+|are\s+)?(?:required|necessary|needed)"
    r"|no\s+experience\s+(?:is\s+)?(?:required|necessary|needed)"
    r"|we\s+(?:will|'ll)\s+(?:train|teach)"
    r"|training\s+(?:will\s+be\s+|is\s+)?provided"
    r"|willing(?:ness)?\s+to\s+learn"
    r"|eager(?:ness)?\s+to\s+learn"
    r"|learn\s+on\s+the\s+job"
    r"|you\s+(?:will|'ll)\s+(?:learn|be\s+trained|be\s+taught)"
    r"|no\s+technical\s+background\s+(?:is\s+)?(?:required|necessary|needed)"
    r")",
    re.IGNORECASE,
)

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")

# Badges shown next to a role title in the README / dashboard.
FLAGS = {
    "will-train": "\U0001f4da",       # 📚  they'll teach you
    "tools-preferred": "\U0001f9ea",  # 🧪  a tool is a plus, not required
}


def strip_html(html: str | None) -> str:
    """Plain text from an HTML blob — good enough for phrase matching."""
    if not html:
        return ""
    return _WS_RE.sub(" ", unescape(_TAG_RE.sub(" ", html))).strip()


def _required_hit_is_soft(plain: str, match: re.Match) -> bool:
    """True if a coding-required hit sits inside a 'preferred / a plus' clause.

    We look a short window AFTER the match (softeners usually trail:
    'experience with SQL is a plus') and a small window before.
    """
    start = max(0, match.start() - 40)
    end = min(len(plain), match.end() + 60)
    return bool(_PREFERRED_RE.search(plain[start:end]))


def classify(text: str | None) -> str:
    """Classify one posting's text. Strictest verdict wins.

    coding-required beats everything (the user is strict on no prior coding);
    will-train beats tools-preferred; anything inconclusive stays unknown.
    """
    if not text:
        return "unknown"
    plain = strip_html(text) if "<" in text else _WS_RE.sub(" ", text)

    m = _CODING_REQUIRED_RE.search(plain)
    if m and not _required_hit_is_soft(plain, m):
        # one soft hit doesn't clear the posting — check for a second, harder hit
        m2 = _CODING_REQUIRED_RE.search(plain, m.end())
        if not m2 or not _required_hit_is_soft(plain, m2):
            return "coding-required"
    elif m:
        m2 = _CODING_REQUIRED_RE.search(plain, m.end())
        if m2 and not _required_hit_is_soft(plain, m2):
            return "coding-required"

    if _WILL_TRAIN_RE.search(plain):
        return "will-train"

    # a tool named near a softener -> preferred, not required
    for tm in _TOOL_MENTION_RE.finditer(plain):
        start = max(0, tm.start() - 40)
        end = min(len(plain), tm.end() + 60)
        if _PREFERRED_RE.search(plain[start:end]):
            return "tools-preferred"

    return "unknown"


def flag(value: str | None) -> str:
    """The emoji shown next to a role title ('' when nothing to show)."""
    return FLAGS.get(value or "", "")

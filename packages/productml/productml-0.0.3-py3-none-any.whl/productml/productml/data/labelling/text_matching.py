from fuzzywuzzy import fuzz
from typing import List, Optional, Tuple


def _exact_match(brands: List[str], tokens: List[str]) -> str:
    for b in brands:
        if b in tokens:
            return 100, b, b
    return 0, "", ""


def _lowercase_match(brands: List[str], tokens: List[str]) -> str:
    _brands = [b.lower() for b in brands]
    _tokens = [t.lower() for t in tokens]
    return _exact_match(_brands, _tokens)


def _fuzzy_match(brands: List[str], tokens: List[str], threshold: float) -> str:
    assert threshold < 100 and threshold > 0
    _brands = [b.lower() for b in brands]
    _tokens = [t.lower() for t in tokens]
    best_match_brand = ""
    best_match_token = ""
    max_score = -1
    for b in _brands:
        for t in _tokens:
            score = fuzz.ratio(b, t)
            if score > max_score:
                max_score = score
                best_match_brand = b
                best_match_token = t
    if max_score > threshold:
        return max_score, best_match_brand, best_match_token
    else:
        return 0, "", ""


def match_brand(
    brands: List[str], tokens: List[str], algo: str, threshold: Optional[int]
) -> Tuple[int, str, str]:
    """
    matching_algo should return an empty string if there are no brand matches along with the score.
    """
    if algo == "exact":
        return exact_match(brands, tokens)
    elif algo == "fuzzy":
        return fuzzy_match(brands, tokens, threshold)
    else:
        raise NotImplementedError

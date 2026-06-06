"""Tests for kata 01 — parse_company."""

from kata_01_pydantic import Company, parse_company


def test_happy_path():
    happy = {
        "name": "Acme Wines",
        "domain": "acmewines.com",
        "status": "operating",
        "signals": [
            {
                "name": "website_live",
                "evidence": "Homepage returned 200 last month",
                "confidence": 0.9,
            },
            {
                "name": "recent_blog_post",
                "evidence": "Latest post March 2026",
                "confidence": 0.85,
            },
        ],
    }
    result = parse_company(happy)
    assert isinstance(result, Company)
    assert result.name == "Acme Wines"
    assert result.domain == "acmewines.com"
    assert result.status == "operating"
    assert len(result.signals) == 2


def test_missing_domain():
    no_domain = {
        "name": "Mystery Corp",
        "status": "uncertain",
        "signals": [
            {
                "name": "no_website",
                "evidence": "No website found in 3 searches",
                "confidence": 0.7,
            },
        ],
    }
    result = parse_company(no_domain)
    assert isinstance(result, Company)
    assert result.domain is None
    assert result.status == "uncertain"


def test_invalid_confidence():
    bad_conf = {
        "name": "BadConfidence Inc",
        "domain": "bad.com",
        "status": "operating",
        "signals": [
            {"name": "weird", "evidence": "some evidence string", "confidence": 1.5},
        ],
    }
    result = parse_company(bad_conf)
    assert isinstance(result, Company)
    assert result.status == "uncertain"
    assert result.signals == []

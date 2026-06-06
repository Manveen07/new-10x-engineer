import pytest
from kata_01_pydantic import Company, Signal
from kata_04_pytest import summarize


@pytest.fixture
def sample_company():
    return Company(
        name="Acme",
        domain="acme.com",
        status="operating",
        signals=[Signal(name="x", evidence="seen on homepage", confidence=0.9)],
    )


def test_summarize_uses_fixture(sample_company):
    result = summarize(sample_company)
    assert "Acme" in result
    assert "operating" in result


@pytest.mark.parametrize(
    "name,domain,status,expected_substr",
    [
        ("Acme", "acme.com", "operating", "operating"),
        ("Closed Co", "closed.com", "closed", "closed"),
        ("Mystery", None, "uncertain", "no domain"),
        ("Big Co", "big.com", "operating", "Big Co"),
    ],
)
def test_summarize_parametrized(name, domain, status, expected_substr):
    c = Company(name=name, domain=domain, status=status, signals=[])
    assert expected_substr in summarize(c)

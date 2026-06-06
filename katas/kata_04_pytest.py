from kata_01_pydantic import Company


def summarize(c: Company) -> str:
    """Return a one-line summary like:
    'Acme Wines (acmewines.com) — operating, 2 signals'
    For missing domain: '... (no domain) — ...'"""
    return f"{c.name} {f'{c.domain}' if c.domain else '(no domain)'}-{c.status} {len(c.signals)} signals"

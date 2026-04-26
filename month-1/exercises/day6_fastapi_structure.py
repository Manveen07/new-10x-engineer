"""
Day 6: FastAPI Structure And Dependency Injection

Goal:
    Scaffold the capstone like a real service: app factory, routers, schemas,
    services, repositories, dependencies, and lifespan-managed clients.

Capstone output:
    Update month-1/capstone/qa-api/app/ to match the target structure.

This is a guided exercise. Do not build a throwaway app; update the capstone.
"""

TARGET_STRUCTURE = """
app/
  main.py
  config.py
  lifespan.py
  dependencies.py
  errors.py
  routers/
    health.py
    auth.py
    users.py
    qa.py
    admin.py
  schemas/
    errors.py
    health.py
    auth.py
    users.py
    qa.py
    admin.py
  services/
    auth.py
    qa.py
    cache.py
    rate_limit.py
  repositories/
    users.py
    refresh_tokens.py
    queries.py
    provider_calls.py
  providers/
    base.py
    mock.py
    registry.py
  clients/
    db.py
    redis.py
    http.py
"""

APP_FACTORY_REQUIREMENTS = [
    "create_app() returns FastAPI",
    "routers are included inside create_app()",
    "lifespan creates and closes shared clients",
    "settings come from pydantic-settings",
    "routes use Depends() instead of global mutable state",
    "tests can override dependencies",
]

HEALTH_ENDPOINTS = [
    "GET /health/live returns {'status': 'ok'} without external checks",
    "GET /health/ready checks PostgreSQL and Redis",
]


def print_exercise() -> None:
    print("Day 6: FastAPI Structure")
    print("\nTarget structure:")
    print(TARGET_STRUCTURE)
    print("App factory requirements:")
    for item in APP_FACTORY_REQUIREMENTS:
        print(f"- {item}")
    print("\nHealth endpoints:")
    for item in HEALTH_ENDPOINTS:
        print(f"- {item}")


if __name__ == "__main__":
    print_exercise()

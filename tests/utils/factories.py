# Request payload factories for API tests.
import itertools

from dotenv import load_dotenv
load_dotenv('.env_5aed5591dc897f4e', override=True)

_counter = itertools.count(1)


def user_payload() -> dict[str, str]:
    n = next(_counter)
    return {"email": f"player{n}@example.com", "username": f"player{n}", "password": "password123"}


def game_payload() -> dict[str, object]:
    return {}


def move_payload(position: int = 0) -> dict[str, int]:
    return {"position": position}

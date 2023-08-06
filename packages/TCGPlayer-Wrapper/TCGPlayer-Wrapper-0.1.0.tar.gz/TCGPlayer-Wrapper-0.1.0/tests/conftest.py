import os

import pytest

from tcg_player.service import TCGPlayer
from tcg_player.sqlite_cache import SQLiteCache


@pytest.fixture(scope="session")
def client_id():
    return os.getenv("TCG_PLAYER_CLIENT_ID", default="Invalid")


@pytest.fixture(scope="session")
def client_secret():
    return os.getenv("TCG_PLAYER_CLIENT_SECRET", default="Invalid")


@pytest.fixture(scope="session")
def session(client_id, client_secret) -> TCGPlayer:
    session = TCGPlayer(
        client_id, client_secret, cache=SQLiteCache("tests/cache.sqlite", expiry=None)
    )
    return session

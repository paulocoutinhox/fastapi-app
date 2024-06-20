from unittest.mock import patch

from sqlalchemy.orm import Session

from helpers.db import get_db


def test_get_db(db: Session):
    with patch("helpers.db.SessionLocal", return_value=db):
        generator = get_db()
        db_session = next(generator)
        assert db_session == db
        generator.close()

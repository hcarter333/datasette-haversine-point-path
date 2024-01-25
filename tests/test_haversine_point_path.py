from datasette_haversine import prepare_connection
import sqlite3
import pytest

KD0FNR = 37.72489522009443, -122.422936174405
BELG = 51.9561076, 5.2400448
IONO = 45.07, -83.56


@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    prepare_connection(conn)
    return conn


@pytest.mark.parametrize(
    "unit,expected",
    (
        ("ft", 5805047),
        ("m", 1769378.36),
        ("in", 69660567),
        ("mi", 1099.44),
        ("nmi", 955.39),
        ("km", 1769.38),
    ),
)
@pytest.mark.parametrize("type", (float, str))
def test_haversine(conn, unit, expected, type):
    actual = conn.execute(
        "select haversine_point_path(?, ?, ?, ?, ?, ?, ?)",
        [type(KD0FNR[0]), type(KD0FNR[1]), type(BELG[0]), type(BELG[1]), type(IONO[0]), type(IONO[1]), unit],
    ).fetchall()[0][0]
    assert expected == pytest.approx(actual)

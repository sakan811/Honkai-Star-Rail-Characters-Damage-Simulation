import sqlite3

import pytest

from main import main


def test_full_process():
    main()

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Acheron')
        result = c.fetchall()
        assert result != []

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Seele')
        result = c.fetchall()
        assert result != []

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM ImbibitorLunae')
        result = c.fetchall()
        assert result != []

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Firefly')
        result = c.fetchall()
        assert result != []

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM DrRatio')
        result = c.fetchall()
        assert result != []

    with sqlite3.connect('hsr_dmg_calculation.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM Numby')
        result = c.fetchall()
        assert result != []


if __name__ == '__main__':
    pytest.main()

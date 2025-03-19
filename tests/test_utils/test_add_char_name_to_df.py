import pytest
import pandas as pd
from unittest.mock import Mock

from hsr_simulation.utils import add_char_name_to_df
from hsr_simulation.character import Character


@pytest.fixture
def mock_character():
    char = Mock(spec=Character)
    char.__class__.__name__ = "TestCharacter"
    return char


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "DMG": [100, 200, 300],
            "DMG_Type": ["Basic", "Skill", "Ultimate"],
            "Round": [1, 1, 2],
        }
    )


def test_add_char_name_normal_df(mock_character, sample_df):
    """Test add_char_name_to_df adds character name correctly"""
    add_char_name_to_df(mock_character, sample_df)

    assert "Character" in sample_df.columns
    assert all(sample_df["Character"] == "TestCharacter")
    assert len(sample_df) == 3


def test_add_char_name_empty_df(mock_character):
    """Test add_char_name_to_df with empty DataFrame"""
    empty_df = pd.DataFrame()
    add_char_name_to_df(mock_character, empty_df)

    assert "Character" in empty_df.columns
    assert len(empty_df) == 0

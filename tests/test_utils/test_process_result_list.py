import pytest
import pandas as pd
import sqlalchemy
from unittest.mock import Mock, patch

from hsr_simulation.utils import process_result_list
from hsr_simulation.character import Character

@pytest.fixture
def mock_character():
    char = Mock(spec=Character)
    char.__class__.__name__ = 'TestCharacter'
    return char

@pytest.fixture
def sample_dict_list():
    return [
        {'DMG': [100, 200], 'DMG_Type': ['Basic', 'Skill'], 'Round': [1, 1]},
        {'DMG': [300], 'DMG_Type': ['Ultimate'], 'Round': [2]}
    ]

@pytest.mark.parametrize("stage_table_name", ["test_table", "stage_dmg"])
def test_process_result_list_valid_input(mock_character, sample_dict_list, stage_table_name):
    """Test process_result_list with valid inputs"""
    mock_engine = Mock(spec=sqlalchemy.engine.Engine)
    
    with patch('hsr_simulation.utils.create_df_from_dict_list') as mock_create_df, \
         patch('hsr_simulation.utils.load_df_to_stage_table') as mock_load_df:
        mock_df = pd.DataFrame()
        mock_create_df.return_value = mock_df
        
        process_result_list(mock_character, mock_engine, sample_dict_list, stage_table_name)
        
        mock_create_df.assert_called_once_with(sample_dict_list)
        mock_load_df.assert_called_once_with(mock_df, mock_engine, stage_table_name)
        assert 'Character' in mock_df.columns

def test_process_result_list_empty_list(mock_character):
    """Test process_result_list with empty dict_list"""
    mock_engine = Mock(spec=sqlalchemy.engine.Engine)
    
    with patch('hsr_simulation.utils.create_df_from_dict_list') as mock_create_df, \
         patch('hsr_simulation.utils.load_df_to_stage_table') as mock_load_df:
        process_result_list(mock_character, mock_engine, [], "test_table")
        
        mock_create_df.assert_called_once_with([])
        mock_load_df.assert_called_once() 
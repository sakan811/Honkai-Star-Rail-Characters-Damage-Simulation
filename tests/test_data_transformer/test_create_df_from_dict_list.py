import pandas as pd
import numpy as np

from hsr_simulation.data_transformer import create_df_from_dict_list


def test_create_df_from_single_dict():
    """Test creating DataFrame from a list containing single dictionary"""
    test_data = [{
        'DMG': [1000, 2000],
        'DMG_Type': ['Normal', 'Critical'],
        'Simulate Round No.': [1, 1]
    }]
    
    result_df = create_df_from_dict_list(test_data)
    
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == ['DMG', 'DMG_Type', 'Simulate Round No.']
    assert len(result_df) == 2
    assert result_df['DMG'].tolist() == [1000, 2000]
    assert result_df['DMG_Type'].tolist() == ['Normal', 'Critical']
    assert result_df['Simulate Round No.'].tolist() == [1, 1]


def test_create_df_from_multiple_dicts():
    """Test creating DataFrame from a list containing multiple dictionaries"""
    test_data = [
        {
            'DMG': [1000],
            'DMG_Type': ['Normal'],
            'Simulate Round No.': [1]
        },
        {
            'DMG': [2000],
            'DMG_Type': ['Critical'],
            'Simulate Round No.': [2]
        }
    ]
    
    result_df = create_df_from_dict_list(test_data)
    
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2
    assert result_df['DMG'].tolist() == [1000, 2000]
    assert result_df['DMG_Type'].tolist() == ['Normal', 'Critical']
    assert result_df['Simulate Round No.'].tolist() == [1, 2]


def test_create_df_from_empty_list():
    """Test creating DataFrame from an empty list"""
    test_data = []
    
    result_df = create_df_from_dict_list(test_data)
    
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 0
    assert list(result_df.columns) == ['DMG', 'DMG_Type', 'Simulate Round No.']


def test_create_df_with_nan_values():
    """Test creating DataFrame with NaN values"""
    test_data = [{
        'DMG': [1000, np.nan],
        'DMG_Type': ['Normal', None],
        'Simulate Round No.': [1, 1]
    }]
    
    result_df = create_df_from_dict_list(test_data)
    
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2
    assert pd.isna(result_df['DMG'].iloc[1])
    assert pd.isna(result_df['DMG_Type'].iloc[1]) 
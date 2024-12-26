import pytest
from hsr_simulation.character import Character

@pytest.fixture
def character():
    return Character()

def test_action_value_calculation(character):
    """Test action value calculations"""
    test_speed = 100
    expected_value = Character.ACTION_VALUE_BASE / test_speed
    
    action_value = character.calculate_action_value(speed=test_speed)
    
    assert action_value == expected_value
    assert character.char_action_value == expected_value

def test_action_forward_simulation(character):
    """Test action forward simulation"""
    character.char_action_value = 100
    action_forward_percent = 0.5
    
    forward_value = character.simulate_action_forward(action_forward_percent)
    
    assert forward_value == 50.0 
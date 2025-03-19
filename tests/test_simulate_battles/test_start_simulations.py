from unittest.mock import Mock, patch
from hsr_simulation.simulate_battles import start_simulations
from hsr_simulation.character import Character


@patch("hsr_simulation.simulate_battles.simulate_cycles")
def test_start_simulations_basic(mock_simulate_cycles):
    """Test basic simulation with minimal parameters"""
    # Setup
    mock_char = Mock(spec=Character)
    mock_char.__class__.__name__ = "TestCharacter"
    mock_simulate_cycles.return_value = {"DMG": [100], "DMG_Type": ["Test"]}

    # Execute
    result = start_simulations(character=mock_char, max_cycles=5, simulation_num=3)

    # Verify
    assert len(result) == 3  # Should have 3 simulation results
    assert mock_simulate_cycles.call_count == 3
    mock_simulate_cycles.assert_any_call(mock_char, 5, 0)
    mock_simulate_cycles.assert_any_call(mock_char, 5, 1)
    mock_simulate_cycles.assert_any_call(mock_char, 5, 2)


@patch("hsr_simulation.simulate_battles.simulate_cycles")
def test_start_simulations_zero_simulations(mock_simulate_cycles):
    """Test with zero simulations"""
    mock_char = Mock(spec=Character)

    result = start_simulations(character=mock_char, max_cycles=5, simulation_num=0)

    assert len(result) == 0
    mock_simulate_cycles.assert_not_called()

from hsr_simulation.character import Character
from hsr_simulation.simulate_cycles import simulate_cycles


def test_simulate_turns_with_default_attributes():
    # Given: A character with default attributes
    character = Character()

    # When:
    result = simulate_cycles(character, max_cycles=5, simulate_round=1)

    # Then: Verify the result is a dictionary with expected keys
    assert isinstance(result, dict)
    assert "DMG" in result
    assert "DMG_Type" in result
    assert "Simulate Round No." in result
    assert len(result["DMG"]) > 0
    assert len(result["DMG_Type"]) > 0
    assert len(result["Simulate Round No."]) > 0


def test_simulate_turns_with_max_cycles_zero():
    # Given: A character with default attributes and max_cycles set to 0
    character = Character()

    # When: Simulating turns with max_cycles=0 and simulate_round=1
    result = simulate_cycles(character, max_cycles=0, simulate_round=1)

    # Then: Verify the result is a dictionary with no actions taken
    assert isinstance(result, dict)
    assert len(result["DMG"]) == 0
    assert len(result["DMG_Type"]) == 0
    assert len(result["Simulate Round No."]) == 0

import pytest

from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


@pytest.mark.parametrize(
    "bonus_spd, expected_bonus_turns",
    [
        (0, 0),  # Case: Base speed, no bonus speed
        (20, 1),  # Case: Speed matches the lowest breakpoint (120)
        (46, 3),  # Case: Speed matches a mid breakpoint (146)
        (100, 6),  # Case: Speed exceeds the highest breakpoint (200)
        (60, 3),  # Case: Speed equals a breakpoint threshold (160)
        (19, 0),  # Case: Speed just below a breakpoint (119)
        (21, 1),  # Case: Speed just above a breakpoint (121)
        (300, 6),  # Case: Very high bonus speed (400)
    ],
)
def test_calculate_spd_breakpoint(bonus_spd, expected_bonus_turns):
    character = HarmonyCharacter()  # Instantiate the character object
    result = character.calculate_spd_breakpoint(bonus_spd)
    assert result == expected_bonus_turns, f"Failed for bonus_spd={bonus_spd}: expected {expected_bonus_turns}, got {result}"

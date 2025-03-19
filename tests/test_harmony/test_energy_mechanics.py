from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


def test_regenerate_energy_normal():
    """Test normal energy regeneration."""
    char = HarmonyCharacter()
    char.regenerate_energy(30)
    assert char.trailblazer_current_energy == 30


def test_regenerate_energy_cap():
    """Test energy regeneration with cap."""
    char = HarmonyCharacter()
    char.trailblazer_current_energy = char.DEFAULT_ULT_ENERGY - 10
    char.regenerate_energy(30)
    assert char.trailblazer_current_energy == char.DEFAULT_ULT_ENERGY


def test_energy_regen_buff():
    """Test energy regeneration buff calculation."""
    char = HarmonyCharacter()
    buff = char.energy_regen_buff(60)
    assert buff == 0.5  # 60/120

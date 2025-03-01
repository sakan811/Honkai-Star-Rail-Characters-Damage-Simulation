from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

class TestRegenerateEnergy:
    def test_regenerate_energy_normal(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 50
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy(30)

        # Assert
        assert character.trailblazer_current_energy == 80

    def test_regenerate_energy_default_amount(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 50
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy()

        # Assert
        assert character.trailblazer_current_energy == 80  # Default amount = 30

    def test_regenerate_energy_exceed_max(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 90
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy(20)

        # Assert
        assert character.trailblazer_current_energy == 100  # Max cap applied

    def test_regenerate_energy_already_max(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 100
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy(50)

        # Assert
        assert character.trailblazer_current_energy == 100  # Shouldn't increase past max

    def test_regenerate_energy_zero_amount(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 60
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy(0)

        # Assert
        assert character.trailblazer_current_energy == 60  # No change when amount = 0

    def test_regenerate_energy_negative_amount(self):
        # Arrange
        character = HarmonyCharacter()
        character.trailblazer_current_energy = 60
        character.trailblazer_ult_energy = 100

        # Act
        character.regenerate_energy(-30)

        # Assert
        assert character.trailblazer_current_energy == 30  # Negative amount decreases energy

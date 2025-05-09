from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


class TestReduceEnemyToughness:
    def test_reduce_toughness_normal(self):
        # Arrange
        character = HarmonyCharacter()
        character.enemy_toughness = 100

        # Act
        character.reduce_enemy_toughness(30)

        # Assert
        assert character.enemy_toughness == 70

    def test_reduce_toughness_to_zero(self):
        # Arrange
        character = HarmonyCharacter()
        character.enemy_toughness = 50

        # Act
        character.reduce_enemy_toughness(60)

        # Assert
        assert character.enemy_toughness == 0

    def test_reduce_toughness_zero_amount(self):
        # Arrange
        character = HarmonyCharacter()
        character.enemy_toughness = 50

        # Act
        character.reduce_enemy_toughness(0)

        # Assert
        assert character.enemy_toughness == 50

    def test_reduce_toughness_never_negative(self):
        # Arrange
        character = HarmonyCharacter()
        character.enemy_toughness = 10

        # Act
        character.reduce_enemy_toughness(20)

        # Assert
        assert character.enemy_toughness == 0  # Ensure toughness does not go negative

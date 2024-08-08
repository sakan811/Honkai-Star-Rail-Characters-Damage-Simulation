#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger


class Summon(Character):
    """
    Base class for a Summon character for characters like Topaz, Jing Yuan, etc.
    """

    def __init__(
            self,
            base_char: Character,
            speed: float = 80,
            ult_energy: int = 0
    ):
        super().__init__(atk=base_char.default_atk, crit_rate=base_char.default_crit_rate,
                         crit_dmg=base_char.crit_dmg, speed=speed, ult_energy=ult_energy)
        self.summon_action_value_for_action_forward = []

    def reset_summon_stat(self) -> None:
        """
        Reset Summon stats
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} stats ...')
        self.summon_action_value_for_action_forward = []


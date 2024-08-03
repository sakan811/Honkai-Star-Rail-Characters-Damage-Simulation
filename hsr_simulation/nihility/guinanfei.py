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
import random

from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.character import Character

script_logger = configure_logging_with_file(log_dir='logs', log_file='guinanfei.log',
                                            logger_name='guinanfei', level='DEBUG')


class Guinanfei(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 106,
            ult_energy: int = 120
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.burn = 0
        self.firekiss = []
        self.a6_dmg_multiplier = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        script_logger.info(f'Simulate enemy turn')
        if self.burn > 0:
            self.burn -= 1
            self._apply_dot()
            if len(self.firekiss) > 0:
                self.firekiss[0] -= 1
                if self.firekiss[0] == 0:
                    self.firekiss = []

        if self.battle_start:
            script_logger.debug(f'Battle Start. Apply A4 trace effect')
            self.battle_start = False
            self.speed *= 1.25
        else:
            self.speed = 106

        if self.burn > 0:
            self.a6_dmg_multiplier = 0.2
        else:
            self.a6_dmg_multiplier = 0

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        script_logger.info(f"{self.__class__.__name__} is using basic attack...")
        if len(self.firekiss) > 0:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10,
                                                       dmg_multipliers=[0.07 * len(self.firekiss), self.a6_dmg_multiplier])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10,
                                                       dmg_multipliers=[self.a6_dmg_multiplier])

        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        # simulate A2 Trace
        if random.random() < 0.8:
            script_logger.debug(f'Apply Burn from A2 trace effect')
            self.burn = 2

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info(f"{self.__class__.__name__} is using skill...")
        if len(self.firekiss) > 0:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.2, break_amount=20,
                                                       dmg_multipliers=[0.07 * len(self.firekiss), self.a6_dmg_multiplier])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.2, break_amount=20,
                                                       dmg_multipliers=[self.a6_dmg_multiplier])

        self.enemy_toughness -= break_amount

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

        self.burn = 2

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__} is using ultimate...')

        if len(self.firekiss) > 0:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.2, break_amount=20,
                                                       dmg_multipliers=[0.07 * len(self.firekiss), self.a6_dmg_multiplier])
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=1.2, break_amount=20,
                                                       dmg_multipliers=[self.a6_dmg_multiplier])

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        if self.burn > 0:
            self._apply_dot(ult_trigger=True)

    def _apply_dot(self, ult_trigger: bool = False) -> None:
        """
        Simulate dot damage.
        :param ult_trigger: Whether the DoT is triggered by Ultimate
        :return: None
        """
        script_logger.info(f'{self.__class__.__name__} is applying dot...')
        if len(self.firekiss) > 0:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.182, break_amount=0,
                                                       dmg_multipliers=[0.07 * len(self.firekiss), self.a6_dmg_multiplier],
                                                       can_crit=False)
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.182, break_amount=0,
                                                       dmg_multipliers=[self.a6_dmg_multiplier], can_crit=False)

        if ult_trigger:
            dmg *= 0.92

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('DoT')

        if len(self.firekiss) < 3:
            self.firekiss.append(3)

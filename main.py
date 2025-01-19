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
import argparse
from typing import List

from hsr_simulation.path_main_func.destruction_main import start_sim_destruction
from hsr_simulation.path_main_func.erudition_main import start_sim_erudition
from hsr_simulation.path_main_func.harmony_main import start_sim_harmony
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.path_main_func.remembrance_main import start_sim_remembrance
from hsr_simulation.path_main_func.hunt_main import start_sim_hunt
from hsr_simulation.path_main_func.nihility_main import start_sim_nihility


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run HSR character damage simulations")
    parser.add_argument(
        "--paths",
        type=str,
        nargs="+",
        choices=["Hunt", "Nihility", "Destruction", "Erudition", "Harmony", "Remembrance"],
        help="Specify which paths to simulate. If not provided, all paths will be simulated.",
    )
    parser.add_argument(
        "--sim-count",
        type=int,
        default=1000,
        help="Number of simulations to run (default: 1000)",
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=10,
        help="Maximum number of cycles to simulate (default: 10)",
    )
    return parser.parse_args()


def run_simulations(paths: List[str], simulation_num: int, max_cycles: int) -> None:
    """Run damage simulations for specified character paths.

    This function executes damage simulations for the specified character paths using the given parameters.
    Each path's simulation is run independently, and any errors in one path's simulation will not affect others.

    Args:
        paths (List[str]): List of paths to simulate. Valid values are 'Hunt', 'Nihility', 'Destruction',
                          'Erudition', and 'Harmony'.
        simulation_num (int): Number of battle simulations to run for each path.
        max_cycles (int): Maximum number of cycles to simulate in each battle.

    Note:
        - The Harmony path currently doesn't use simulation_num and max_cycles parameters
        - If a path's simulation fails, an error will be logged but execution will continue for remaining paths
    """
    path_to_func = {
        "Hunt": start_sim_hunt,
        "Nihility": start_sim_nihility,
        "Destruction": start_sim_destruction,
        "Erudition": start_sim_erudition,
        "Harmony": lambda x, y: start_sim_harmony(),  # Harmony doesn't take args currently
        "Remembrance": start_sim_remembrance,
    }

    for path in paths:
        try:
            main_logger.info(f"Starting simulation for {path} path...")
            if path == "Harmony":
                path_to_func[path](None, None)
            else:
                path_to_func[path](simulation_num, max_cycles)
        except Exception as e:
            main_logger.error(f"Error in {path} simulation: {e}", exc_info=True)


if __name__ == "__main__":
    args = parse_args()

    # If no paths specified, run all
    paths_to_run = (
        args.paths
        if args.paths
        else ["Hunt", "Nihility", "Destruction", "Erudition", "Harmony", "Remembrance"]
    )

    try:
        run_simulations(paths_to_run, args.sim_count, args.max_cycles)
    except Exception as e:
        main_logger.error(e, exc_info=True)
        main_logger.error("Unexpected error occurred.")

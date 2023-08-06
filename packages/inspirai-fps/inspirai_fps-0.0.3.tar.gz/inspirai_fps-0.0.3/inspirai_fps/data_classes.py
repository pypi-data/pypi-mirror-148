from typing import Union, List, NamedTuple
from enum import Enum, unique
from simple_command_pb2 import GameState
from queue import Queue

Number = Union[int, float]


class Vector3D(NamedTuple):
    x: Number
    y: Number
    z: Number


class Orientation(NamedTuple):
    pitch: Number
    yaw: Number
    roll: Number


class SupplyInfo(NamedTuple):
    supply_id: int = 0
    supply_location: Vector3D = Vector3D(0, 0, 0)
    supply_amount: int = 0


class EnemyInfo(NamedTuple):
    enemy_id: int = 0
    enemy_dir: Vector3D = Vector3D(0, 0, 0)  # direction to enemy
    enemy_health: int = 0
    enemy_distance: Number = 0  # distance to enemy


class AgentObservation(NamedTuple):
    """a data class that wraps agent observation properties"""

    camera_angle: Orientation = Orientation(0, 0, 0)
    location: Vector3D = Vector3D(0, 0, 0)
    move_dir: Vector3D = Vector3D(0, 0, 0)
    move_speed: Number = 0
    health: Number = 0
    weapon_ammo: Number = 0
    spare_ammo: Number = 0
    on_ground: bool = True
    is_attack: bool = False
    is_reload: bool = False
    hit_enemy: bool = False
    hit_by_enemy: bool = False
    num_supply: int = 0
    is_waiting_respawn: bool = False
    is_invincible: bool = False
    supplies: List[SupplyInfo] = []
    enemies: List[EnemyInfo] = []


class AgentAction(NamedTuple):
    """a data class that wraps agent action properties"""

    walk_dir: Number = 0
    walk_speed: Number = 0
    turn_lr_delta: Number = 0
    look_up_delta: Number = 0
    jump: bool = False
    pickup: bool = False
    shoot: bool = False
    reload: bool = False


class MyGameState(Enum):
    START = 0
    UPDATE = 1
    END = 2


import grpc
import logging
import subprocess
from concurrent import futures
import simple_command_pb2
import simple_command_pb2_grpc
from attrs import define


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@define
class GameConfig:
    """
    GameConfig is a data class that wraps game configuration properties
    """

    port: int = 50051
    timeout: int = 10
    game_mode: int = 0
    time_scale: int = 100
    map_id: int = 1
    random_seed: int = 0
    num_rounds: int = 1
    trigger_range: float = 1
    engine_dir: str = "../unity3d"
    map_dir: str = "../data"
    num_agents: int = 1
    use_depth_map: bool = False
    record: bool = False
    replay_suffix: str = ""
    start_location: Vector3D = Vector3D(0, 0, 0)
    target_location: Vector3D = Vector3D(5, 0, 5)
    walk_speed: float = 1


class QueueServer(simple_command_pb2_grpc.CommanderServicer):
    def __init__(self, request_queue, response_queue) -> None:
        super().__init__()
        self.request_queue = request_queue
        self.response_queue = response_queue

    def Request_S2A_UpdateGame(self, request, context):
        self.request_queue.put(request)
        logging.info("Put request into queue ...")
        logging.info(request)

        reply = self.response_queue.get()
        logging.info("Get reply from queue ...")
        logging.info(reply)

        return reply


class SimpleGame:
    GameStateMap = {
        GameState.start: MyGameState.START,
        GameState.update: MyGameState.UPDATE,
        GameState.over: MyGameState.END,
    }

    class Mode(Enum):
        NAVIGATION = 0
        SUP_GATHER = 1
        SUP_BATTLE = 2

    def __init__(self) -> None:
        self.__game_state = None
        self.__time_step = 0
        self.__engine_path = "../unity3d/fps.x86_64"
        self.__engine_log_dir = "../unity3d/logs"
        self.__request_queue = Queue()
        self.__response_queue = Queue()
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        simple_command_pb2_grpc.add_SimpleCommandServicer_to_server(
            QueueServer(self.__request_queue, self.__response_queue), self.__server
        )
        self.__server.add_insecure_port("[::]:50051")

    def get_agent_obs(self) -> AgentObservation:
        return AgentObservation()

    def send_agent_action(self, action: AgentAction) -> None:
        pass

    def init(self) -> None:
        self.__server.start()
        logging.info("Server started ...")

        # start a subprocess to run the game engine
        # and redirect stdout and stderr to log file
        self.__engine_process = subprocess.Popen(
            [self.__engine_path, "--log-file", self.__engine_log_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info("Engine started ...")

        # wait for the game engine to start
        self.__request_queue.get()  # wait for the first request
        logging.info("Game engine started ...")

    def is_episode_finished(self):
        return self.__game_state == MyGameState.END

    def new_episode(self):
        response = simple_command_pb2.A2S_Reply_Data()
        response.game_state = GameState.reset

    def __set_GM(self, gm_cmd):
        pass

    @property
    def game_state(self):
        return self.__game_state

    @property
    def time_step(self):
        return self.__time_step

    def __repr__(self) -> str:
        return f"SimpleGame(game_state={self.game_state}, time_step={self.time_step})"


if __name__ == "__main__":
    print(
        AgentObservation(
            supplies=[
                SupplyInfo(
                    supply_id=1, supply_location=Vector3D(1, 2, 3), supply_amount=10
                )
            ],
        )
    )
    print(AgentAction(walk_dir=19))

    game = SimpleGame()

    print(game)

    game.init()

    # print(game)

    print(game.game_state)

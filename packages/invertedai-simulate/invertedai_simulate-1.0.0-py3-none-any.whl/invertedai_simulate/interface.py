from .zmq_client import ApiMessagingClient
from typing import Dict, Tuple, Any
import argparse
import numpy as np
import matplotlib.pyplot as plt
import gym
from halo import Halo


Action = Tuple[float, float]
Obs = Dict[str, np.ndarray]


class ClientHandshakeError(Exception):
    pass


class ServerTimeoutError(Exception):
    pass


class IAIEnv(gym.Env):
    """
    A gym environment that connects to the iai server application running the simulation
    """
    def __init__(self, config):
        self.zmq_server_address = f"tcp://{config.zmq_server_address}"
        self.client_id = config.client_id
        self.remote = ApiMessagingClient(self.zmq_server_address, self.client_id)
        self.enable_progress_spinner = config.enable_progress_spinner
        for i in range(config.num_handshake_tries):
            if self.remote.client_handshake():
                break
        else:
            raise ClientHandshakeError
        self.state = None
        self.obs = None

    def set_scenario(self, scenario_name, world_parameters=None, vehicle_physics=None, scenario_parameters=None,
                     sensors=None):
        """

        :param scenario_name:
        :type scenario_name:
        :param world_parameters:
        :type world_parameters:
        :param vehicle_physics:
        :type vehicle_physics:
        :param scenario_parameters:
        :type scenario_parameters:
        :param sensors:
        :type sensors:
        :return:
        :rtype:
        """
        with Halo(text=f'Loading: {scenario_name} scenario', spinner='dots', enabled=self.enable_progress_spinner):
            self.remote.initialize(scenario_name, world_parameters, vehicle_physics, scenario_parameters, sensors)
            _, message = self.remote.get_reply()
        return message

    def get_map(self):
        """
        Returns the map of the scenario in OSM format
        """
        raise NotImplementedError

    def set_goal_location(self):
        """
        Returns the current location of all agents
        """
        pass

    def reset(self, rand_seed=None):
        """
        Restarts the scenario
        :param rand_seed
        """
        if rand_seed is None:
            rand_seed = 0
        self.remote.send_command("reset", {'tensor': np.array(rand_seed)})
        _, message = self.remote.get_reply()
        self.obs = message
        return message

    def visualize_fig(self, fig):
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.imshow(self.obs['front_image'].squeeze().permute(1, 2, 0))
        ax1.axis('off')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.imshow(self.obs['birdview_image'].squeeze().permute(1, 2, 0))
        ax2.axis('off')
        plt.ion()
        plt.show()
        plt.pause(0.001)

    def render(self, mode="human"):
        pass

    def step(self, action: Action) -> Tuple[object, float, bool, dict]:
        """
        Accepts the next action of the ego vehicle and generates the next state of all
        the agents in the world
        :param action:
        :type action:
        :return:
        :rtype:
        """
        self.remote.send_command("step", {'step': action})
        _, message = self.remote.get_reply()
        obs = message['obs']
        reward = message['reward']
        done = message['done']
        info = message['info']
        return obs, reward, done, info

    def get_reward(self) -> float:
        return self.state['reward']

    def get_done(self) -> bool:
        return self.state['done']

    def get_info(self) -> Dict[str, Any]:
        return self.state['info']

    def close(self):
        self.remote.close()

    def end_simulation(self):
        self.remote.send_command("end")
        message = self.remote.listen()
        return message.decode()

    def get_actions(self):
        self.remote.send_command("serverdrive", {'tensor': np.array(0)})
        message = self.remote.listen()
        return message.decode()

    @staticmethod
    def add_config(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--num_handshake_tries', type=int, default=10)
        parser.add_argument('--zmq_server_address', type=str, default='localhost:5555')
        parser.add_argument('--client_id', type=str, default='0')
        parser.add_argument('--enable_progress_spinner', type=int, default=1)


gym.register('iai/GenericEnv-v0', entry_point=IAIEnv)

# coding=utf-8
# Copyright 2020 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple sensors related to the environment."""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from policydissect.quadrupedal.vision4leg.envs.sensors import sensor
import typing
import numpy as np

import os
import inspect
currentdir = os.path.dirname(os.path.abspath(
  inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)


_ARRAY = typing.Iterable[float]  # pylint:disable=invalid-name
_FLOAT_OR_ARRAY = typing.Union[float, _ARRAY]  # pylint:disable=invalid-name
_DATATYPE_LIST = typing.Iterable[typing.Any]  # pylint:disable=invalid-name


class LastActionSensor(sensor.BoxSpaceSensor):
  """A sensor that reports the last action taken."""

  def __init__(self,
               num_actions: int,
               lower_bound: _FLOAT_OR_ARRAY = -1.0,
               upper_bound: _FLOAT_OR_ARRAY = 1.0,
               name: typing.Text = "LastAction",
               dtype: typing.Type[typing.Any] = np.float64) -> None:
    """Constructs LastActionSensor.

    Args:
      num_actions: the number of actions to read
      lower_bound: the lower bound of the actions
      upper_bound: the upper bound of the actions
      name: the name of the sensor
      dtype: data type of sensor value
    """
    self._num_actions = num_actions
    self._env = None

    super(LastActionSensor, self).__init__(name=name,
                                           shape=(self._num_actions,),
                                           lower_bound=lower_bound,
                                           upper_bound=upper_bound,
                                           dtype=dtype)

  def on_reset(self, env):
    """From the callback, the sensor remembers the environment.

    Args:
      env: the environment who invokes this callback function.
    """
    self._env = env

  def _get_observation(self) -> _ARRAY:
    """Returns the last action of the environment."""
    return self._env.last_action


class GoalPosSensor(sensor.BoxSpaceSensor):
  """A sensor that reports the goal position taken."""

  def __init__(self,
               goal_dim=3,
               name: typing.Text = "GoalPos",
               dtype: typing.Type[typing.Any] = np.float64) -> None:
    """Constructs LastActionSensor.

    Args:
      num_actions: the number of actions to read
      lower_bound: the lower bound of the actions
      upper_bound: the upper bound of the actions
      name: the name of the sensor
      dtype: data type of sensor value
    """
    self._goal_dim = goal_dim
    self._env = None

    super(GoalPosSensor, self).__init__(name=name,
                                        shape=(self._goal_dim * 2,),
                                        dtype=dtype)

  def on_reset(self, env):
    """From the callback, the sensor remembers the environment.

    Args:
      env: the environment who invokes this callback function.
    """
    self._env = env

  def _get_observation(self) -> _ARRAY:
    """Returns the last action of the environment."""
    return np.concatenate([np.array(self._env._robot.GetBasePosition()), self._env.world_dict["goal_pos"]])


class ForceSensor(sensor.BoxSpaceSensor):
  """A sensor that reports the feet contact forces."""

  def __init__(self,
               goal_dim=24,
               name: typing.Text = "Force",
               dtype: typing.Type[typing.Any] = np.float64) -> None:
    """Constructs LastActionSensor.

    Args:
      num_actions: the number of actions to read
      lower_bound: the lower bound of the actions
      upper_bound: the upper bound of the actions
      name: the name of the sensor
      dtype: data type of sensor value
    """
    self._env = None
    self.feet_id = [2 + 3 * i for i in range(4)]

    super(ForceSensor, self).__init__(name=name,
                                      shape=(24,),
                                      dtype=dtype)

  def on_reset(self, env):
    """From the callback, the sensor remembers the environment.

    Args:
      env: the environment who invokes this callback function.
    """
    self._env = env

  def _get_observation(self) -> _ARRAY:
    """Returns the last action of the environment."""
    f1, f2, f3, f4 = self._env._pybullet_client.getJointStates(
      self._robot.quadruped, self.feet_id)
    forces = np.concatenate([np.array(f1[2]), np.array(f2[2]),
                             np.array(f3[2]), np.array(f4[2])], axis=0)
    return forces

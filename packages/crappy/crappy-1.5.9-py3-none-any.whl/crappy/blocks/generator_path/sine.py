# coding: utf-8

from time import time
import numpy as np
from typing import Union, Callable

from .path import Path


class Sine(Path):
  """To generate a sine wave."""

  def __init__(self,
               time: float,
               cmd: float,
               condition: Union[str, bool, Callable],
               freq: float,
               amplitude: float,
               offset: float = 0,
               phase: float = 0) -> None:
    """Sets the args and initializes parent class.

    Args:
      time:
      cmd:
      condition (:obj:`str`): Representing the condition to end this path. See
        :ref:`generator path` for more info.
      freq: Frequency of the sine in `Hz`.
      amplitude: Amplitude of the sine wave.
      offset (optional): Offset of the sine.
      phase (optional): Phase of the sine.
    """

    Path.__init__(self, time, cmd)
    self.condition = self.parse_condition(condition)
    self.amplitude = amplitude / 2
    self.offset = offset
    self.phase = phase
    self.k = 2 * np.pi * freq

  def get_cmd(self, data: dict) -> float:
    if self.condition(data):
      raise StopIteration
    return np.sin((time() - self.t0) * self.k - self.phase) * \
        self.amplitude + self.offset

# coding: utf-8

from typing import Union, Callable
from .path import Path


class Constant(Path):
  """Simplest condition. It will send value until condition is reached."""

  def __init__(self,
               time: float,
               cmd: float,
               condition: Union[str, bool, Callable],
               send_one: bool = True,
               value: float = None) -> None:
    """Sets the args and initializes parent class.

    Args:
      time:
      cmd:
      condition (:obj:`str`): Representing the condition to end this path. See
        :ref:`generator path` for more info.
      send_one (:obj:`str`, optional): If :obj:`True`, this condition will send
        the value at least once before checking the condition.
      value: What value must be sent.
    """

    Path.__init__(self, time, cmd)
    self.condition = self.parse_condition(condition)
    self.value = cmd if value is None else value
    if send_one:
      self.get_cmd = self.get_cmd_first
    else:
      self.get_cmd = self.get_cmd_condition

  def get_cmd_first(self, _) -> float:
    self.get_cmd = self.get_cmd_condition
    return self.value

  def get_cmd_condition(self, data: dict) -> float:
    if self.condition(data):
      raise StopIteration
    return self.value

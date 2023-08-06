# coding: utf-8

from .cameralink import Cl_camera
from .._global import OptionalModule
try:
  from . import clModule as Cl
except (ModuleNotFoundError, ImportError):
  Cl = OptionalModule("clModule")


class Jai8(Cl_camera):
  """This class supports Jai GO-5000-PMCL gray cameras.

  This one uses FullAreaGray8 module for maximum framerate.
  """

  def __init__(self, **kwargs) -> None:
    if 'camera_type' not in kwargs:
      kwargs['camera_type'] = "FullAreaGray8"
    if 'config_file' not in kwargs:
      kwargs['config_file'] = False
    Cl_camera.__init__(self, **kwargs)
    self.settings['width'].limits = (1, 2560)
    self.settings['width'].default = 2560
    self.settings['height'].limits = (1, 2048)
    self.settings['height'].default = 2048
    self.add_setting('exposure', setter=self._set_exp, getter=self._get_exp,
                     limits=(10, 800000))

  def _set_w(self, val: int) -> None:
    self.stopAcq()
    Cl_camera._set_w(self, val)
    self.cap.serialWrite('WTC={}\r\n'.format(val))
    self.startAcq()

  def _set_h(self, val: int) -> None:
    self.stopAcq()
    Cl_camera._set_h(self, val)
    self.cap.serialWrite('HTL={}\r\n'.format(val))
    self.startAcq()

  def _get_format(self) -> int:
    r = self.cap.serialWrite('BA?\r\n')
    return int(r[3])

  def _set_format(self, val: int) -> None:
    self.cap.serialWrite('BA={}\r\n'.format(val))

  def _set_exp(self, val: int) -> None:
    self.cap.serialWrite('PE={}\r\n'.format(val))

  def _get_exp(self) -> int:
    return int(self.cap.serialWrite('PE?\r\n').strip()[3:])

  def get_image(self) -> tuple:
    return Cl_camera.get_image(self)

  def close(self) -> None:
    Cl_camera.close(self)

  def open(self, **kwargs) -> None:
    Cl_camera.open(self, **kwargs)
    self.cap.serialWrite('TAGM=5\r\n')  # (default)
    self._set_format(0)  # Set camera to 8 bits
    self.cap.set(Cl.FG_CAMERA_LINK_CAMTYP, 208)  # Set the input to 8 bits
    self.cap.set(Cl.FG_SENSORREADOUT, 0)  # Sets the correct framegrabber mode


class Jai(Jai8):
  """This class allows the use of 10 and 12 bits mode for the Jai Cameras.
  Obviously, the framerate will be slower than the 8 bits version."""

  def __init__(self, **kwargs) -> None:
    kwargs['camera_type'] = "MediumAreaGray16"
    Jai8.__init__(self, **kwargs)
    self.add_setting("data_format", setter=self._set_format, default=2,
                     getter=self._get_format,
                     limits={'10 bits': 1, '12 bits': 2})

  def get_image(self) -> tuple:
    t, f = Cl_camera.get_image(self)
    return t, f >> 4

  def open(self) -> None:
    Cl_camera.open(self)
    # dual tap (default does not allow 12 bits)
    self.cap.serialWrite('TAGM=1\r\n')
    self._set_format(2)  # 12 bits
    self.cap.set(Cl.FG_CAMERA_LINK_CAMTYP, 212)  # Set the input to 12 bits
    self.cap.set(Cl.FG_SENSORREADOUT, 7)  # Sets the correct framegrabber mode

  def close(self) -> None:
    Jai8.close(self)

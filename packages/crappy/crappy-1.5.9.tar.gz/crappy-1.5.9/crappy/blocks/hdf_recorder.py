# coding: utf-8

from os import path, makedirs
import numpy as np

from .._global import OptionalModule
try:
  import tables
except ModuleNotFoundError:
  tables = OptionalModule("tables", "Hdf_recorder needs the tables module to "
                          "write hdf files.")

from .block import Block


class Hdf_recorder(Block):
  """To save data efficiently in a hdf5 file.

  This block is is meant to save data coming by arrays at a high rate
  (`>1kHz`). It uses the module :mod:`tables`.

  Important:
    Do not forget to specify the type of data to be saved (see ``atom``
    parameter) to avoid casting the data into another type, as this could
    result in data loss or inefficient saving.
  """

  def __init__(self,
               filename: str,
               node: str = 'table',
               expected_rows: int = 10**8,
               atom=None,
               label: str = 'stream',
               metadata: dict = None) -> None:
    """Sets the args and initializes the parent class.

    Args:
      filename (:obj:`str`): Path of the file where the data should be saved.
      node (:obj:`str`, optional): The name of the node where the data will be
        saved.
      expected_rows (:obj:`int`, optional): The number of expected rows in the
        file. It is used to optimize the dumping.
      atom (optional): This represent the type of data to be stored in the
        table. It can be given as a :class:`tables.Atom` instance, as a
        :class:`numpy.array` or as a :obj:`str`.
      label (:obj:`str`, optional): The key of the :obj:`dict` that contains
        the array to save.
      metadata (:obj:`dict`, optional): A :obj:`dict` containing additional
        info to save in the `hdf5` file.
    """

    Block.__init__(self)
    self.filename = filename
    self.node = node
    self.expected_rows = expected_rows
    self.atom = tables.Int16Atom() if atom is None else atom
    self.label = label
    self.metadata = {} if metadata is None else metadata

    if not isinstance(self.atom, tables.Atom):
      self.atom = tables.Atom.from_dtype(np.dtype(self.atom))

  def prepare(self) -> None:
    assert self.inputs, "No input connected to the hdf_recorder!"
    assert len(self.inputs) == 1,\
        "Cannot link more than one block to a hdf_recorder!"
    d = path.dirname(self.filename)
    if not path.exists(d):
      # Create the folder if it does not exist
      try:
        makedirs(d)
      except OSError:
        assert path.exists(d), "Error creating " + d
    if path.exists(self.filename):
      # If the file already exists, append a number to the name
      print("[hdf_recorder] WARNING!", self.filename, "already exists !")
      name, ext = path.splitext(self.filename)
      i = 1
      while path.exists(name + "_%05d" % i + ext):
        i += 1
      self.filename = name + "_%05d" % i + ext
      print("[hdf_recorder] Using", self.filename, "instead!")
    self.hfile = tables.open_file(self.filename, "w")
    for name, value in self.metadata.items():
      self.hfile.create_array(self.hfile.root, name, value)

  def begin(self) -> None:
    data = self.inputs[0].recv_chunk()
    w = data[self.label][0].shape[1]
    self.array = self.hfile.create_earray(
        self.hfile.root,
        self.node,
        self.atom,
        (0, w),
        expectedrows=self.expected_rows)
    for d in data[self.label]:
      self.array.append(d)

  def loop(self) -> None:
    data = self.inputs[0].recv_chunk()
    for d in data[self.label]:
      self.array.append(d)

  def finish(self) -> None:
    self.hfile.close()


class Hdf_saver(Hdf_recorder):
  def __init__(self, *args, **kwargs) -> None:
    print('#### WARNING ####\n'
          'The block "Hdf_saver" has been renamed to "Hdf_recorder".\n'
          'Please replace the name in your program, '
          'it will be removed in future versions\n'
          '#################')
    Hdf_recorder.__init__(self, *args, **kwargs)

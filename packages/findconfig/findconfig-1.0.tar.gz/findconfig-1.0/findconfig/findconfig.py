import xdg
import inspect
from pathlib import Path

def findconfig(filename, allow_dot=True, use_xdg=True, use_home=True,
                         use_src=True, more_paths = []):
  """
  Find a config file.

  :param filename: The filename to search for.
  :param allow_dot: Whether to allow a prepended dot to the filename.
  :param use_xdg: Whether to search in the XDG config directories.
  :param use_home: Whether to search in the user home directory.
  :param use_src: Whether to search in the source directory of the caller module.
  :param more_paths: A list of additional paths to search in.
  :return: The path to the file, or None if not found.
  """
  search_paths = []
  if use_xdg:
    search_paths.append(xdg.xdg_config_home())
    search_paths += xdg.xdg_config_dirs()
  if use_home:
    search_paths.append(Path.home())
  if use_src:
    stk = inspect.stack()
    if len(stk) > 1:
      srcdir = Path(stk[1].filename).parent
      while srcdir.joinpath('__init__.py').exists():
        search_paths.append(srcdir)
        srcdir = srcdir.parent
      search_paths.append(srcdir)
  search_paths += [Path(p) for p in more_paths]
  for path in search_paths:
    if path.is_dir():
      filenames = [path / filename]
      if allow_dot:
        filenames.append(path / f".{filename}")
      for f in filenames:
        if f.is_file():
          return f
  return None

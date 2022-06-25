import glob
import os
from collections import defaultdict, OrderedDict

import yaml

from constants import PROBLEM_PATHS, UTILITY_FILES, PARSONS_GLOB, PARSONS_FOLDER_PATH 

def load_config_file(paths):
  """
  Loads a YAML file.
  Args:
      paths: Either a single path or a list of paths for YAML files.

  Returns: The contents of the YAML file as a defaultdict, returning None
      for unspecified attributes.
  """
  if type(paths) != list:
    paths = [paths]
  for path in paths:
    try:
      with open(os.path.abspath(path), 'r') as file:
        config = yaml.load(file, Loader=yaml.Loader)
      if type(config) == dict:
        config = defaultdict(lambda: None, config)
      return config
    except IOError as e:
      pass
  raise Exception("Cannot find files {0}".format(paths))

def load_config(problem_name):
  """
  Loads a YAML file, assuming that the YAML file is located at {PROBLEM_PATHS}/{problem_name}.yaml
  Normalizes problem_name to lowercase as all filenames should be lowercased.
   
  Args:
      problem_name: The name of the problem.

  Returns: The contents of the YAML file as a defaultdict, returning None
      for unspecified attributes.
  """
  config_files = []
  for path in PROBLEM_PATHS:
    config_files.append(os.path.join(os.path.abspath(path), problem_name.lower() + ".yaml"))
  return load_config_file(config_files)

def problem_name_from_file(filename):
  with open(filename, "r", encoding="utf8") as f:
    cur_lines = f.readlines()
    for line in cur_lines:
        cur_words = line.lstrip().split()
        if cur_words and cur_words[0] == 'def':
            func_sig = cur_words[1]
            name = func_sig[:func_sig.index('(')]
            return name


def path_to_name(names_to_paths, path):
    for key, val in names_to_paths.items():
        if val == path:
            return key

import functools
import yaml

from hunter_pkg import flogging
from hunter_pkg import log_level


with open("hunter_pkg/config/stats.yaml") as file:
    _map = yaml.safe_load(file)

def get(path):
    keys = path.split(".")
    val = _map

    for i, key in enumerate(keys):
        try:
            val = val[key]

            if i >= len(keys) - 1:
                return val
        except KeyError:
            return None

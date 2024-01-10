from dataclasses import dataclass, field
from typing import List, Dict
import json

with open("config.json", "r") as configfile:
    Config = json.load(configfile)

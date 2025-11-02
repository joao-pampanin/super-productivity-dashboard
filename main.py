import pandas as pd
import json
from helper.get_projects import get_projects

path = 'file.json'

df = get_projects(path)
df

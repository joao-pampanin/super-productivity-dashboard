import pandas as pd
import json
from helper.get_projects import get_projects
from helper.get_finished_tasks import get_finished_tasks
from helper.get_simple_counters import get_simple_counters

path = 'file.json'

df = get_projects(path)
df

finished_df = get_finished_tasks(path)
finished_df.sample(1).T

simple_counters_df = get_simple_counters(path)
simple_counters_df.sample(1).T

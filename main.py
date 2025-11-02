import pandas as pd
import json
from helper.get_projects import get_projects
from helper.get_finished_tasks import get_finished_tasks

path = 'file.json'

df = get_projects(path)
df

finished_df = get_finished_tasks(path)
finished_df.sample(1).T

"""Helper function to extract simple counters (habit tracker) from a JSON file and return them as a pandas DataFrame."""

import json
from typing import Any, Dict

import pandas as pd


def get_simple_counters(path: str) -> pd.DataFrame:
    with open(path, 'r') as f:
        data = json.load(f)

    if not (isinstance(data, dict) and 'simpleCounter' in data):
        raise KeyError("No 'simpleCounter' key found in the root of the JSON file.")
    simple_counter = data['simpleCounter']
    if not (isinstance(simple_counter, dict) and 'entities' in simple_counter):
        raise KeyError("No 'entities' key found in 'simpleCounter' section of the JSON file.")
    entities = simple_counter['entities']
    if not isinstance(entities, dict):
        raise ValueError("'entities' is not a dictionary in the 'simpleCounter' section of the JSON file.")

    # Only keep relevant columns and explode countOnDay
    records = []
    for entity in entities.values():
        if not isinstance(entity, dict):
            raise ValueError("Each entity in 'entities' should be a dictionary.")
        base = {k: entity.get(k) for k in ['id', 'title', 'type']}
        count_on_day = entity.get('countOnDay', {})
        if isinstance(count_on_day, dict) and count_on_day:
            for day, count in count_on_day.items():
                rec = base.copy()
                rec['date'] = day
                rec['count'] = count
                records.append(rec)
        else:
            rec = base.copy()
            rec['date'] = None
            rec['count'] = None
            records.append(rec)

    df = pd.DataFrame(records)
    return df

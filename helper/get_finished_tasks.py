"""Helper function to extract finished tasks from a JSON file and return them as a pandas DataFrame."""

import json
import pandas as pd


def convert_milliseconds_to_timedelta(milliseconds: int) -> pd.Timedelta:
    """Convert milliseconds to a pandas Timedelta."""
    return pd.to_timedelta(milliseconds, unit='ms')


def convert_unix_timestamp_to_datetime(unix_timestamp: int) -> pd.Timestamp:
    """Convert a Unix timestamp (in milliseconds) to a pandas Timestamp."""
    return pd.to_datetime(unix_timestamp, unit='ms')


def convert_dict_milliseconds_to_timedelta(d: dict) -> dict:
    """Convert all values in a dict from milliseconds to pandas Timedelta."""
    if not isinstance(d, dict):
        return d
    return {k: convert_milliseconds_to_timedelta(v) for k, v in d.items()}


def extract_entities_from_archive(archive: dict) -> list:
    """Extract task entities from an archive section (archiveYoung or archiveOld)."""
    if not (isinstance(archive, dict) and 'task' in archive):
        return []
    task = archive['task']
    if not (isinstance(task, dict) and 'entities' in task):
        return []
    entities = task['entities']
    if not isinstance(entities, dict):
        return []
    rows = []
    for entity in entities.values():
        if isinstance(entity, dict):
            rows.append(entity)
    return rows


def process_task_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all conversions to the task DataFrame."""
    
    # Unix timestamp to datetime conversion
    for col in ['created', 'modified', 'doneOn']:
        if col in df.columns:
            df[col] = df[col].apply(convert_unix_timestamp_to_datetime)
    
    # Milliseconds to Timedelta conversion
    for col in ['timeSpent', 'timeEstimate']:
        if col in df.columns:
            df[col] = df[col].apply(convert_milliseconds_to_timedelta)
    
    # Convert dict of milliseconds to dict of Timedelta for timeSpentOnDay
    if 'timeSpentOnDay' in df.columns:
        df['timeSpentOnDay'] = df['timeSpentOnDay'].apply(convert_dict_milliseconds_to_timedelta)
    return df

def get_finished_tasks(path: str) -> pd.DataFrame:
    """Extract finished tasks from both archiveYoung and archiveOld sections of the JSON file."""
    with open(path, 'r') as f:
        data = json.load(f)

    all_rows = []
    for archive_key in ['archiveYoung', 'archiveOld']:
        archive = data.get(archive_key)
        if archive is not None:
            all_rows.extend(extract_entities_from_archive(archive))

    if not all_rows:
        raise ValueError("No finished tasks found in 'archiveYoung' or 'archiveOld' sections of the JSON file.")

    df = pd.DataFrame(all_rows)
    df = process_task_dataframe(df)
    return df

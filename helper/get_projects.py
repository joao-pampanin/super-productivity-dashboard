"""Helper function to extract project data from a Super Productivity JSON file."""

import json
import pandas as pd


def get_projects(path: str) -> pd.DataFrame:
	"""Extracts project data from a Super Productivity JSON file and returns it as a DataFrame.
	Args:
		path (str): Path to the Super Productivity JSON file.
	Returns:
		pd.DataFrame: DataFrame containing project entity IDs, titles, and archived status.
	"""

	with open(path, 'r') as f:
		data = json.load(f)

	rows = []
	if isinstance(data, dict) and 'project' in data:
		project = data['project']
		if isinstance(project, dict) and 'entities' in project:
			entities = project['entities']
			if isinstance(entities, dict):
				for entity_id, entity in entities.items():
					title = entity.get('title', None) if isinstance(entity, dict) else None
					is_archived = entity.get('isArchived', None) if isinstance(entity, dict) else None
					rows.append({'id': entity_id, 'title': title, 'isArchived': is_archived})
			else:
				raise ValueError("'entities' is not a dictionary in the 'project' section of the JSON file.")
		else:
			raise KeyError("No 'entities' key found in the 'project' section of the JSON file.")
	else:
		raise KeyError("No 'project' key found in the root of the JSON file.")

	df = pd.DataFrame(rows)
	return df

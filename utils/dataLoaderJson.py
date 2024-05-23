import json
from typing import Dict, Any


class DataLLoader:
    def __init__(self, pathJson: str) -> None:
        """Initialize DataLoader with the path to the JSON file."""
        self.pathJson = pathJson
        self.data = self.__openJson__()

    def __openJson__(self) -> dict:
        """Load JSON data from the specified file."""
        try:
            with open(self.pathJson) as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.pathJson}' not found")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file '{self.pathJson}'")

    def get_data(self) -> dict:
        """Return the loaded JSON data."""
        return self.data

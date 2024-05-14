import json
from typing import Dict, Any


class DataLLoader:
    def __init__(self,pathJson: str) -> None:
        """Initiliaze DataLoader with the path to the JSON file.

        Args:
            pathJson (str): paht to the json file
        """
        self.pathJson = pathJson
        self.data = self.__openJson__()

    def __openJson__(self)->Dict[str,Any]:
        """Load Json data from the specified file

        Returns:
            _type_: data json instance with the dat from json file
        """
        try:
            with open(self.pathJson) as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.path_json}' not fournd")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file '{self.pathJson}'.")
        
    
    def get_data(self)->Dict[str,Any]:
        """ Return the loaded JSON data.

        Returns:
            _type_: _description_
        """
        return self.data 
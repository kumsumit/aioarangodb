__all__ = ["Fields", "Headers", "Json", "Jsons", "Params"]

from typing import Any, Dict, List, Sequence, Union

Json = Dict[str, Any]
Jsons = List[Json]
Params = Dict[str, Union[bool, int, str]]
Headers = Dict[str, str]
Fields = Union[str, Sequence[str]]
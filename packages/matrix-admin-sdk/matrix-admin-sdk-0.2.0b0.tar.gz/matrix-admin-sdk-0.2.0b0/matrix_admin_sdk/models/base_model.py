from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

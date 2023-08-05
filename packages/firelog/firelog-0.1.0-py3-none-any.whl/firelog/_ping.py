from datetime import datetime
from typing import Optional, Dict, Any


class Ping:
    timestamp: datetime
    app: str
    params: Dict[str, Any]

    def __init__(self, app: str, view: str, timestamp: Optional[datetime] = None, **params):
        if timestamp is None:
            self.timestamp = datetime.now()
        self.app = app
        self.view = view
        self.params = params

    def to_json(self) -> Dict:
        return {
            "ts": self.timestamp.isoformat(),
            "params": self.params
        }
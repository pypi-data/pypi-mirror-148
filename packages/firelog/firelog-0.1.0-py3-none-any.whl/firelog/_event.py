from datetime import datetime
from typing import Optional, Dict, Any


class Event:
    timestamp: datetime
    app: str
    params: Dict[str, Any]

    def __init__(self, app: str, view: str, event_type: str, timestamp: Optional[datetime] = None, **params):
        if timestamp is None:
            self.timestamp = datetime.now()
        self.app = app
        self.view = view
        self.event_type = event_type
        self.params = params

    def to_json(self) -> Dict:
        return {
            "ts": self.timestamp.isoformat(),
            "type": self.event_type,
            "params": self.params
        }

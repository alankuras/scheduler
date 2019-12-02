from datetime import datetime, timedelta


class Campaign:
    def __init__(self, start: datetime, end: datetime, name="Campaign Name", patching_duration=120, server_limit=20):
        self.start = start
        self.end = end
        self.server_limit = server_limit
        self.name = name
        self.patching_duration = patching_duration
    
    @property
    def patching_duration(self):
        return self._patching_duration

    @patching_duration.setter
    def patching_duration(self, patching_duration):
        self._patching_duration = timedelta(minutes=patching_duration)

    def __repr__(self):
        return f"<Campaign name='{self.name}' start='{self.start}' end='{self.end}' patching_duration='{self.patching_duration}' server_limit='{self.server_limit}'>"

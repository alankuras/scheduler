from datetime import datetime


class Freeze:
    def __init__(self, begin: datetime, end: datetime):
        self.begin = begin
        self.end = end

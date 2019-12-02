from datetime import datetime, timedelta
from .server import Server, Env


class Slot:
    def __init__(self, datetime: datetime, freeze_period=False, size=20):
        """slot size - maximum number of servers to be patched in specific time slot 
        freeze_period - slot is placed during freeze period 
        """
        self.datetime = datetime
        self.timedelta = timedelta(
            hours=self.datetime.hour,
            minutes=self.datetime.minute
            )
        self.size = size
        self.servers = list()
        self.freeze_period = freeze_period

    def __repr__(self):
        return f"<Slot datetime='{str(self.datetime)}' freeze_period='{self.freeze_period}' size='{self.size}' left='{self.size - len(self.servers)}'"

    @property
    def not_full(self):
        return True if (self.size - len(self.servers) > 0) else False

    def append(self, server: Server) -> None:
        if len(self.servers) >= self.size:
            raise Exception("Slot is full")

        if not self._slot_time_in_server_maintenance_window(server):
            raise Exception("Slot out of server maintenance window")

        if self.freeze_period and server.env == Env.PROD: 
            raise Exception("Production server cannot be scheduled during freeze period")
        
        self.servers.append(server)

    def _slot_time_in_server_maintenance_window(self, server: Server) -> bool:
        window = server.maintenance_window.get(self.datetime.isoweekday()) 
        if window:
            if window.get('begin') <= self.timedelta <= window.get('end'):
                return True
        return False

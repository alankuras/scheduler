from datetime import timedelta
from .campaign import Campaign
from .freeze import Freeze
from .slot import Slot
from .server import Server, Env

class Schedule:
    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self._freezes = list()
        self._slots = self._create_slots()
        self.unassigned_servers = {env:[] for env in Env}

    @property
    def filled_slots(self) -> list:
        return [slot for slot in self._slots if slot.servers]

    @property
    def usable_slots(self) -> list:
        return [slot for slot in self._slots if slot.not_full]

    @property
    def all_slots(self) -> list:
        return [slot for slot in self._slots]

    def __repr__(self):
        return f"<Schedule max_servers='{len(self._slots) * self.campaign.server_limit}'>"

    def add_freeze(self, freeze: Freeze) -> None:
        self._freezes.append(freeze)
        self._slots = self._create_slots()

    def add_server(self, server: Server) -> None:
        self.unassigned_servers[server.env].append(server)

    def calculate(self) -> bool:
        for env in [Env.IT, Env.DEV, Env.QA, Env.PROD]:
            for server in self.unassigned_servers[env]:
                if self._server_assigned_to_slot(server):
                    self.unassigned_servers[env].remove(server)

        # return False if there are some servers left in unassigned_servers, True otherwise
        return False if sum(len(x) for x in self.unassigned_servers.values()) > 0 else True

    def _in_freeze_period(self, date):
        for freeze in self._freezes:
            if freeze.begin <= date <= freeze.end:
                return True
        return False

    """ creates Slots within campaign window
    to be filled by the Servers
    """
    def _create_slots(self) -> list:
        slot_time = self.campaign.start
        slots = list()
        
        while slot_time <= self.campaign.end - self.campaign.patching_duration:
            slots.append(
                Slot(
                    datetime=slot_time,
                    size=self.campaign.server_limit,
                    freeze_period=self._in_freeze_period(slot_time)
                )
            )
            slot_time += self.campaign.patching_duration
        return slots

    def _server_assigned_to_slot(self, server: Server) -> bool:
        for slot in self.usable_slots:
            try:
                slot.append(server)
                return True
            except Exception:
                continue
        # servers without proper slot goes to below list
        #self.unassigned_servers.append(server)
        return False
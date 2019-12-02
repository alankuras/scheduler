from enum import Enum, auto
from .maintenance import MaintenanceWindow


class Server:
    def __init__(self, hostname: str, app_code: str, env: str, tag: str = None, maintenance_window=None, **kwargs):
        self.hostname = hostname
        self.app_code = app_code
        self.env = env
        self.tag = tag
        self.maintenance_window = MaintenanceWindow(maintenance_window, self.env.name).maintenance_window

        # additional fields eg.id
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, env):
        self._env = Env(env)

    def __repr__(self):
        return f"<Server hostname='{self.hostname}' env='{self.env}' tag='{self.tag}' app_code='{self.app_code}'>"


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Env(AutoName):
    IT = auto()
    DEV = auto()
    QA = auto()
    PROD = auto()



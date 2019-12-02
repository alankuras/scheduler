from re import split
from datetime import timedelta

class MaintenanceWindow:
    def __init__(self, maintenance_window: str, env: str):
        self.env = env
        self.maintenance_window = maintenance_window

    def __repr__(self):
        return f"<Maintenance_window maintenance_window='{self.maintenance_window}'>"

    @property
    def maintenance_window(self):
        return self._maintenance_window

    @maintenance_window.setter
    def maintenance_window(self, maintenance_window):
        if maintenance_window is None:
            maintenance_window = self._set_default_maintenance_window()
        self._maintenance_window = self._parse_maintenance_window(maintenance_window)

    def _set_default_maintenance_window(self) -> str:
        default_maintenance_window = {
            "PROD": "Sat,00:00-23:59;Sun,00:00-23:59",
            "DEV": "Mon,00:00-23:59;Tue,00:00-23:59;Wed,00:00-23:59;Thu,00:00-23:59;Fri,00:00-23:59",
            "IT": "Mon,00:00-23:59;Tue,00:00-23:59;Wed,00:00-23:59;Thu,00:00-23:59;Fri,00:00-23:59",
            "QA": "Mon,00:00-23:59;Tue,00:00-23:59;Wed,00:00-23:59;Thu,00:00-23:59;Fri,00:00-23:59"
        }
        return default_maintenance_window.get(self.env)

    def _parse_maintenance_window(self, maintenance_window):
        window = dict()
        for entry in maintenance_window.split(";"):
            day = entry.split(",")[0]
            hour_begin = entry.split(",")[1].split("-")[0]
            hour_end = entry.split(",")[1].split("-")[1]
            window.update({
                self._weekday_to_isoweekday(day): {
                    'begin': timedelta(
                        hours=int(hour_begin.split(":")[0]),
                        minutes=int(hour_begin.split(":")[1])
                    ),
                    'end': timedelta(
                        hours=int(hour_end.split(":")[0]),
                        minutes=int(hour_end.split(":")[1])
                    )
                } 
            })
        return window
    
    @staticmethod
    def _weekday_to_isoweekday(day: str) -> int:
        weekday_map = {
            'Mon': 1,
            'Tue': 2,
            'Wed': 3,
            'Thu': 4,
            'Fri': 5,
            'Sat': 6,
            'Sun': 7
        }
        return weekday_map.get(day) 

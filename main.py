from datetime import datetime
from scheduler.server import Server
from scheduler.schedule import Schedule
from scheduler.campaign import Campaign
from scheduler.freeze import Freeze

campaign = Campaign(
    start=datetime.strptime('01/01/20 07:00', '%d/%m/%y %H:%M'),
    end=datetime.strptime('14/01/20 22:00', '%d/%m/%y %H:%M')
    )
campaign.patching_duration = 120
campaign.server_limit = 10

schedule = Schedule(campaign=campaign)

freeze_first = Freeze(
    begin=datetime.strptime('02/01/20 00:00', '%d/%m/%y %H:%M'),
    end=datetime.strptime('03/01/20 23:59', '%d/%m/%y %H:%M')
    )

freeze_second = Freeze(
    begin=datetime.strptime('01/01/20 09:00', '%d/%m/%y %H:%M'),
    end=datetime.strptime('09/01/20 23:59', '%d/%m/%y %H:%M')
    )

schedule.add_freeze(freeze_first)
schedule.add_freeze(freeze_second)

server = Server(
        hostname="hostname",
        app_code="ABC",
        env="PROD"
)


print(campaign)
print(schedule)
print(server)
print(server.maintenance_window)
print(schedule.add_server(server))
print(schedule.calculate())
print(schedule.filled_slots)

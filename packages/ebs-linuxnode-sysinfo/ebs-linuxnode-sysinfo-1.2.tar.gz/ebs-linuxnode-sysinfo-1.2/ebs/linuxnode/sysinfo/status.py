

import psutil
import time
from .temperature import TemperatureInfo
from .disks import DiskInfo
from .memory import MemoryInfo
from .display import DisplayInfo
from .base import SysInfoBase


class StatusInfo(SysInfoBase):
    def __init__(self, *args):
        super(StatusInfo, self).__init__(*args)

    def install(self):
        super(StatusInfo, self).install()
        temperature = TemperatureInfo(self.actual)
        temperature.install()
        disks = DiskInfo(self.actual)
        disks.install()
        memory = MemoryInfo(self.actual)
        memory.install()
        display = DisplayInfo(self.actual)
        display.install()
        self._items = {
            'uptime': self._uptime,
            'disks': disks,
            'memory': memory,
            'display': display,
            'temperature': temperature,
        }

    def _uptime(self):
        return time.time() - psutil.boot_time()

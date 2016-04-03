# coding: utf-8
from __future__ import unicode_literals, print_function
import subprocess

from .base import VolumeController


class OSXVolumeController(VolumeController):
    '''VolumeController implementation for Mac OS X platform'''

    def __init__(self):
        super(OSXVolumeController, self).__init__()

    def __osa(self, ascript):
        osap = subprocess.Popen(
            ['osascript', '-e', ascript, ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = osap.communicate()
        if stderr:
            raise RuntimeError('osascript returned error: {}'.format(stderr))
        return stdout.strip()

    def get_volume(self, channel='output'):
        if channel not in self.get_volume_channels():
            raise KeyError('No such channel: {}'.format(channel))
        return float(
            self.__osa('{} volume of (get volume settings)'.format(channel))
        )

    def set_volume(self, value, channel='output'):
        if channel not in self.get_volume_channels():
            raise KeyError('No such channel: {}'.format(channel))
        min_volume, max_volume = self.get_volume_range(channel)
        if not min_volume <= value <= max_volume:
            raise ValueError(
                'Value not in range: {:.1f} - {:.1f}'.format(
                    min_volume, max_volume
                )
            )
        self.__osa('set volume {} volume {}'.format(channel, value))

    def get_volume_range(self, channel='output'):
        return (0, 100, )

    def get_volume_step(self, channel='output'):
        # Mac will take your value as is when you set volume,
        # but the actually volume will be rounded, that's said,
        # setting to 5.49 result in 5 and setting to 5.51 result in 6
        return 1

    def get_volume_channels(self):
        return ('output', 'input', 'alert', )

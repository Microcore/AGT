# coding: utf-8
from __future__ import unicode_literals, print_function

from pulsectl import Pulse

from .base import VolumeController


class LinuxVolumeController(VolumeController):
    '''Linux (PulseAudio) implementation of VolumeController'''

    def __init__(self):
        super(LinuxVolumeController, self).__init__()
        self.__pulse = Pulse()

    def __get_sink_by_name(self, name):
        '''Get actual PulseAudio sink (device?) by name'''
        for sink in self.__pulse.sink_list():
            if sink.name == name:
                return sink
        raise KeyError('No such device: {}'.format(name))

    def get_volume(self, channel=None):
        available_channels = self.get_volume_channels()
        channel = channel or available_channels[0]
        if channel not in available_channels:
            raise KeyError('No such channel: {}'.format(channel))
        return self.__pulse.volume_get_all_chans(
            self.__get_sink_by_name(channel)
        ) * 100.0

    def set_volume(self, value, channel=None):
        available_channels = self.get_volume_channels()
        channel = channel or available_channels[0]
        if channel not in available_channels:
            raise KeyError('No such channel: {}'.format(channel))
        self.__pulse.volume_set_all_chans(
            self.__get_sink_by_name(channel),
            value / 100.0
        )

    def get_volume_range(self, channel=None):
        return (0, 100, )

    def get_voilume_step(self, channel=None):
        return 1

    def get_volume_channels(self):
        return tuple([c.name for c in self.__pulse.sink_list()])

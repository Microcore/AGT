# coding: utf-8
from __future__ import unicode_literals, print_function


class VolumeController(object):
    '''Base abstract class'''
    def __init__(self):
        super(VolumeController, self).__init__()

    def get_volume(self, channel='output'):
        '''Get volume of specific channel'''
        raise NotImplementedError('Should be implemented in subclass')

    def set_volume(self, value, channel='output'):
        '''Set volume of specific channel'''
        raise NotImplementedError('Should be implemented in subclass')

    def get_volume_range(self, channel='output'):
        '''
        Get volume range of specific channel
        Returns (min, max, )
        '''
        raise NotImplementedError('Should be implemented in subclass')

    def get_volume_step(self, channel='output'):
        '''Get minimal step of specific channel'''
        raise NotImplementedError('Should be implemented in subclass')

    def get_volume_channels(self):
        '''
        Get all available volume channels
        Returns tuple of strings
        '''
        raise NotImplementedError('Should be implemented in subclass')

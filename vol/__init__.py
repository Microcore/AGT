# coding: utf-8
'''
A cross platform implementation of volume control
'''
from __future__ import unicode_literals, print_function
from sys import platform

if platform == 'darwin':
    from .osx import OSXVolumeController as VolumeController
elif platform == 'win32':
    from .win32 import Win32VolumeController as VolumeController
else:
    raise NotImplementedError(
        'VolumeController for {} platform has not been implemented yet'.format(platform)
    )

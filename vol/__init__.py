# coding: utf-8
from __future__ import unicode_literals, print_function
from sys import platform

if platform == 'darwin':
    from .osx import OSXVolumeController as VolumeController
else:
    raise NotImplementedError(
        'VolumeController for {} platform has not been implemented yet'.format(platform)
    )

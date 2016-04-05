# coding: utf-8
# Code excerpted from http://blog.sina.com.cn/s/blog_4513dde60101lt0a.html
# Original author info
# 2012.12.14 PM 10:08
# python 2.7.1
# xialulee
# Modified by Joker Qyou
from __future__ import unicode_literals, print_function

from comtypes import *

from .base import VolumeController


class IAudioEndpointVolume(IUnknown):
    _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'RegisterControlChangeNotify',
                  (['in'], c_voidp, 'pNotify')
                  ),
        COMMETHOD([], HRESULT, 'UnregisterControlChangeNotify',
                  (['in'], c_voidp, 'pNotify')
                  ),
        COMMETHOD([], HRESULT, 'GetChannelCount',
                  (['out'], POINTER(c_uint), 'pnChannelCount')
                  ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                  (['in'], c_float, 'fLevel'),
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                  (['out'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                  (['out'], POINTER(c_float), 'pfLevel')
                  ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                  (['in'], c_uint, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                  (['in'], c_uint, 'nChannel'),
                  (['in'], c_float, 'fLevel'),
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                  (['in'], c_uint, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevelDB')
                  ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                  (['in'], c_uint, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevel')
                  ),
        COMMETHOD([], HRESULT, 'SetMute',
                  (['in'], c_int, 'bMute'),
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'GetMute',
                  (['out'], POINTER(c_bool), 'pbMute')
                  ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                  (['out'], POINTER(c_uint), 'pnStep'),
                  (['out'], POINTER(c_uint), 'pnStepCount')
                  ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
                  (['in'], c_voidp, 'pguidEventContext')
                  ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                  (['out'], POINTER(c_uint), 'pdwHardwareSupportMask')
                  ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
                  (['out'], POINTER(c_float), 'pflVolumeMindB'),
                  (['out'], POINTER(c_float), 'pflVolumeMaxdB'),
                  (['out'], POINTER(c_float), 'pflVolumeIncrementdB')
                  )
    ]


class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
                  (['in'], POINTER(GUID), 'iid'),
                  (['in'], c_uint, 'dwClsCtx'),
                  (['in'], c_voidp, 'pActivationParams'),
                  (['out'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
                  ),
        COMMETHOD([], HRESULT, 'OpenPropertyStore',
                  (['in'], c_int32, 'stgmAccess'),
                  (['out'], c_voidp, 'ppProperties')
                  ),
        COMMETHOD([], HRESULT, 'GetId',
                  (['out'], c_voidp, 'ppstrId')
                  ),
        COMMETHOD([], HRESULT, 'GetState',
                  (['out'], POINTER(c_uint), 'pdwState')
                  )
    ]


class IMMDeviceEnumerator(IUnknown):
    _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                  (['in'], c_int, 'dataFlow'),
                  (['in'], c_int, 'dwStateMask'),
                  (['out'], POINTER(c_voidp), 'ppDevices')
                  ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                  (['in'], c_int, 'dataFlow'),
                  (['in'], c_int, 'role'),
                  (['out'], POINTER(POINTER(IMMDevice)))
                  ),
        COMMETHOD([], HRESULT, 'GetDevice',
                  (['in'], c_voidp, 'pwstrId'),
                  (['out'], POINTER(POINTER(IMMDevice)))
                  ),
        COMMETHOD([], HRESULT, 'RegisterEndpointNotificationCallback',
                  (['in'], c_voidp)
                  ),
        COMMETHOD([], HRESULT, 'UnregisterEndpointNotificationCallback',
                  (['in'], c_voidp)
                  )
    ]


class Win32VolumeController(VolumeController):
    '''VolumeController implementation for Win32 platform'''

    def __init__(self):
        super(Win32VolumeController, self).__init__()

        clsid = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
        pMde = CoCreateInstance(clsid, interface=IMMDeviceEnumerator)

        EDataFlow_eRender = 0
        ERole_eConsole = 0

        pDevice = pMde.GetDefaultAudioEndpoint(
            EDataFlow_eRender, ERole_eConsole)

        CLSCTX_ALL = 0x17

        iid = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
        self.__pEndPoint = pDevice.Activate(byref(iid), CLSCTX_ALL, None)
        # By step:
        # self.__pEndPoint.VolumeStepUp(None)
        # self.__pEndPoint.VolumeStepDown(None)

    def get_volume(self, channel='master'):
        if channel not in self.get_volume_channels():
            raise KeyError('No such channel: {}'.format(channel))
        return self.__pEndPoint.GetMasterVolumeLevelScalar() * 100.0

    def set_volume(self, value, channel='master'):
        if channel not in self.get_volume_channels():
            raise KeyError('No such channel: {}'.format(channel))
        min_volume, max_volume = self.get_volume_range(channel)
        if not min_volume <= value <= max_volume:
            raise ValueError(
                'Value not in range: {:.1f} - {:.1f}'.format(
                    min_volume, max_volume
                )
            )
        self.__pEndPoint.SetMasterVolumeLevelScalar(value / 100.0, None)

    def get_volume_range(self, channel='master'):
        return (0, 100, )

    def get_volume_step(self, channel='master'):
        # Windows actually takes volume as float, if you
        # set it to 10, you'll get it as 9.9999
        # The Windows mixer rounds it when displaying on UI,
        # so deal with that yourself.
        return 1

    def get_volume_channels(self):
        # TODO Maybe we should query and return all sessions here?
        return ('master', )

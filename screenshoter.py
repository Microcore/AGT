# -*- coding: utf-8 -*-

from datetime import datetime
import logging
from multiprocessing import Process
import os
import sys
import time

from PIL import ImageGrab
import wx


__path__ = os.path.abspath(os.path.dirname(__file__))

class ScreenshoterApp(wx.App):

    def __init__(self, save_path):
        # Perform arg2attr procedure before super class init, 
        # cause the other way an AttributeError will occur. 
        self.save_path = save_path
        super(ScreenshoterApp, self).__init__(False, None)

    def OnInit(self):
        self.MAINFRAME = HotkeyFrame()
        self.sound = wx.Sound(os.path.join(__path__, 'shutter.wav'))
        # Always return true
        return True

    def __del__(self):
        del self.save_path
        del self.sound

class HotkeyFrame(wx.Frame):
    '''
    An invisible frame (window) for hotkey listening. 
    '''
    def __init__(self):
        super(HotkeyFrame, self).__init__(parent=None, 
                                          id=wx.ID_ANY, 
                                          pos=(10, 10), 
                                          size=(10, 10))
        self.SetTransparent(0)
        self.Show(False)
        self.wholeScreenHotkeyId = 100
        self.selectScreenHotkeyId = 101
        self.regHotkeys()

    def regHotkeys(self):
        '''
        Register hot keys. 
        '''
        # Ctrl + Alt + Z for fullscreen capture
        self.RegisterHotKey(self.wholeScreenHotkeyId, 
                            wx.MOD_ALT | wx.MOD_CONTROL, 
                            ord('Z'))
        self.Bind(wx.EVT_HOTKEY, 
                  self.handleHotKey, 
                  id=self.wholeScreenHotkeyId)

        # Ctrl + Alt + A for selection capture
        self.RegisterHotKey(self.selectScreenHotkeyId, 
                            wx.MOD_ALT | wx.MOD_CONTROL, 
                            ord('A'))
        self.Bind(wx.EVT_HOTKEY, 
                  self.handleHotKey, 
                  id=self.selectScreenHotkeyId)

    def handleHotKey(self, evt):
        '''
        Handle registered hotkey events. 
        '''
        screenshot = ImageGrab.grab()
        if evt.Id == self.selectScreenHotkeyId:
            try:
                wx.GetApp().SELECTFRAME.close()
            except Exception, e:
                pass
            wx.GetApp().SELECTFRAME = SelectFrame(img=screenshot)
        elif evt.Id == self.wholeScreenHotkeyId:
            filename = datetime.strftime(datetime.now(), '%Y.%m.%d.%H-%M-%S.%f')
            filename = 'Screenshot.%s.png' % filename
            wx.GetApp().sound.Play(wx.SOUND_ASYNC)

            screenshot.save(os.path.join(wx.GetApp().save_path, filename))

    def __del__(self):
        del self.wholeScreenHotkeyId
        del self.selectScreenHotkeyId

class SelectFrame(wx.Frame):
    '''
    Capture selected area. 
    '''
    def __init__(self, img):
        super(SelectFrame, self).__init__(parent=None, 
                                          id=wx.ID_ANY, 
                                          pos=(0, 0))
        self.img = img
        # self.SetTransparent(255)
        self.selection = [0, 0, 0, 0]

        # Convert PIL image to wx bitmap for display
        wxImage = wx.EmptyImage(*self.img.size)
        wxImage.SetData(self.img.convert('RGB').tostring())
        self.bitmap = wxImage.ConvertToBitmap()
        self.IMAGECTRL = wx.StaticBitmap(self, wx.ID_ANY, self.bitmap)

        # Bind event handlers
        self.IMAGECTRL.Bind(wx.EVT_MOTION, self.handleMouseMove)
        self.IMAGECTRL.Bind(wx.EVT_LEFT_DOWN, self.handleMouseDown)
        self.IMAGECTRL.Bind(wx.EVT_LEFT_UP, self.handleMouseUp)
        self.IMAGECTRL.Bind(wx.EVT_PAINT, self.handlePaint)

        self.Bind(wx.EVT_KEY_DOWN, self.saveScreenshot)

        self.ShowFullScreen(True)
        self.Raise()
        self.SetFocus()
        # self.RequestUserAttention()

    def handleMouseMove(self, evt):
        '''
        Handle mouse move event. 
        Will do:
            update borders of selected area if mouse left key is being hold; 
            refresh the borders displayed if mouse left key is being hold; 
        '''
        if evt.LeftIsDown():
            self.selection[2], self.selection[3] = evt.GetX(), evt.GetY()
            self.IMAGECTRL.Refresh()

    def handleMouseDown(self, evt):
        '''
        Handle mouse left key down event. 
        Will do:
            update the first point coordinates on mouse left key down. 
        '''
        self.selection[0], self.selection[1] = evt.GetX(), evt.GetY()

    def handleMouseUp(self, evt):
        '''
        Handle mouse left key up event. 
        Will do:
            update the second point coordinates on mouse left key up. 
        '''
        self.selection[2], self.selection[3] = evt.GetX(), evt.GetY()

    def handlePaint(self, evt):
        '''
        Handle bitmap paint event. 
        Will do:
            Repaint the screenshot selection. 
        '''
        if self.selection[2] - self.selection[0] != 0 \
        and self.selection[3] - self.selection[1] != 0:
            dc = wx.PaintDC(self.IMAGECTRL)
            # Dont clear the graphic context, cause if you do that
            # too often, the screen will flash very hard
            # dc.Clear()

            # Overlay the saved fullscreen bitmap
            dc.DrawBitmap(self.bitmap, 0, 0)
            # Draw borders of selected area
            dc.SetPen(wx.Pen(wx.RED, 1))
            # --->
            dc.DrawLine(self.selection[0], 
                        self.selection[1], 
                        self.selection[2], 
                        self.selection[1])
            # |
            # |
            # Y
            dc.DrawLine(self.selection[2], 
                        self.selection[1], 
                        self.selection[2], 
                        self.selection[3])
            # <---
            dc.DrawLine(self.selection[2], 
                        self.selection[3], 
                        self.selection[0], 
                        self.selection[3])
            # A
            # |
            # |
            dc.DrawLine(self.selection[0], 
                        self.selection[3], 
                        self.selection[0], 
                        self.selection[1])

    def saveScreenshot(self, evt):
        '''
        Save selected area of the whole screenshot to file. 
        '''
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.close()
        if evt.GetKeyCode() != wx.WXK_RETURN:
            return
        x1, y1, x2, y2 = self.selection
        if x1 - x2 == 0 or y1 - y2 == 0:
            return

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        selected_area = self.img.crop(box=(x1, y1, x2, y2))
        filename = datetime.strftime(datetime.now(), '%Y.%m.%d.%H-%M-%S.%f')
        filename = 'Screenshot.%s.png' % filename
        wx.GetApp().sound.Play(wx.SOUND_ASYNC)

        selected_area.save(os.path.join(wx.GetApp().save_path, filename))
        self.close()

    def close(self):
        wx.GetApp().SELECTFRAME = None
        self.Destroy()

    def __del__(self):
        del self.img
        del self.bitmap
        del self.selection
        del self.IMAGECTRL
        

def main(save_path):
    app = ScreenshoterApp(save_path)
    sys.exit(app.MainLoop())

if __name__ == '__main__':
    main('D:\\')

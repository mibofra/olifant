#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sat Mar 31 15:44:43 2012

import wx
import os
import sys
from olifant import Olifant
from olifantException import OlifantException

# begin wxGlade: extracode
# end wxGlade

def showError(label,text):
	dial = wx.MessageDialog(None, text , label , wx.ICON_ERROR)
        dial.ShowModal()

class MyFrame(wx.Frame):

    olifant = None #olifant

    def __init__(self, *args, **kwds):

        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.bitmap_1 = wx.StaticBitmap(self, -1, wx.Bitmap("./images/icon.png", wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.label_5 = wx.StaticText(self, -1, "Select monitoring mode:", style=wx.ALIGN_CENTRE)
        self.combo_box_1 = wx.ComboBox(self, -1, choices=["Password mode", "USB mode", "Strong mode"], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
        self.Lock = wx.Button(self, -1, "Lock")
        self.checkbox_1 = wx.CheckBox(self, -1, "AC Cable")
        self.checkbox_2 = wx.CheckBox(self, -1, "Power button")
        self.checkbox_3 = wx.CheckBox(self, -1, "Battery")
        self.label_6 = wx.StaticText(self, -1, "About Olifant", style=wx.ALIGN_RIGHT)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Olifant")
        self.SetSize((436, 316))
        self.SetFocus()
        self.bitmap_1.SetMinSize((16, 16))
        self.label_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.combo_box_1.SetSelection(0)
        self.label_6.SetForegroundColour(wx.Colour(10, 64, 255))
        self.label_6.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 1, ""))
        # end wxGlade

	self.combo_box_1.SetEditable(False)
	self.checkbox_1.SetValue(True)
	self.checkbox_2.SetValue(True)
	self.checkbox_3.SetValue(True)
	self.Bind(wx.EVT_BUTTON, self.OnLockClick, self.Lock)

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 3, 0, 0)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_1.Add(self.bitmap_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1.Add((400, 20), 0, 0, 0)
        sizer_1.Add(self.label_5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_1.Add(self.combo_box_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_1.Add(self.Lock, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.checkbox_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        grid_sizer_1.Add(self.checkbox_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        grid_sizer_1.Add(self.checkbox_3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_1.Add(self.label_6, 0, wx.ALL|wx.ALIGN_RIGHT, 6)
        self.SetSizer(sizer_1)
        sizer_1.SetSizeHints(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    
    def OnLockClick(self, event):
	alarms = []
	if self.checkbox_1.IsChecked():
		alarms.append(Olifant.AC_ALARM)
	if self.checkbox_2.IsChecked():
		alarms.append(Olifant.POWER_BUTTON_ALARM)
	if self.checkbox_3.IsChecked():
		alarms.append(Olifant.BATTERY_ALARM)

	if len(alarms) == 0:
		showError('Warning','You have all 3 options disabled, are you sure?')

	choice = self.combo_box_1.GetCurrentSelection()
	try:
		if choice == 0:
			self.olifant = Olifant(Olifant.PASSWD_MODE, alarms)
		elif choice == 1:
			self.olifant = Olifant(Olifant.USB_MODE, alarms)
		elif choice == 2:
			self.olifant = Olifant(Olifant.STRONG_MODE, alarms)
		else:
			showError('Wrong Selection','Olifant option unknown')
	
		if choice == 0:
        		passdlg = MyDialog1(self, -1,MyDialog1.ACTIVATE_MODE)
			passdlg.clearAll() #TODO we need this because of a bug
			passdlg.ShowModal()
			pwd = passdlg.getPasswd()

			if pwd == '':
				showError('Error!','password cannot be empty')
			else:
				try:
					self.olifant.lock(pwd)
					FlagList = ['FULLSCREEN_NOMENUBAR',
  						     'FULLSCREEN_NOTOOLBAR',
  				                     'FULLSCREEN_NOSTATUSBAR',
  				                     'FULLSCREEN_NOBORDER',
  				                     'FULLSCREEN_NOCAPTION',
  				                     'FULLSCREEN_ALL']
					self.ShowFullScreen(True,FlagList)
					activedlg = MyDialog(self,-1)
					activedlg.setOlifant(self.olifant)
					activedlg.setParentFrame(self)
					activedlg.ShowModal()
				except OlifantException as ex:
					showError('Olifant exception',ex.getMessage())
		else:
			showError('Error','Not supported yet')

	except OlifantException as ex:
		showError('Olifant exception',ex.getMessage())

# end of class MyFrame

"""
useless one!!
"""
class MyDialog2(wx.Dialog):

    passwd = []

    def getPasswd(self):
	''.join(self.passwd)

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog2.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.choose_pswd = wx.StaticText(self, -1, "Choose password", style=wx.ALIGN_CENTRE)
        self.pass1 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.confirm_pswd = wx.StaticText(self, -1, "Confirm password", style=wx.ALIGN_CENTRE)
        self.pass2 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.button_1 = wx.Button(self, -1, "1")
        self.button_2 = wx.Button(self, -1, "2")
        self.button_3 = wx.Button(self, -1, "3")
        self.button_4 = wx.Button(self, -1, "4")
        self.button_5 = wx.Button(self, -1, "5")
        self.button_6 = wx.Button(self, -1, "6")
        self.button_7 = wx.Button(self, -1, "7")
        self.button_8 = wx.Button(self, -1, "8")
        self.button_9 = wx.Button(self, -1, "9")
        self.button_DEL = wx.Button(self, -1, "DEL")
        self.button_0 = wx.Button(self, -1, "0")
        self.button_OK = wx.Button(self, -1, "OK")
        self.activate = wx.Button(self, -1, "Activate alarm")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog2.__set_properties
        self.SetTitle("dialog_3")
        self.SetSize((300, 370))
        self.choose_pswd.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.pass1.SetMinSize((150, 30))
        self.confirm_pswd.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.pass2.SetMinSize((150, 30))
        self.button_1.SetMinSize((50, 50))
        self.button_2.SetMinSize((50, 50))
        self.button_3.SetMinSize((50, 50))
        self.button_4.SetMinSize((50, 50))
        self.button_5.SetMinSize((50, 50))
        self.button_6.SetMinSize((50, 50))
        self.button_7.SetMinSize((50, 50))
        self.button_8.SetMinSize((50, 50))
        self.button_9.SetMinSize((50, 50))
        self.button_DEL.SetMinSize((50, 50))
        self.button_0.SetMinSize((50, 50))
        self.button_OK.SetMinSize((50, 50))
        # end wxGlade

	#self.choose_pswd.SetEditable(False)

    def __do_layout(self):
        # begin wxGlade: MyDialog2.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_4 = wx.GridSizer(2, 3, 0, 0)
        grid_3 = wx.GridSizer(2, 3, 0, 0)
        grid_2 = wx.GridSizer(1, 3, 0, 0)
        grid_1 = wx.GridSizer(1, 3, 0, 0)
        sizer_2.Add(self.choose_pswd, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_2.Add(self.pass1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 6)
        sizer_2.Add(self.confirm_pswd, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.pass2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 6)
        grid_1.Add(self.button_1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_1.Add(self.button_2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_1.Add(self.button_3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(grid_1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_2.Add(self.button_4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_2.Add(self.button_5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_2.Add(self.button_6, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(grid_2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_3.Add(self.button_7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_3.Add(self.button_8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_3.Add(self.button_9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(grid_3, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_4.Add(self.button_DEL, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_4.Add(self.button_0, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_4.Add(self.button_OK, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add(grid_4, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_2.Add(self.activate, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.SetSizer(sizer_2)
        self.Layout()
        # end wxGlade

    def __onKeyPress(self):
	print "pressed"

    """
    def OnAlarmClick(self, event, ol):
	passvalue_1 = self.pass1.GetValue()
	passvalue_2 = self.pass2.GetValue()
	if  passvalue_1 == passvalue_2:
		try:
			olifant.lock(passvalue_1)
			almdlg = MyDialog(self, -1)
			almdlg.Lock_copy.Bind(EVT_BUTTON, almdlg.OnClick, olifant, passvalue1)
			almdlg.Destroy()
		except OlifantException as ex:
			print ex.getMessage() #TODO far comparire box di errore
	else:			
		print "Le password sono diverse." #TODO far comparire dialog box di errore
     """
# end of class MyDialog2


class MyPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.bitmap_1_copy = wx.StaticBitmap(self, -1, wx.Bitmap("images/icon.png", wx.BITMAP_TYPE_ANY))
        self.label_1_copy = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.label_7 = wx.StaticText(self, -1, "https://launchpad.net/olifant", style=wx.ALIGN_CENTRE)
        self.label_8 = wx.StaticText(self, -1, "author")
        self.label_10_copy = wx.StaticText(self, -1, "kokito\n(jumba@LP)", style=wx.ALIGN_CENTRE)
        self.label_9 = wx.StaticText(self, -1, "Actual developers")
        self.label_10 = wx.StaticText(self, -1, "Cristian_C\nSquall867")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyPanel.__set_properties
        self.SetSize((310, 310))
        self.bitmap_1_copy.SetMinSize((64, 64))
        self.label_1_copy.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_7.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_8.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.label_9.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.bitmap_1_copy, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        sizer_3.Add(self.label_1_copy, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        sizer_3.Add(self.label_7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        sizer_3.Add(self.label_8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        sizer_3.Add(self.label_10_copy, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        sizer_3.Add(self.label_9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        sizer_3.Add(self.label_10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        self.SetSizer(sizer_3)
        # end wxGlade

# end of class MyPanel


class MyDialog(wx.Dialog):

    olifant = None
    parentFrame = None

    def __init__(self,*args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.bitmap_1_copy_copy = wx.StaticBitmap(self, -1, wx.Bitmap("images/icon.png", wx.BITMAP_TYPE_ANY))
        self.label_1_copy_copy = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.label_4 = wx.StaticText(self, -1, "ALARM ACTIVATED", style=wx.ALIGN_CENTRE)
        self.Lock_copy = wx.Button(self, -1, "Unlock")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("dialog_1")
        self.bitmap_1_copy_copy.SetMinSize((64, 64))
        self.label_1_copy_copy.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_4.SetForegroundColour(wx.Colour(255, 0, 0))
        self.label_4.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade
	self.Lock_copy.Bind(wx.EVT_BUTTON,self.OnUnlockClick)

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_1_copy.Add((400, 30), 0, 0, 0)
        sizer_1_copy.Add(self.bitmap_1_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1_copy.Add(self.label_1_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1_copy.Add(self.label_4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 26)
        sizer_1_copy.Add((400, 30), 0, 0, 0)
        sizer_1_copy.Add(self.Lock_copy, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_1_copy.Add((400, 30), 0, 0, 0)
        self.SetSizer(sizer_1_copy)
        sizer_1_copy.Fit(self)
        self.Layout()
        # end wxGlade

    def setOlifant(self,olifant):
	self.olifant = olifant

    def setParentFrame(self,frame):
	self.parentFrame = frame

    def OnUnlockClick(self,evt):
        passdlg = MyDialog1(self, -1,MyDialog1.DEACTIVATE_MODE)
	passdlg.clearAll() #TODO we need this because of a bug
	passdlg.ShowModal()
	try:
		self.olifant.unlock(passdlg.getPasswd())
                self.parentFrame.ShowFullScreen(False)
		self.Close()
	except OlifantException as ex:
		showError('Olifant Exception',ex.getMessage())
	

# end of class MyDialog


class MyDialog1(wx.Dialog):
    ACTIVATE_MODE = '0'
    DEACTIVATE_MODE = '1'

    passwd = []

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog1.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.Password = wx.StaticText(self, -1, "Password", style=wx.ALIGN_CENTRE)
        self.pswd = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.button_1_u = wx.Button(self, -1, "1")
        self.button_2_u = wx.Button(self, -1, "2")
        self.button_3_u = wx.Button(self, -1, "3")
        self.button_4_u = wx.Button(self, -1, "4")
        self.button_5_u = wx.Button(self, -1, "5")
        self.button_6_u = wx.Button(self, -1, "6")
        self.button_7_u = wx.Button(self, -1, "7")
        self.button_8_u = wx.Button(self, -1, "8")
        self.button_9_u = wx.Button(self, -1, "9")
        self.button_DEL_u = wx.Button(self, -1, "DEL")
        self.button_0_u = wx.Button(self, -1, "0")
        self.button_OK_u = wx.Button(self, -1, "OK")

	if args[2] == MyDialog1.ACTIVATE_MODE:
		self.Unlock = wx.Button(self, -1, "Activate alarm")
	else:
        	self.Unlock = wx.Button(self, -1, "Deactivate alarm")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog1.__set_properties
        self.SetTitle("dialog_2")
        self.SetSize((300, 321))
        self.Password.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.pswd.SetMinSize((150, 30))
        self.button_1_u.SetMinSize((50, 50))
        self.button_2_u.SetMinSize((50, 50))
        self.button_3_u.SetMinSize((50, 50))
        self.button_4_u.SetMinSize((50, 50))
        self.button_5_u.SetMinSize((50, 50))
        self.button_6_u.SetMinSize((50, 50))
        self.button_7_u.SetMinSize((50, 50))
        self.button_8_u.SetMinSize((50, 50))
        self.button_9_u.SetMinSize((50, 50))
        self.button_DEL_u.SetMinSize((50, 50))
        self.button_0_u.SetMinSize((50, 50))
        self.button_OK_u.SetMinSize((50, 50))
        # end wxGlade

	self.pswd.SetEditable(False)
        self.button_1_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_2_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_3_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_4_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_5_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_6_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_7_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_8_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_9_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_0_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_DEL_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.button_OK_u.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)


    def __do_layout(self):
        # begin wxGlade: MyDialog1.__do_layout
        sizer_2_u = wx.BoxSizer(wx.VERTICAL)
        grid_4_u = wx.GridSizer(2, 3, 0, 0)
        grid_3_u = wx.GridSizer(2, 3, 0, 0)
        grid_2_u = wx.GridSizer(1, 3, 0, 0)
        grid_1_u = wx.GridSizer(1, 3, 0, 0)
        sizer_2_u.Add(self.Password, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer_2_u.Add(self.pswd, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 6)
        grid_1_u.Add(self.button_1_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_1_u.Add(self.button_2_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_1_u.Add(self.button_3_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2_u.Add(grid_1_u, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_2_u.Add(self.button_4_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_2_u.Add(self.button_5_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_2_u.Add(self.button_6_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2_u.Add(grid_2_u, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_3_u.Add(self.button_7_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_3_u.Add(self.button_8_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_3_u.Add(self.button_9_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2_u.Add(grid_3_u, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        grid_4_u.Add(self.button_DEL_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_4_u.Add(self.button_0_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_4_u.Add(self.button_OK_u, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2_u.Add(grid_4_u, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_2_u.Add(self.Unlock, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.SetSizer(sizer_2_u)
        self.Layout()
        # end wxGlade

    def __onKeyClick(self,evt):
	button = (evt.GetEventObject()).Label
	if not ( (button == 'DEL') or (button == 'OK') ):
		self.passwd.append(button)
		self.pswd.SetValue(''.join(self.passwd))
	elif button == 'DEL' and (len(self.passwd)>0):
		self.passwd.pop()
		self.pswd.SetValue(''.join(self.passwd))
	else:
		self.Close()

    def getPasswd(self):
		return ''.join(self.passwd)

    def clearAll(self):
		self.passwd = []

    """
    def OnAlarmClick(self, event, ol, password):
	passvalue = self.pswd.GetValue()
	if  passvalue == password:
		try:
			self.olifant.unlock(passvalue)
		except OlifantException as ex:
			print ex.getMessage() #TODO far comparire box di errore
	else:			
		print "Le password sono diverse." #TODO far comparire dialog box di errore
    """

# end of class MyDialog1


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    Olifant_main = MyFrame(None, -1, "")
    app.SetTopWindow(Olifant_main)
    Olifant_main.Show()
    app.MainLoop()
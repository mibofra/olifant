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


class DialogUSbSelection(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: DialogUSbSelection.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.UsbSelectionLabel = wx.StaticText(self, -1, "Select Usb Key", style=wx.ALIGN_CENTRE)
        self.UsbSelectCombobox = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: DialogUSbSelection.__set_properties
        self.SetTitle("UsbSelect")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: DialogUSbSelection.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.UsbSelectionLabel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(self.UsbSelectCombobox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class DialogUSbSelection
class MyFrame(wx.Frame):

    olifant = None #olifant

    def __init__(self, *args, **kwds):

        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.LogoMainFrame_1 = wx.StaticBitmap(self, -1, wx.Bitmap("images/icon.png", wx.BITMAP_TYPE_ANY), style=wx.SIMPLE_BORDER)
        self.labelMainFrame_1 = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.MonitorModSelectionLabel = wx.StaticText(self, -1, "Select monitoring mode:", style=wx.ALIGN_CENTRE)
        self.MonitorModSelectionBox = wx.ComboBox(self, -1, choices=["Password mode", "USB mode", "Strong mode"], style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)
        self.LockButton = wx.Button(self, -1, "Lock")
        self.PowerSupplyCheckbox = wx.CheckBox(self, -1, "power supply")
        self.PowerBCheckbox = wx.CheckBox(self, -1, "power button")
        self.BatteryModCheckbox = wx.CheckBox(self, -1, "battery mode")
        self.ClosedlidModCheckbox = wx.CheckBox(self, -1, "closed lid")
        self.window_1 = wx.HyperlinkCtrl(self, -1, "About Olifant", "https://launchpad.net/olifant")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Olifant")
        self.SetSize((436, 316))
        self.SetFocus()
        self.LogoMainFrame_1.SetMinSize((64, 64))
        self.labelMainFrame_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.MonitorModSelectionBox.SetSelection(0)
        # end wxGlade

	self.MonitorModSelectionBox.SetEditable(False)
	self.PowerSupplyCheckbox.SetValue(True)
	self.PowerBCheckbox.SetValue(True)
	self.BatteryModCheckbox.SetValue(True)
	self.ClosedlidModCheckbox.SetValue(True)
	self.Bind(wx.EVT_BUTTON, self.OnLockClick, self.LockButton)

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        GridMainFrame = wx.GridSizer(1, 4, 0, 0)
        sizerMainFrame.Add((400, 20), 0, 0, 0)
        sizerMainFrame.Add(self.LogoMainFrame_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerMainFrame.Add(self.labelMainFrame_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerMainFrame.Add((400, 20), 0, 0, 0)
        sizerMainFrame.Add(self.MonitorModSelectionLabel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizerMainFrame.Add(self.MonitorModSelectionBox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizerMainFrame.Add(self.LockButton, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        GridMainFrame.Add(self.PowerSupplyCheckbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridMainFrame.Add(self.PowerBCheckbox, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridMainFrame.Add(self.BatteryModCheckbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridMainFrame.Add(self.ClosedlidModCheckbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        sizerMainFrame.Add(GridMainFrame, 1, wx.EXPAND, 0)
        sizerMainFrame.Add(self.window_1, 0, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(sizerMainFrame)
        sizerMainFrame.SetSizeHints(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    
    def OnLockClick(self, event):

	alarms = []
	if self.PowerSupplyCheckbox.IsChecked():
		alarms.append(Olifant.AC_ALARM)
	if self.PowerBCheckbox.IsChecked():
		alarms.append(Olifant.POWER_BUTTON_ALARM)
	if self.BatteryModCheckbox.IsChecked():
		alarms.append(Olifant.BATTERY_ALARM)
	if self.ClosedlidModCheckbox.IsChecked():
		alarms.append(Olifant.LID_OPENED_ALARM)

	if len(alarms) == 0:
		showError('Warning','You have all 3 options disabled, are you sure?Olifant will just do nothin')

	choice = self.MonitorModSelectionBox.GetCurrentSelection()
	try:
		if choice == 0:
			self.olifant = Olifant(Olifant.PASSWD_MODE,alarms)
		elif choice == 1:
			self.olifant = Olifant(Olifant.USB_MODE,alarms)
		elif choice == 2:
			self.olifant = Olifant(Olifant.STRONG_MODE,alarms)
		else:
			showError('Wrong Selection','Olifant option unknown')
	
		if choice == 0:
        		passdlg = MyDialog2(self,-1)
			passdlg.clearAll() #TODO we need this because of a bug
			passdlg.ShowModal()
			pwd = passdlg.getPasswd()

			if pwd == '':
				showError('Error!','password cannot be empty')
			else:
				try:
					self.olifant.lock(pwd)
					"""
					FlagList = ['FULLSCREEN_NOMENUBAR',
  						     'FULLSCREEN_NOTOOLBAR',
  				                     'FULLSCREEN_NOSTATUSBAR',
  				                     'FULLSCREEN_NOBORDER',
  				                     'FULLSCREEN_NOCAPTION',
  				                     'FULLSCREEN_ALL']
					self.ShowFullScreen(True,FlagList)
					"""
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

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog2.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.ChoosePswdLabel = wx.StaticText(self, -1, "Choose password", style=wx.ALIGN_CENTRE)
        self.ChoosePswdBox = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.ConfirmPswdLabel = wx.StaticText(self, -1, "Confirm password", style=wx.ALIGN_CENTRE)
        self.ConfirmPswdBox = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.KeypadButton_1 = wx.Button(self, -1, "1")
        self.KeypadButton_2 = wx.Button(self, -1, "2")
        self.KeypadButton_3 = wx.Button(self, -1, "3")
        self.KeypadButton_4 = wx.Button(self, -1, "4")
        self.KeypadButton_5 = wx.Button(self, -1, "5")
        self.KeypadButton_6 = wx.Button(self, -1, "6")
        self.KeypadButton_7 = wx.Button(self, -1, "7")
        self.KeypadButton_8 = wx.Button(self, -1, "8")
        self.KeypadButton_9 = wx.Button(self, -1, "9")
        self.KeypadButton_DEL = wx.Button(self, -1, "DEL")
        self.KeypadButton_0 = wx.Button(self, -1, "0")
        self.KeypadButtonButton_Enable = wx.Button(self, -1, "ENABLE")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.focus = self.ChoosePswdBox  

    def __set_properties(self):
        # begin wxGlade: MyDialog2.__set_properties
        self.SetTitle("dialog_3")
        self.SetSize((300, 370))
        self.ChoosePswdLabel.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.ChoosePswdBox.SetMinSize((150, 30))
        self.ConfirmPswdLabel.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.ConfirmPswdBox.SetMinSize((150, 30))
        self.KeypadButton_1.SetMinSize((50, 50))
        self.KeypadButton_2.SetMinSize((50, 50))
        self.KeypadButton_3.SetMinSize((50, 50))
        self.KeypadButton_4.SetMinSize((50, 50))
        self.KeypadButton_5.SetMinSize((50, 50))
        self.KeypadButton_6.SetMinSize((50, 50))
        self.KeypadButton_7.SetMinSize((50, 50))
        self.KeypadButton_8.SetMinSize((50, 50))
        self.KeypadButton_9.SetMinSize((50, 50))
        self.KeypadButton_DEL.SetMinSize((50, 50))
        self.KeypadButton_0.SetMinSize((50, 50))
        self.KeypadButtonButton_Enable.SetMinSize((50, 50))
        self.KeypadButtonButton_Enable.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        # end wxGlade

	self.ChoosePswdBox.SetEditable(False)
        self.KeypadButton_1.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_2.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_3.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_4.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_5.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_6.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_7.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_8.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_9.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_DEL.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButton_0.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.KeypadButtonButton_Enable.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.ChoosePswdBox.Bind(wx.EVT_SET_FOCUS, self.__onPswdBoxFocused)
        self.ConfirmPswdBox.Bind(wx.EVT_SET_FOCUS, self.__onPswdBoxFocused)
	#self.choose_pswd.SetEditable(False)

    def __do_layout(self):
        # begin wxGlade: MyDialog2.__do_layout
        sizerPswdDialog = wx.BoxSizer(wx.VERTICAL)
        GridPswdDialog_4 = wx.GridSizer(2, 3, 0, 0)
        GridPswdDialog_3 = wx.GridSizer(2, 3, 0, 0)
        GridPswdDialog_2 = wx.GridSizer(1, 3, 0, 0)
        GridPswdDialog_1 = wx.GridSizer(1, 3, 0, 0)
        sizerPswdDialog.Add(self.ChoosePswdLabel, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizerPswdDialog.Add(self.ChoosePswdBox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 6)
        sizerPswdDialog.Add(self.ConfirmPswdLabel, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerPswdDialog.Add(self.ConfirmPswdBox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 6)
        GridPswdDialog_1.Add(self.KeypadButton_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_1.Add(self.KeypadButton_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_1.Add(self.KeypadButton_3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizerPswdDialog.Add(GridPswdDialog_1, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridPswdDialog_2.Add(self.KeypadButton_4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_2.Add(self.KeypadButton_5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_2.Add(self.KeypadButton_6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizerPswdDialog.Add(GridPswdDialog_2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridPswdDialog_3.Add(self.KeypadButton_7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_3.Add(self.KeypadButton_8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_3.Add(self.KeypadButton_9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizerPswdDialog.Add(GridPswdDialog_3, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        GridPswdDialog_4.Add(self.KeypadButton_DEL, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_4.Add(self.KeypadButton_0, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        GridPswdDialog_4.Add(self.KeypadButtonButton_Enable, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizerPswdDialog.Add(GridPswdDialog_4, 1, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        self.SetSizer(sizerPswdDialog)
        self.Layout()
        # end wxGlade

    def __onKeyClick(self,evt):
	button = (evt.GetEventObject()).Label
	passwd = self.focus.GetValue()
	if button == 'DEL':
	   if len(passwd) > 0:
		passwd = self.passwd[:-1]
		self.focus.SetValue(passwd)
	elif button == 'ENABLE':
	   self.Close()
	else:
	   passwd += button
	   self.focus.SetValue(passwd)

    def __onPswdBoxFocused(self, evt):
	self.focus = evt.GetEventObject()

    def getPasswd(self):
	if self.ConfirmPswdBox.GetValue() != self.ChoosePswdBox.GetValue():
		showError('Error!','Password and confirmation do not match.')
	else:
		return self.ChoosePswdBox.GetValue()

    def clearAll(self):
		self.ChoosePswdBox.SetValue("")
		self.ConfirmPswdBox.SetValue("")


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
        self.AboutLogo = wx.StaticBitmap(self, -1, wx.Bitmap("images/icon.png", wx.BITMAP_TYPE_ANY))
        self.AboutLabel_1 = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.AboutLabel_2 = wx.StaticText(self, -1, "https://launchpad.net/olifant", style=wx.ALIGN_CENTRE)
        self.AboutLabel_3 = wx.StaticText(self, -1, "author")
        self.AboutLabel_4 = wx.StaticText(self, -1, "kokito\n(jumba@LP)", style=wx.ALIGN_CENTRE)
        self.AboutLabel_5 = wx.StaticText(self, -1, "Actual developers")
        self.AboutLabel_6 = wx.StaticText(self, -1, "Cristian_C\nSquall867")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyPanel.__set_properties
        self.SetSize((312, 312))
        self.AboutLogo.SetMinSize((16, 16))
        self.AboutLabel_1.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.AboutLabel_2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.AboutLabel_3.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.AboutLabel_5.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        AboutSizer = wx.BoxSizer(wx.VERTICAL)
        AboutSizer.Add(self.AboutLogo, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 8)
        AboutSizer.Add(self.AboutLabel_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        AboutSizer.Add(self.AboutLabel_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        AboutSizer.Add(self.AboutLabel_3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        AboutSizer.Add(self.AboutLabel_4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        AboutSizer.Add(self.AboutLabel_5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        AboutSizer.Add(self.AboutLabel_6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        self.SetSizer(AboutSizer)
        # end wxGlade

# end of class MyPanel


class MyDialog(wx.Dialog):

    olifant = None
    parentFrame = None

    def __init__(self,*args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.LogoActivated = wx.StaticBitmap(self, -1, wx.Bitmap("images/icon.png", wx.BITMAP_TYPE_ANY))
        self.ActivatedLabel_1 = wx.StaticText(self, -1, "Olifant 1.0", style=wx.ALIGN_CENTRE)
        self.ActivatedLabel_2 = wx.StaticText(self, -1, "ALARM ACTIVATED", style=wx.ALIGN_CENTRE)
        self.AlarmActivatedUnlockButton = wx.Button(self, -1, "Unlock")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("dialog_1")
        self.LogoActivated.SetMinSize((16, 16))
        self.ActivatedLabel_1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.ActivatedLabel_2.SetForegroundColour(wx.Colour(255, 0, 0))
        self.ActivatedLabel_2.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        # end wxGlade
	self.AlarmActivatedUnlockButton.Bind(wx.EVT_BUTTON,self.OnUnlockClick)

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        SizerAlarmActivated = wx.BoxSizer(wx.VERTICAL)
        SizerAlarmActivated.Add((400, 30), 0, 0, 0)
        SizerAlarmActivated.Add(self.LogoActivated, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        SizerAlarmActivated.Add(self.ActivatedLabel_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        SizerAlarmActivated.Add(self.ActivatedLabel_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 26)
        SizerAlarmActivated.Add((400, 30), 0, 0, 0)
        SizerAlarmActivated.Add(self.AlarmActivatedUnlockButton, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        SizerAlarmActivated.Add((400, 30), 0, 0, 0)
        self.SetSizer(SizerAlarmActivated)
        SizerAlarmActivated.Fit(self)
        self.Layout()
        # end wxGlade

    def setOlifant(self,olifant):
	self.olifant = olifant

    def setParentFrame(self,frame):
	self.parentFrame = frame

    def OnUnlockClick(self,evt):
        passdlg = MyDialog1(self, -1)
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

    passwd = []

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog1.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.UnlockPswdLabel = wx.StaticText(self, -1, "Password", style=wx.ALIGN_CENTRE)
        self.UnlockPswdTextbox = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.UnlockKeypadButton_1 = wx.Button(self, -1, "1")
        self.UnlockKeypadButton_2 = wx.Button(self, -1, "2")
        self.UnlockKeypadButton_3 = wx.Button(self, -1, "3")
        self.UnlockKeypadButton_4 = wx.Button(self, -1, "4")
        self.UnlockKeypadButton_5 = wx.Button(self, -1, "5")
        self.UnlockKeypadButton_6 = wx.Button(self, -1, "6")
        self.UnlockKeypadButton_7 = wx.Button(self, -1, "7")
        self.UnlockKeypadButton_8 = wx.Button(self, -1, "8")
        self.UnlockKeypadButton_9 = wx.Button(self, -1, "9")
        self.UnlockKeypadButton_DEL = wx.Button(self, -1, "DEL")
        self.UnlockKeypadButton_0 = wx.Button(self, -1, "0")
        self.UnlockKeypadButton_Disable = wx.Button(self, -1, "DISABLE")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog1.__set_properties
        self.SetTitle("dialog_2")
        self.SetSize((300, 321))
        self.UnlockPswdLabel.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.UnlockPswdTextbox.SetMinSize((150, 30))
        self.UnlockKeypadButton_1.SetMinSize((50, 50))
        self.UnlockKeypadButton_2.SetMinSize((50, 50))
        self.UnlockKeypadButton_3.SetMinSize((50, 50))
        self.UnlockKeypadButton_4.SetMinSize((50, 50))
        self.UnlockKeypadButton_5.SetMinSize((50, 50))
        self.UnlockKeypadButton_6.SetMinSize((50, 50))
        self.UnlockKeypadButton_7.SetMinSize((50, 50))
        self.UnlockKeypadButton_8.SetMinSize((50, 50))
        self.UnlockKeypadButton_9.SetMinSize((50, 50))
        self.UnlockKeypadButton_DEL.SetMinSize((50, 50))
        self.UnlockKeypadButton_0.SetMinSize((50, 50))
        self.UnlockKeypadButton_Disable.SetMinSize((50, 50))
        self.UnlockKeypadButton_Disable.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        # end wxGlade

	self.UnlockPswdTextbox.SetEditable(False)
        self.UnlockKeypadButton_1.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_2.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_3.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_4.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_5.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_6.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_7.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_8.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_9.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_DEL.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_0.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)
        self.UnlockKeypadButton_Disable.Bind(wx.EVT_BUTTON,self.__onKeyClick)#,self.button_1_u)


    def __do_layout(self):
        # begin wxGlade: MyDialog1.__do_layout
        UnlockSizer = wx.BoxSizer(wx.VERTICAL)
        UnlockGrid_4 = wx.GridSizer(2, 3, 0, 0)
        UnlockGrid_3 = wx.GridSizer(2, 3, 0, 0)
        UnlockGrid_2 = wx.GridSizer(1, 3, 0, 0)
        UnlockGrid_1 = wx.GridSizer(1, 3, 0, 0)
        UnlockSizer.Add(self.UnlockPswdLabel, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)
        UnlockSizer.Add(self.UnlockPswdTextbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 6)
        UnlockGrid_1.Add(self.UnlockKeypadButton_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_1.Add(self.UnlockKeypadButton_2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_1.Add(self.UnlockKeypadButton_3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockSizer.Add(UnlockGrid_1, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        UnlockGrid_2.Add(self.UnlockKeypadButton_4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_2.Add(self.UnlockKeypadButton_5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_2.Add(self.UnlockKeypadButton_6, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockSizer.Add(UnlockGrid_2, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        UnlockGrid_3.Add(self.UnlockKeypadButton_7, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_3.Add(self.UnlockKeypadButton_8, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_3.Add(self.UnlockKeypadButton_9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockSizer.Add(UnlockGrid_3, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        UnlockGrid_4.Add(self.UnlockKeypadButton_DEL, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_4.Add(self.UnlockKeypadButton_0, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockGrid_4.Add(self.UnlockKeypadButton_Disable, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        UnlockSizer.Add(UnlockGrid_4, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        self.SetSizer(UnlockSizer)
        self.Layout()
        # end wxGlade

    def __onKeyClick(self,evt):
	button = (evt.GetEventObject()).Label
	if not ( (button == 'DEL') or (button == 'DISABLE') ):
		self.passwd.append(button)
		self.UnlockPswdTextbox.SetValue(''.join(self.passwd))
	elif button == 'DEL' and (len(self.passwd)>0):
		self.passwd.pop()
		self.UnlockPswdTextbox.SetValue(''.join(self.passwd))
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

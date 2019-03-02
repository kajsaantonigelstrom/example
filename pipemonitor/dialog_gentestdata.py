import wx

class GenerateTestdataDialog(wx.Dialog): 
   def __init__(self, parent, title, controller):
      self.controller = controller
      super(GenerateTestdataDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 

      sizer = wx.GridBagSizer(6, 2)

      y = 0;
      combo = wx.StaticText(panel, label="count")
      sizer.Add(combo, pos=(y, 0), flag=wx.ALIGN_CENTER, border=5)
      tc2 = wx.TextCtrl(panel)
      sizer.Add(tc2, pos=(y, 1), flag=wx.EXPAND, border=5)


      y = y +1
      btn = wx.Button(panel, label = "Generate Test Data")
      sizer.Add(btn, pos=(y, 0), span=(0,2), flag=wx.ALIGN_CENTER, border=5)
      self.Bind(wx.EVT_BUTTON, self.OnClick, btn)

      panel.SetSizer(sizer)
      sizer.Fit(parent)

   def OnClick(self, event):
      dial = wx.MessageDialog(None, 'All current Brains will be wiped. Sure?', 'WARNING!!!',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
      if dial.ShowModal() == wx.ID_YES:
          self.controller.CreateTestData(5);

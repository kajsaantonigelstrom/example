import wx

class GenerateTestdataDialog(wx.Dialog): 
   def __init__(self, parent, title, controller):
      self.controller = controller
      super(GenerateTestdataDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 

      vbox = wx.BoxSizer(wx.VERTICAL)
      hbox = wx.BoxSizer(wx.HORIZONTAL)

      t1 = wx.StaticText(panel, label="No of Brains")
      hbox.Add(t1);
      tc2 = wx.TextCtrl(panel)
      hbox.Add(tc2)
      vbox.Add((15, 15))
      vbox.Add(hbox, flag=wx.ALIGN_CENTER)

      btn_genbrains = wx.Button(panel, label = "Generate Test Data")
      btn_cancel = wx.Button(panel, label = "Cancel")
      vbox.Add(btn_genbrains, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_cancel, flag=wx.ALIGN_CENTER)
      self.Bind(wx.EVT_BUTTON, self.OnClick, btn_genbrains)

      panel.SetSizer(vbox)

   def OnClick(self, event):
      dial = wx.MessageDialog(None, 'All current Brains will be wiped. Sure?', 'WARNING!!!',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
      if dial.ShowModal() == wx.ID_YES:
          self.controller.CreateTestData(5);

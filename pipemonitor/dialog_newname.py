import wx

class AskNameDialog(wx.Dialog): 
   def __init__(self, parent, title, oldname): 
      super(AskNameDialog, self).__init__(parent, title = title) 
      panel = wx.Panel(self) 

      vbox = wx.BoxSizer(wx.VERTICAL)
      t1 = wx.StaticText(panel, label="Recipe Name:")
      vbox.Add(t1, flag=wx.ALIGN_CENTER)
      self.name = wx.TextCtrl(panel)
      self.name.SetValue(oldname)
      vbox.Add(self.name, flag=wx.ALIGN_CENTER)

      btn_ok = wx.Button(panel, id=wx.ID_OK)
      self.Bind(wx.EVT_BUTTON, self.OnClick, btn_ok)
      btn_cancel = wx.Button(panel, id=wx.ID_CANCEL)
      vbox.Add(btn_ok, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_cancel, flag=wx.ALIGN_CENTER)

      panel.SetSizer(vbox)
      self.newname = ""
   def OnClick(self, event):
       self.newname = self.name.GetValue();
       wx.Window.Close(self)
   def GetNewName(self):
       return self.newname

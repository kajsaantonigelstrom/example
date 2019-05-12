import wx

# Generate Jobs dialog

class GenerateJobsDialog(wx.Dialog): 
   def __init__(self, parent, title, controller): 
      self.controller = controller
      super(GenerateJobsDialog, self).__init__(parent, title = title, size = (250,200))
      panel = wx.Panel(self) 

      vbox = wx.BoxSizer(wx.VERTICAL)

      combo = wx.StaticText(panel, label="Recipe:")
      vbox.Add((14, 14))
      vbox.Add(combo, flag=wx.ALIGN_CENTER)

      recipes = controller.GetRecipeList()
      self.cb = wx.ComboBox(panel, pos=wx.DefaultPosition, size=wx.DefaultSize,
          choices=recipes, style=0, validator=wx.DefaultValidator,
            name=wx.ComboBoxNameStr)
      self.cb.SetSelection(0)
      btn_genjobs = wx.Button(panel, label = "Generate Jobs")
      self.Bind(wx.EVT_BUTTON, self.OnClick, btn_genjobs)
      btn_cancel = wx.Button(panel, id=wx.ID_CANCEL)
      self.logcheckbox = wx.CheckBox(panel, label="Delete Old Logfiles", style=wx.CHK_2STATE)
      self.logcheckbox.SetValue(self.controller.deletelogfileflag)
      vbox.Add(self.cb, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_genjobs, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_cancel, flag=wx.ALIGN_CENTER)
      vbox.Add((14, 14))
      vbox.Add(self.logcheckbox, flag=wx.ALIGN_CENTER)
      vbox.Add((14, 14))
      panel.SetSizer(vbox)

   def OnClick(self, event):
       recipe = self.cb.GetStringSelection()
       self.controller.deletelogfileflag = self.logcheckbox.IsChecked()
       error = self.controller.CreateJobs(recipe)
       if (error != ""):
           dial = wx.MessageDialog(None, error, 'WARNING!!!',
            wx.OK | wx.ICON_QUESTION)
           dial.ShowModal()
       self.Destroy()

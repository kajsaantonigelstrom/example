import wx

class GenerateJobsDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(GenerateJobsDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 

      vbox = wx.BoxSizer(wx.VERTICAL)

      combo = wx.StaticText(panel, label="Recipe:")
      vbox.Add((14, 14))
      vbox.Add(combo, flag=wx.ALIGN_CENTER)

      recipes = ['Recipe 1', 'Kajsas recept']
      cb = wx.ComboBox(panel, pos=wx.DefaultPosition, size=wx.DefaultSize,
          choices=recipes, style=0, validator=wx.DefaultValidator,
            name=wx.ComboBoxNameStr)
      btn_genjobs = wx.Button(panel, label = "Generate Jobs")
      btn_cancel = wx.Button(panel, label = "Cancel")
      vbox.Add(cb, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_genjobs, flag=wx.ALIGN_CENTER)
      vbox.Add(btn_cancel, flag=wx.ALIGN_CENTER)

      panel.SetSizer(vbox)

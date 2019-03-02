import wx

class GenerateJobsDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(GenerateJobsDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 

      sizer = wx.GridBagSizer(6, 2)

      y = 0;
      combo = wx.StaticText(panel, label="Recipe:")
      sizer.Add(combo, pos=(y, 0), flag=wx.ALIGN_CENTER, border=5)

      recipes = ['Recipe 1', 'Kajsas recept']
      cb = wx.ComboBox(panel, pos=wx.DefaultPosition, size=wx.DefaultSize,
          choices=recipes, style=0, validator=wx.DefaultValidator,
            name=wx.ComboBoxNameStr)
      sizer.Add(cb, pos=(y, 1), flag=wx.ALIGN_CENTER, border=5)

      y = y +1
      btn = wx.Button(panel, label = "Generate Jobs")
      sizer.Add(btn, pos=(y, 0), span=(0,2), flag=wx.ALIGN_CENTER, border=5)

      panel.SetSizer(sizer)
      sizer.Fit(parent)      
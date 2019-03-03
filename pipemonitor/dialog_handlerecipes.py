import wx

class HandleRecipesDialog(wx.Dialog): 
   def __init__(self, parent, title, controller): 
      self.controller = controller
      super(HandleRecipesDialog, self).__init__(parent, title = title, size = (350,250)) 
      panel = wx.Panel(self) 

      vbox = wx.BoxSizer(wx.VERTICAL)
      vbox.Add((15, 15))

      hbox2 = wx.BoxSizer(wx.HORIZONTAL)


      currentjobs = ['Recipe 1', 'Kajas recept', '<new>'] 
      currlist = wx.ListBox(panel, size = (100,-1), choices = currentjobs, style = wx.LB_SINGLE)        
      hbox2.Add(currlist, proportion=1, flag=wx.EXPAND)

      hbox2.Add((5, 5))

      tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
      hbox2.Add(tc3, proportion=1, flag=wx.EXPAND)

      vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

      hbox = wx.BoxSizer(wx.HORIZONTAL)
      btn_save = wx.Button(panel, label="Save")
      btn_close = wx.Button(panel, label="Close")
      hbox.Add(btn_save)
      hbox.Add(btn_close)
      vbox.Add(hbox,flag=wx.ALIGN_RIGHT)

      panel.SetSizer(vbox)

import wx

class HandleRecipesDialog(wx.Dialog): 
   def __init__(self, parent, title): 
      super(HandleRecipesDialog, self).__init__(parent, title = title, size = (250,150)) 
      panel = wx.Panel(self) 

      sizer = wx.GridBagSizer(6, 2)

      y = 0;
      currentjobs = ['Recipe 1', 'Kajas recept', '<new>'] 
      currlist = wx.ListBox(panel, size = (100,-1), choices = currentjobs, style = wx.LB_SINGLE)        
      sizer.Add(currlist, pos=(y, 0), flag=wx.EXPAND|wx.ALL, border=5)

      tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
      sizer.Add(tc3, pos=(y, 1), flag=wx.EXPAND|wx.ALL, border=5)
      y = y +1
      
      j3 = wx.Button(panel, label="Save")#, pos=(200, 325))
      sizer.Add(j3, pos=(y, 1), border=5)

      
      panel.SetSizer(sizer)
      sizer.Fit(parent)
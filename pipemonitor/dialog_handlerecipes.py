import wx
NEWNAME = "<new>"
from dialog_newname import AskNameDialog

class HandleRecipesDialog(wx.Dialog): 
    def __init__(self, parent, title, controller): 
        self.controller = controller
        super(HandleRecipesDialog, self).__init__(parent, title = title, size = (750,250)) 
        panel = wx.Panel(self) 

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((15, 15))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)


        self.recipelist = wx.ListBox(panel, size = (100,-1), style = wx.LB_SINGLE)        
        self.Bind(wx.EVT_LISTBOX, self.SelectRecipe, self.recipelist)
        hbox2.Add(self.recipelist, proportion=1, flag=wx.EXPAND)

        hbox2.Add((5, 5))

        self.tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(150,150))
        hbox2.Add(self.tc3, proportion=4, flag=wx.EXPAND)

        vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_save = wx.Button(panel, label="Save")
        btn_close = wx.Button(panel, label="Close")
        btn_rename = wx.Button(panel, label="Rename")
        btn_delete = wx.Button(panel, label="Delete")
        self.Bind(wx.EVT_BUTTON, self.Save, btn_save)
        self.Bind(wx.EVT_BUTTON, self.Close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.Rename, btn_rename)
        self.Bind(wx.EVT_BUTTON, self.Delete, btn_delete)
        hbox.Add(btn_rename)
        hbox.Add(btn_delete)
        hbox.Add(btn_save)
        hbox.Add(btn_close)
        vbox.Add(hbox,flag=wx.ALIGN_CENTER)

        panel.SetSizer(vbox)
      
        self.UpdateRecipeList()
        self.recipelist.SetSelection(0)
        self.SelectRecipe(None)

    def UpdateRecipeList(self):
        recipelist = self.controller.GetRecipeList()
        recipelist.append(NEWNAME)
        self.recipelist.Set(recipelist)
        
    def SelectRecipe(self, event):
        ix = self.recipelist.GetSelection()
        recipe = self.controller.GetRecipe(self.recipelist.GetString(ix))
        self.tc3.SetValue(recipe)

    # Name entry dialog used for New and Rename
    def AskForNewName(self, title, currname):
        dlg = AskNameDialog(self, title, currname);
        dlg.ShowModal()
        newname = dlg.GetNewName()
        dlg.Destroy()
        return newname

    # Methods bound to the buttons
    def Save(self, event):
        ix = self.recipelist.GetSelection()
        recipename = self.recipelist.GetString(ix)
        if (recipename == NEWNAME):
            recipename = self.AskForNewName("Save New Recipe", "")
        if (recipename != ""):
            res = self.controller.WriteRecipe(recipename, self.tc3.GetValue())
            if (not res):
                print ("Error writing", recipename)
        self.UpdateRecipeList()
        self.recipelist.SetSelection(ix)
        self.SelectRecipe(None)
        
    def Close(self, event):
        wx.Window.Close(self)
        #wx.PostEvent(self, wx.CLOSE_WINDOW)
        return

    def Rename(self, event):
        ix = self.recipelist.GetSelection()
        recipename = self.recipelist.GetString(ix)
        if (recipename == NEWNAME):
            return
        newname = self.AskForNewName("Rename Recipe", recipename)
        if (newname != recipename):
            self.controller.RenameRecipe(recipename, newname)
        self.UpdateRecipeList()
        self.recipelist.SetSelection(ix)
        self.SelectRecipe(None)
        return
    def Delete(self, event):
        ix = self.recipelist.GetSelection()
        recipename = self.recipelist.GetString(ix)
        if (recipename == NEWNAME):
            return
        dial = wx.MessageDialog(None, 'You want to delete '+recipename+"?", 'WARNING!!!',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.controller.DeleteRecipe(recipename)
        self.UpdateRecipeList()
        self.recipelist.SetSelection(ix)
        self.SelectRecipe(None)
        return

            
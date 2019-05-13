import wx
# The Select Brains dialog
class SelectBrainsDialog(wx.Dialog):
    def __init__(self, parent, title, controller):
        self.controller = controller
        super(SelectBrainsDialog, self).__init__(parent, title=title, size=(250, 550))

        #get the current selection from the controller
        self.selections = controller.GetSelections()

        panel = wx.Panel(self)

        self.sellist = wx.CheckListBox(panel,choices=self.selections.choices,size=(-1,450))
        for ix in range(0, len(self.selections.choices)):
            self.sellist.Check(ix, self.selections.selection[ix])
        btn_cancel = wx.Button(panel, id=wx.ID_CANCEL)

        btn_ok = wx.Button(panel, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.btn_OK, btn_ok)

        btn_all = wx.Button(panel, label="Select All")
        self.Bind(wx.EVT_BUTTON, self.bnt_selectAll, btn_all)

        btn_none = wx.Button(panel, label="UNselect All")
        self.Bind(wx.EVT_BUTTON, self.bnt_selectNone, btn_none)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(15,15)
        
        topbox = wx.BoxSizer(wx.HORIZONTAL)
        topbox.Add(self.sellist, 2, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)

        selbox = wx.BoxSizer(wx.VERTICAL)
        selbox.Add(btn_all, flag=wx.ALIGN_CENTER_VERTICAL)
        selbox.Add(btn_none, flag=wx.ALIGN_CENTER_VERTICAL)

        topbox.Add(selbox, 1, flag=wx.ALIGN_CENTER_VERTICAL)

        vbox.Add(topbox)

        okbox = wx.BoxSizer(wx.HORIZONTAL)
        okbox.Add(btn_ok, flag=wx.ALIGN_CENTER)
        okbox.Add(btn_cancel, flag=wx.ALIGN_CENTER)
        vbox.Add(15,15);
        vbox.Add(okbox, flag=wx.ALIGN_CENTER)
        panel.SetSizer(vbox)

    def btn_OK(self, event):
        # Transfer selections from control to selections
        for ix in range(0,len(self.selections.choices)):
            self.selections.selection[ix] = self.sellist.IsChecked(ix)
        self.selections.write()
        self.Destroy()

    def bnt_selectAll(self, event):
        # Set all checkboxes
        for ix in range(0, len(self.selections.choices)):
            self.sellist.Check(ix, True)

    def bnt_selectNone(self, event):
        # Set all checkboxes
        for ix in range(0, len(self.selections.choices)):
            self.sellist.Check(ix, False)

import wx
import sys
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        #menu bar
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()        
        file.Append(101, '&quit', 'Quit')
        file.Append(102, '&save', 'Save')
        #edit.Append(101, '', 'Copy')
        #edit.Append(101, '', 'Paste')
        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')

        sizer = wx.GridBagSizer(10, 7)

        # Buttons
        b1 =wx.Button(self, label="QUIT")
        self.Bind(wx.EVT_BUTTON, self.OnClick,b1)

        b2 =wx.Button(self, label="button with long text")#, pos=(200, 325))
        sizer.Add(b1, pos=(0, 3), flag=wx.ALIGN_CENTER, border=15)

        sizer.Add(b2, pos=(1, 3), flag=wx.ALIGN_CENTER, border=5)

        textinput = wx.StaticText(self, label="text input")
        sizer.Add(textinput, pos=(2, 0), flag=wx.ALIGN_CENTER, border=5)
        tc2 = wx.TextCtrl(self)
        sizer.Add(tc2, pos=(2, 1), span=(1, 6), flag=wx.EXPAND, border=5)

        mult = wx.StaticText(self, label="multeline input")
        sizer.Add(mult, pos=(3, 0), flag=wx.ALIGN_CENTER, border=5)
        tc3 = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(tc3, pos=(3, 1), span=(1, 6), flag=wx.EXPAND, border=5)

        l1 = wx.StaticText(self, label="list")
        sizer.Add(l1, pos=(4, 0), flag=wx.ALIGN_CENTER, border=5)

        languages = ['alt1', 'alt2', 'alt3', 'alt4', 'alt5', 'alt6'] 
        lst = wx.ListBox(self, size = (100,-1), choices = languages, style = wx.LB_SINGLE)        
        sizer.Add(lst, pos=(4, 1), span=(1, 6), flag=wx.EXPAND, border=5)


        combo = wx.StaticText(self, label="combo")
        sizer.Add(combo, pos=(5, 0), flag=wx.ALIGN_CENTER, border=5)
        cb = wx.ComboBox(self, pos=wx.DefaultPosition, size=wx.DefaultSize,
            choices=languages, style=0, validator=wx.DefaultValidator,
            name=wx.ComboBoxNameStr)
        sizer.Add(cb, pos=(5, 1), span=(1, 6), flag=wx.EXPAND, border=5)

        #Radio buttons
        radiosizer = wx.BoxSizer(wx.HORIZONTAL)
        rb1 = wx.RadioButton(self, -1, 'One', (10, 10), style=wx.RB_GROUP)
        rb2 = wx.RadioButton(self, -1, 'Two', (10, 30))
        rt = wx.StaticText(self, label="Radio")
        radiosizer.Add(rt, 1);
        radiosizer.Add(rb1, 1)
        radiosizer.Add(rb2, 1)
        sizer.Add(radiosizer, pos=(6, 3), border=5)
        #Checkbox
        cb = wx.CheckBox(self, -1 ,'toggle')
        sizer.Add(cb, pos=(7, 0), border=5)
        # SLider
        s1 = wx.StaticText(self, label="slider")
        sizer.Add(s1, pos=(8, 0), flag=wx.ALIGN_CENTER,  border=5)
        slider1 = wx.Slider(self, -1, 0, 0, 1000, size=(250,25))
        sizer.Add(slider1, pos=(8, 1), span=(2, 5), border=5)

        #Progress bar
        s1 = wx.StaticText(self, label="progress")
        sizer.Add(s1, pos=(10, 0), flag=wx.ALIGN_CENTER,  border=5)
        gauge = wx.Gauge(self, -1, 50, size=(250, 25))
        sizer.Add(gauge, pos=(10, 1), span=(2, 5), border=5)
        gauge.SetValue(20)

        # add menu and status
        parent.SetMenuBar(menubar)
        parent.SetTitle('wxpython')


        self.toolbar = parent.CreateToolBar()
        self.toolbar.AddTool(1, '', wx.Bitmap('exit.png'))
        self.toolbar.Realize()

        self.statusbar = parent.CreateStatusBar()
        self.statusbar.SetStatusText('Status : x')

        
        sizer.AddGrowableCol(2)
        self.SetSizer(sizer)
        sizer.Fit(parent)
        
    def OnClick(self,event):
        sys.exit()


app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
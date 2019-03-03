import wx
from dialog_gentestdata import GenerateTestdataDialog
from dialog_genjobs import GenerateJobsDialog
from dialog_handlerecipes import HandleRecipesDialog

class MainWindow(wx.Frame):
    def __init__(self, parent, monitor):
        super(MainWindow, self).__init__(parent, title="hej", size=(500,500))

        menubar = wx.MenuBar()
        file = wx.Menu()
        functions = wx.Menu()        
        file.Append(101, '&quit', 'Quit')
        functions.Append(102, '&recipes', 'Handle Recipes');
        functions.Append(103, '&jobs', 'Generate Jobs');
        functions.Append(104, '&testdata', 'Generate Test Brains');

        menubar.Append(file, '&File')
        menubar.Append(functions, 'F&unctions')
        self.SetMenuBar(menubar)
        menubar.Bind(wx.EVT_MENU, self.menuhandler) 
        self.SetTitle('Kajsas Pipe Monitor')
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(2000)

        self.monitor = monitor
        self.InitUI()
        self.Centre()

    def update(self, event):
        self.monitor.updatebrainstate();
        self.currlist.Set(self.monitor.currentjobs)
        self.queuelist.Set(self.monitor.jobqueue)
        self.finishedlist.Set(self.monitor.finishedjobs)
            
        

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='On-going jobs:')
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 5))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.currlist = wx.ListBox(panel, size = (100,-1))        
        hbox3.Add(self.currlist, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=10)

        vbox.Add((-1, 5))
        # Headers for queue/finished
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(panel, label='Job Queue:')
        hbox2.Add(st3, 3, wx.ALIGN_LEFT)
        st4 = wx.StaticText(panel, label='Finished:')
#        hbox2.AddSpacer(150)
        hbox2.Add(st4, 3, wx.ALIGN_RIGHT)
#        hbox2.AddSpacer(150)
        vbox.Add(hbox2, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        # Listboxes for queue/finished
        vbox.Add((-1, 5))
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.queuelist = wx.ListBox(panel, size = (100,-1))        
        self.finishedlist = wx.ListBox(panel, size = (100,-1))        
        hbox3.Add(self.queuelist, proportion=1, flag=wx.EXPAND)
        hbox3.Add((5, 5))
        hbox3.Add(self.finishedlist, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        # Buttons for queue/finished
        vbox.Add((-1, 5))
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(panel, label="Total:")
        j2 = wx.TextCtrl(panel)
        j3 = wx.Button(panel, label="Clear")#, pos=(200, 325))
        jobsizer.Add(j1, 0);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);

        j1 = wx.StaticText(panel, label="Total:")
        j2 = wx.TextCtrl(panel)
        j3 = wx.Button(panel, label="Clear")#, pos=(200, 325))
        jobsizer.Add(j1, 0);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        # Job Folder
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(panel, label="Job Folder")
        j2 = wx.TextCtrl(panel)
        j3 = wx.Button(panel, label="...")#, pos=(200, 325))
        jobsizer.Add(j1, 1);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        # Brains Folder
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(panel, label="Brains Folder")
        j2 = wx.TextCtrl(panel)
        j3 = wx.Button(panel, label="...")#, pos=(200, 325))
        jobsizer.Add(j1, 1);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        panel.SetSizer(vbox)
        
    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        elif id == 102:
            #self.SelectTestDataFolder(event)
            HandleRecipesDialog(self, "Handle Recipes").ShowModal();
        elif id == 103:
            GenerateJobsDialog(self, "Generate Jobs").ShowModal();
        elif id == 104:
            GenerateTestdataDialog(self, "Generate Test Brains", self.monitor).ShowModal();
        self.Show()
    def SelectTestDataFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:    
            x = 1


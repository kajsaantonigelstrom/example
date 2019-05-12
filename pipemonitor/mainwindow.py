import wx
import sys
from dialog_gentestdata import GenerateTestdataDialog
from dialog_genjobs import GenerateJobsDialog
from dialog_handlerecipes import HandleRecipesDialog

class MainWindow(wx.Frame):
    def __init__(self, parent, monitor):
        super(MainWindow, self).__init__(parent, title="hej", size=(650,650))

        menubar = wx.MenuBar()
        file = wx.Menu()
        functions = wx.Menu()        
        file.Append(101, '&Quit', 'Quit')
        functions.Append(102, '&Handle Recipes', 'Handle Recipes');
        functions.Append(103, '&Generate Jobs', 'Generate Jobs');
        functions.Append(104, '&Generate Test Brains', 'Generate Test Brains');

        menubar.Append(file, '&File')
        menubar.Append(functions, 'F&unctions')
        self.SetMenuBar(menubar)
        menubar.Bind(wx.EVT_MENU, self.menuhandler) 
        self.SetTitle('Kajsas Pipe Monitor')
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateUI, self.timer)
        self.timer.Start(2000)

        self.monitor = monitor
        self.InitUI()
        self.Centre()

    def updateUI(self, event=None):
        self.monitor.updatebrainstate();
        self.currlist.Set(self.monitor.currentjobs)
        self.queuelist.Set(self.monitor.jobqueue)
        self.finishedlist.Set(self.monitor.finishedjobs)
        self.finished_total.SetLabel(str(len(self.monitor.finishedjobs)))
        self.queue_total.SetLabel(str(len(self.monitor.jobqueue)))
        

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # The listbox with on-going jobs
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='On-going jobs:       ')
        banana = wx.StaticBitmap(panel, -1, wx.Bitmap("banana.png", wx.BITMAP_TYPE_ANY), (0, 0), (32, 32))
        banana.Bind(wx.EVT_LEFT_DOWN, self.GoingBananas)

        hbox2.Add(st2)
        hbox2.Add(banana, flag=wx.RIGHT)
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
        self.queue_hdr = wx.StaticText(panel, label="Total: ")
        self.queue_total = wx.StaticText(panel, label="0")
        self.queue_clear = wx.Button(panel, label="Clear")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.ClearQueue, self.queue_clear)
        jobsizer.Add(self.queue_hdr, 0);
        jobsizer.Add(self.queue_total, 3);
        jobsizer.Add(self.queue_clear, 0);

        self.finished_hdr = wx.StaticText(panel, label="Total: ")
        self.finished_total = wx.StaticText(panel, label = "0")
        self.finished_clear = wx.Button(panel, label="Clear")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.ClearFinished, self.finished_clear)
        jobsizer.Add(self.finished_hdr, 0);
        jobsizer.Add(self.finished_total, 3);
        jobsizer.Add(self.finished_clear, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

        # Job Folder
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        jobfolder_hdr = wx.StaticText(panel, label="Job Folder")
        self.jobfolder_txt = wx.TextCtrl(panel)
        self.jobfolder_txt.SetValue(self.monitor.jobfolder);
        jobfolder_sel = wx.Button(panel, label="...")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.SelectJobFolder, jobfolder_sel)
        jobsizer.Add(jobfolder_hdr, 1);
        jobsizer.Add(self.jobfolder_txt, 3);
        jobsizer.Add(jobfolder_sel, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        # Brains Folder
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        brainsfolder_hdr = wx.StaticText(panel, label="Brains Folder")
        self.brainsfolder_txt = wx.TextCtrl(panel)
        self.brainsfolder_txt.SetValue(self.monitor.braintopfolder);
        brainsfolder_sel = wx.Button(panel, label="...")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.SelectBrainFolder, brainsfolder_sel)
        jobsizer.Add(brainsfolder_hdr, 1);
        jobsizer.Add(self.brainsfolder_txt, 3);
        jobsizer.Add(brainsfolder_sel, 0);
        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)
        
        panel.SetSizer(vbox)
        
    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        elif id == 102:
            #self.SelectTestDataFolder(event)
            HandleRecipesDialog(self, "Handle Recipes", self.monitor).ShowModal();
        elif id == 103:
            GenerateJobsDialog(self, "Generate Jobs", self.monitor).ShowModal();
        elif id == 104:
            GenerateTestdataDialog(self, "Generate Test Brains", self.monitor).ShowModal();
        self.updateUI()

    # Methods bound to the buttons:
    def SelectJobFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.SetPath(self.monitor.jobfolder)
        if dlg.ShowModal() == wx.ID_OK:    
            self.monitor.SetJobFolder(dlg.GetPath())
            self.jobfolder_txt.SetValue(self.monitor.jobfolder);

    def SelectBrainFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.SetPath(self.monitor.braintopfolder)
        if dlg.ShowModal() == wx.ID_OK:    
            self.monitor.SetBrainsFolder(dlg.GetPath())
            self.brainsfolder_txt.SetValue(self.monitor.braintopfolder);

    def ClearFinished(self, event):
        self.monitor.ClearFinished()
        self.updateUI()
        
    def ClearQueue(self, event):
        self.monitor.ClearQueue()
        self.updateUI()

    def GoingBananas(self, event):
        dial = wx.MessageDialog(None, 'All current Jobs will be deleted. Sure?\n(Remember to kill all Workers)', 'WARNING!!!',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.monitor.ClearQueue()
            self.monitor.ClearFinished()
            self.monitor.ClearCurrent()
            dial.Destroy()




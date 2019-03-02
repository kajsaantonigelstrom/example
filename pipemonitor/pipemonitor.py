# -*- coding: utf-8 -*-
import sys
import os
import uuid
import shutil
from time import sleep
import wx
from dialog_gentestdata import GenerateTestdataDialog
from dialog_genjobs import GenerateJobsDialog
from dialog_handlerecipes import HandleRecipesDialog

def deletefiles(dir):
    os.chdir(dir);
    l = filter(os.path.isfile, os.listdir(dir))
    for f in l:
        os.remove(dir+"/"+f)

class Monitor:
    def CheckConfig(self):
        # Open the main config file
        mconfigfilename = "pipemonitor.cfg"
        try:
            f = open(mconfigfilename,"r");
        except:
            estring = "Monitor Configuration file '"+mconfigfilename+"' not found"
            print estring
            return 0;

        # First line in pipemonitor.cfg is the Job folder
        self.jobfolder = f.readline().rstrip();
        self.recipefolder = f.readline().rstrip();
        self.braintopfolder = f.readline().rstrip();
        f.close()
        
        # Check that we can create files in the jobfolder
        filename = self.jobfolder+"/"+str(uuid.uuid4())
#        print filename
        try:
            f = open(filename, "w");
            f.write("hej")
            f.close()
            os.remove(filename);
        except:
            print "Not allowed to write in folder", self.jobfolder
            return 0
        
        # Check that we can read the recipefolder
        self.recipelist = os.listdir(self.recipefolder)
        try:
            self.recipelist = os.listdir(self.recipefolder)
        except:
            estring = "Cannot reach the folder '"+self.recipefolder+"'"
            print estring
            return 0

        return 1

    def CreateTestData(self, count):


        # remove current data
        shutil.rmtree(self.braintopfolder)
        try:
            shutil.rmtree(self.braintopfolder)
        except:
            pass
        # remove jobs in jobfolder
        deletefiles(self.jobfolder);
        deletefiles(self.jobfolder+"/current");
        deletefiles(self.jobfolder+"/finished");
        
        print "Creating ", count, "brains"
        os.mkdir(self.braintopfolder)
        for i in range(1,count+1):
            # Create a subject with a test image
            braindir = self.braintopfolder + "/Brain"+str(i)
            os.mkdir(braindir);
            os.chdir(braindir);

            f = open("test.image", "w");
            f.write("hej")
            f.close()

            # Create a corresponding job file
            jobfile = self.jobfolder+"/Brain"+str(i)+".txt"
            f = open(jobfile,"w")
            f.write(braindir);
            f.write("\n")
            frcp = open(self.recipefolder+"/Kajsa.rcp")
            while(1):
                rline = frcp.readline()
                if (rline == ""):
                    break;
                f.write(rline);
            frcp.close()
            f.close()
class MainWindow(wx.Panel):
    def __init__(self, parent, monitor):
        wx.Panel.__init__(self, parent)
        self.monitor = monitor

        menubar = wx.MenuBar()
        file = wx.Menu()
        functions = wx.Menu()        
        file.Append(101, '&quit', 'Quit')
        functions.Append(102, '&recipes', 'Handle Recipes');
        functions.Append(103, '&jobs', 'Generate Jobs');
        functions.Append(104, '&testdata', 'Generate Test Brains');

        menubar.Append(file, '&File')
        menubar.Append(functions, 'F&unctions')

        sizer = wx.GridBagSizer(6, 2)
        #sizer = wx.FlexGridSizer(6, 10)
        textinput = wx.StaticText(self, label="On-going jobs:")
        y=0; 
        sizer.Add(textinput, pos=(y, 0), flag=wx.ALIGN_LEFT, border=5)
        y=y+1
        currentjobs = ['2/5 Brain1 : fenix/worker', '4/5 Brain3 : fenix/worker'] 
        currlist = wx.ListBox(self, size = (100,-1), choices = currentjobs, style = wx.LB_SINGLE)        
        sizer.Add(currlist, pos=(y, 0), span=(0,2), flag=wx.EXPAND|wx.ALL, border=5)
        y=y+1;
        # List headers
        textinput = wx.StaticText(self, label="Job Queue:")
        sizer.Add(textinput, pos=(y, 0), flag=wx.ALIGN_LEFT, border=5)

        textinput = wx.StaticText(self, label="Finished:")
        sizer.Add(textinput, pos=(y, 1), flag=wx.ALIGN_LEFT, border=5)
        y=y+1

        # Job list and Finished list
        queuelist = wx.ListBox(self, size = (100,-1), style = wx.LB_SINGLE)        
        sizer.Add(queuelist, pos=(y, 0), flag=wx.EXPAND, border=5)

        finishedlist = wx.ListBox(self, size = (100,-1), style = wx.LB_SINGLE)        
        sizer.Add(finishedlist, pos=(y, 1), flag=wx.EXPAND, border=5)
        y = y +1
        # List buttons
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(self, label="Total:")
        j2 = wx.TextCtrl(self)
        j3 = wx.Button(self, label="Clear")#, pos=(200, 325))
        jobsizer.Add(j1, 1);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        sizer.Add(jobsizer, pos=(y, 0), border=5)
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(self, label="Total:")
        j2 = wx.TextCtrl(self)
        j3 = wx.Button(self, label="Clear")#, pos=(200, 325))
        jobsizer.Add(j1, 1);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        sizer.Add(jobsizer, pos=(y, 1), border=5)
        
        
        y=y+1

        # Job Folder
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        j1 = wx.StaticText(self, label="Job Folder")
        j2 = wx.TextCtrl(self)
        j3 = wx.Button(self, label="...")#, pos=(200, 325))
        jobsizer.Add(j1, 1);
        jobsizer.Add(j2, 3);
        jobsizer.Add(j3, 0);
        sizer.Add(jobsizer, pos=(y, 0), span=(0,2), border=5)

        y=y+1

        # Brains Folder
        brainsizer = wx.BoxSizer(wx.HORIZONTAL)
        b1 = wx.StaticText(self, label="Brains Folder")
        b2 = wx.TextCtrl(self)
        b3 = wx.Button(self, label="...")#, pos=(200, 325))
        brainsizer.Add(b1, 1);
        brainsizer.Add(b2, 3);
        brainsizer.Add(b3, 0);
        sizer.Add(brainsizer, pos=(y, 0), span=(0,2), border=5)
        

        parent.SetMenuBar(menubar)
        menubar.Bind(wx.EVT_MENU, self.menuhandler) 
        parent.SetTitle('Kajsas Pipe Monitor')

        self.SetSizer(sizer)
        sizer.Fit(parent)

        
#        self.Show(True);
        
    def menuhandler(self, event):
        print 111
        id = event.GetId();
        if (id == 101):
            sys.exit();
        elif id == 102:
            HandleRecipesDialog(self, "Handle Recipes").ShowModal();
        elif id == 103:
            GenerateJobsDialog(self, "Generate Jobs").ShowModal();
        elif id == 104:
            GenerateTestdataDialog(self, "Generate Test Brains", self.monitor).ShowModal();

    def SelectTestDataFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:    
            print 123
        else:
            print 234
def main():

    # Create the Monitor object
    monitor = Monitor()
    # Validate configuration
    if (not monitor.CheckConfig()):
        sys.exit();

    app = wx.App(False)
    frame = wx.Frame(None)
    panel = MainWindow(frame, monitor)
    frame.Show()
    app.MainLoop()    


if __name__ == '__main__':
    main()

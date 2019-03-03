﻿# -*- coding: utf-8 -*-
import sys
import os
import uuid
import shutil
from time import sleep
import wx
from mainwindow import MainWindow

def deletefiles(dir):
    os.chdir(dir);
    l = filter(os.path.isfile, os.listdir(dir))
    for f in l:
        os.remove(dir+"/"+f)

class Monitor:
    def __init__(self):
        self.currentjobs = []
        self.jobqueue = []
        self.finishedjobs = []
    def updatebrainstate(self):
        os.chdir(self.jobfolder)
        self.jobqueue = filter(os.path.isfile, os.listdir(self.jobfolder))
        os.chdir(self.jobfolder+'/current')
        self.currentjobs = filter(os.path.isfile, os.listdir(self.jobfolder+'/current'))
        os.chdir(self.jobfolder+'/finished')
        self.finishedjobs = filter(os.path.isfile, os.listdir(self.jobfolder+'/finished'))

    def CheckConfig(self):
        # Open the main config file
        mconfigfilename = "pipemonitor.cfg"
        try:
            f = open(mconfigfilename,"r");
        except:
            estring = "Monitor Configuration file '"+mconfigfilename+"' not found"
            print (estring)
            return 0;

        # First line in pipemonitor.cfg is the Job folder
        self.jobfolder = f.readline().rstrip();
        self.recipefolder = f.readline().rstrip();
        self.braintopfolder = f.readline().rstrip();
        f.close()
        
        # Check that we can create files in the jobfolder
        filename = self.jobfolder+"/"+str(uuid.uuid4())
#        print (filename)
        try:
            f = open(filename, "w");
            f.write("hej")
            f.close()
            os.remove(filename);
        except:
            print ("Not allowed to write in folder", self.jobfolder)
            return 0
        
        # Check that we can read the recipefolder
        self.recipelist = os.listdir(self.recipefolder)
        try:
            self.recipelist = os.listdir(self.recipefolder)
        except:
            estring = "Cannot reach the folder '"+self.recipefolder+"'"
            print (estring)
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
        
        print ("Creating ", count, "brains")
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

def main():

    # Create the Monitor object
    monitor = Monitor()
    # Validate configuration
    if (not monitor.CheckConfig()):
        sys.exit();

    app = wx.App(False)
    frame = MainWindow(None, monitor)
    frame.Show()
    app.MainLoop()    


if __name__ == '__main__':
    main()

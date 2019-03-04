# -*- coding: utf-8 -*-
import sys
import os
import uuid
import shutil
from time import sleep
import wx
from mainwindow import MainWindow

# delete files in a folder (not recursive);
# removes the folder if possible
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

    # Called periodically to check the state of jobs
    # Updates the lists that will be shown in the UI
    def updatebrainstate(self):
        os.chdir(self.jobfolder)
        self.jobqueue = filter(os.path.isfile, os.listdir(self.jobfolder))
        os.chdir(self.jobfolder+'/finished')
        self.finishedjobs = filter(os.path.isfile, os.listdir(self.jobfolder+'/finished'))
        # For the current jobs we want to present the .state file
        os.chdir(self.jobfolder+'/current')
        self.currentjobs = []
        jobfiles = filter(os.path.isfile, os.listdir(self.jobfolder+'/current'))
        for jobfile in jobfiles:
            try:
                f = open(jobfile,"r");
                self.brainfolder = f.readline().rstrip();
                f.close()
            except:
                print ("Error opening", jobfile)
                continue;
            statefilename = self.brainfolder+"/"+os.path.basename(self.brainfolder)+".state"
            try:
                f = open(statefilename,"r")
                self.currentjobs.append(f.readline().rstrip())
                f.close()
            except:
                estring = "Error opening " + statefilename
                self.currentjobs.append(estring)

    # Check access rights for folders to be used
    def CheckConfig(self):
        # Open the main config file
        self.startfolder = os.getcwd()
        self.mconfigfilename = "pipemonitor.cfg"
        try:
            f = open(self.mconfigfilename,"r");
        except:
            estring = "Monitor Configuration file '"+self.mconfigfilename+"' not found"
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

    # Re-writes the configuration file; used when the user changes
    # jobdir or brainsdir
    def writeCfgFile(self):
        os.chdir(self.startfolder)
        self.mconfigfilename = "pipemonitor.cfg"
        try:
            f = open(self.mconfigfilename,"w");
            f.write(self.jobfolder)
            f.write("\n");
            f.write(self.recipefolder)
            f.write("\n");
            f.write(self.braintopfolder)
            f.write("\n");
            f.close()
        except:
            estring = "Monitor Configuration file '"+mconfigfilename+"' not found"
            print (estring)
            return 0;

    ## Methods below here are entry points for the commands in the
    ## user interface
    def ClearFinished(self):
        deletefiles(self.jobfolder+"/finished");

    def ClearQueue(self):
        deletefiles(self.jobfolder);

    # Create one job file for each subfolder in the Brains folder
    # The job file:
    # line 1: The full path to the Brains subfolder
    # line 2-n: The lines in the Recipe
    def CreateJobs(self, recipe):
        recipe = self.CheckRecipeName(recipe)
        # remove jobs in jobfolder
        deletefiles(self.jobfolder);
        deletefiles(self.jobfolder+"/current");
        deletefiles(self.jobfolder+"/finished");
        recipestr = ""
        try:
            frcp = open(self.recipefolder+"/"+recipe, "r")
            recipestr = frcp.read();
            frcp.close()
        except:
            return "Cannot open the recipe ',"+recipe+"'"

        os.chdir(self.braintopfolder)
        brainlist = filter(os.path.isdir, os.listdir(self.braintopfolder))
        for brain in brainlist:
            # Create a corresponding job file
            jobfile = self.jobfolder+"/"+brain+".job"
            f = open(jobfile,"w")
            f.write(self.braintopfolder+"/"+brain);
            f.write("\n")
            f.write(recipestr)
            f.close()
        return ""

    # Utility for off-line testing: creates a number of test Brains
    # in the Brains folder
    def CreateTestData(self, count):

        # remove current data
        shutil.rmtree(self.braintopfolder)
        try:
            shutil.rmtree(self.braintopfolder)
        except:
            pass
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

    def SetBrainsFolder(self, dir):
        self.braintopfolder = dir
        self.writeCfgFile()

    def SetJobFolder(self, dir):
        self.jobfolder = dir
        try:
            os.mkdir(dir+"/current")
            os.mkdir(dir+"/finished")
        except:
            pass
        self.writeCfgFile()

    # Get recipe names; the API uses the Recipe name without the
    # extension (.rcp) that is used when storing them on disc
    def GetRecipeList(self):
        os.chdir(self.recipefolder)
        rdir = filter(os.path.isfile, os.listdir(self.recipefolder))
        for ix in range(0,len(rdir)):
            # mask away .rcp
            s = rdir[ix]
            s = s[:len(s)-4]
            rdir[ix] = s
        return rdir

    # Handle recipe extension: The API will work both if you use the
    # exension and if you don't
    def CheckRecipeName(self, recipename):
        pos = recipename.find('.rcp')
        if (pos < 0):
            recipename = recipename+".rcp"
        return recipename
        
    # Read a specific recipe
    def GetRecipe(self, recipename):
        recipename = self.CheckRecipeName(recipename)
        try:
            frcp = open(self.recipefolder+"/"+recipename, "r")
            recipe = frcp.read();
            recipe = recipe.encode('utf-8')
            frcp.close()
            return recipe
        except:
            return ""
        
    def DeleteRecipe(self, recipename):
        recipename = self.CheckRecipeName(recipename)
        recipename = self.recipefolder+"/"+recipename;
        os.remove(recipename);
        
    def RenameRecipe(self, recipename, newname):
        recipename = self.CheckRecipeName(recipename)
        newname = self.CheckRecipeName(newname)
        fromfile = self.recipefolder+"/"+recipename;
        to = self.recipefolder+"/"+newname;
        os.rename(fromfile, to);
        
    def WriteRecipe(self, recipename, recipe):
        recipename = self.CheckRecipeName(recipename)
        try:
            recipe = recipe.decode('utf-8')
            frcp = open(self.recipefolder+"/"+recipename, "w")
            frcp.write(recipe)
            frcp.close()
            return True
        except:
            return False
        return False
        
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

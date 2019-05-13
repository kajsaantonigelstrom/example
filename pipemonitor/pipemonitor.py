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
    l = list(filter(os.path.isfile, os.listdir(dir)))
    for f in l:
        os.remove(dir+"/"+f)

class BrainSelections:
    def __init__(self, braintopfolder):
        self.braintopfolder = braintopfolder
        self.startfolder = os.getcwd()
        self.initlist()

    def initlist(self):
        self.selection = []
        os.chdir(self.braintopfolder)
        self.choices = list(filter(os.path.isdir, os.listdir(self.braintopfolder)))
        for i in range(0, len(self.choices)):
            self.selection.append(True)

        #reset cwd
        os.chdir(self.startfolder)

        # check if there is a file already
        try:
            f = open("selectedbrains.txt", "r")
            index = 0
            while (True):
                line = f.readline().rstrip();
                if (line == ""):
                    break;
                s = True
                if (line[0] == "0"):
                    s = False
                c = line[2:]
                if len(self.choices) <= index or self.choices[index] != c:
                    raise BaseException("Not matching")
                self.selection[index] = s
                index = index + 1
            f.close()
            if index != len(self.selection):
                raise BaseException("Not matching")
        except:
            # list has changed; regenerate
            for i in range(0, len(self.choices)):
                self.selection[i] = True
            self.write()

    def write(self):
        try:
            saveddir =  os.getcwd()
            os.chdir(self.startfolder)
            f = open("selectedbrains.txt", "w")
            for i in range(0, len(self.choices)):
                s = "0"
                if (self.selection[i]):
                    s = "1"
                f.write(s+" "+self.choices[i]+"\n")
            f.close()
        except:
            print "Error writing 'selectedbrains.txt"
        os.chdir(saveddir)

    def braincount(self):
        return len(self.choices)

    def selectedcount(self):
        count = 0
        for i in range(0, len(self.choices)):
            if (self.selection[i]):
                count = count + 1
        return count


class Monitor:
    def __init__(self):
        self.currentjobs = []
        self.jobqueue = []
        self.finishedjobs = []
        self.deletelogfileflag = True

    def readstatestring(self, jobfile):
        try:
            f = open(jobfile,"r");
            self.brainfolder = f.readline().rstrip();
            f.close()
        except:
            return ""

        statefilename = self.brainfolder+"/"+os.path.basename(self.brainfolder)+".state"
        try:
            f = open(statefilename,"r")
            state = f.readline().rstrip()
            f.close()
            return state
        except:
            return ""
        
    # Called periodically to check the state of jobs
    # Updates the lists that will be shown in the UI
    def updatebrainstate(self):
        os.chdir(self.jobfolder)
        self.jobqueue = list(filter(os.path.isfile, os.listdir(self.jobfolder)))

        # For the finished jobs we want to present if the job went OK/Error
        os.chdir(self.jobfolder+'/finished')
        self.finishedjobs = list(filter(os.path.isfile, os.listdir(self.jobfolder+'/finished')))
        for ix in range(0,len(self.finishedjobs)):
            statestring = self.readstatestring(self.finishedjobs[ix])
            if (statestring==""):
                print("Cannot read state for "+self.finishedjobs[ix])
                continue
            if (statestring.find("ERROR") >= 0):
                self.finishedjobs[ix] = self.finishedjobs[ix] + " " + statestring

        # For the current jobs we want to present the .state file
        os.chdir(self.jobfolder+'/current')
        self.currentjobs = []
        jobfiles = list(filter(os.path.isfile, os.listdir(self.jobfolder+'/current')))
        for jobfile in jobfiles:
            statestring = self.readstatestring(jobfile)
            if (statestring == ""):
                continue;
            self.currentjobs.append(statestring)

    # Check access rights for folders to be used
    def CheckWritable(self, folder):
        filename = folder+"/"+str(uuid.uuid4())
        try:
            f = open(filename, "w");
            f.write("hej")
            f.close()
            os.remove(filename);
        except:
            return False
        return True

    def CheckConfig(self):
        # Open the main config file
        self.startfolder = os.getcwd()
        self.mconfigfilename = "pipemonitor.cfg"
        try:
            f = open(self.mconfigfilename,"r");
            # First line in pipemonitor.cfg is the Job folder
            self.mainconfigfile = f.readline().rstrip();
            self.recipefolder = f.readline().rstrip();
            f.close()
        except:
            self.errormessage = "Monitor Configuration file '"+self.mconfigfilename+"' not found"
            return False;
        
        # Read the main config file
        try:
            f = open(self.mainconfigfile,"r")
            self.jobfolder = f.readline().rstrip();
            self.braintopfolder = f.readline().rstrip();
            f.close()
        except:
            self.errormessage = "Main Configuration File '"+self.mainconfigfile+"' not found"
            return False;

        # Check that we can create files in the jobfolder
        # Check that we can create files in the jobfolder
        if (self.CheckWritable(self.jobfolder)==False):
            self.errormessage = "Not allowed to write in folder " + self.jobfolder
            return False
        # Check that we can write files in the brainsfolder
        if (self.CheckWritable(self.braintopfolder)==False):
            self.errormessage = "Not allowed to write in folder " + self.braintopfolder
            return False
        
        # Check that the Recipe Folder exists
        try:
            l = os.listdir(self.recipefolder)
        except:
            self.errormessage = "Recipe Folder '"+self.recipefolder+"' not found"
            return False;

        # Create 'current' and 'finished' in the jobfolder
        currentfolder = self.jobfolder+"/current"
        try:
            l = os.listdir(currentfolder)
        except:
            try:
                os.mkdir(currentfolder)
            except:
                self.errormessage = "Cannot create folder "+currentfolder
                return False
        finishedfolder  = self.jobfolder+"/finished"
        try:
            l = os.listdir(finishedfolder)
        except:
            try:
                os.mkdir(finishedfolder)
            except:
                self.errormessage = "Cannot create folder "+finishedfolder
                return False

        self.brainselections = BrainSelections(self.braintopfolder)
        return True

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

    def ClearCurrent(self):
        deletefiles(self.jobfolder + "/current");

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
        brainlist = self.brainselections.choices
        for ix in range(0, len(brainlist)):
            if (not self.brainselections.selection[ix]):
                continue
            brain = brainlist[ix]
            # Create a corresponding job file
            jobfile = self.jobfolder+"/"+brain+".job"
            f = open(jobfile,"w")
            deletestring = "0"
            if (self.deletelogfileflag):
                deletestring = "1"
            f.write(deletestring+" "+self.braintopfolder+"/"+brain);
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
        self.brainselections.initlist()

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
        rdir = list(filter(os.path.isfile, os.listdir(self.recipefolder)))
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
        except:
            pass
        try:
            frcp = open(self.recipefolder+"/"+recipename, "w")
            frcp.write(recipe)
            frcp.close()
            return True
        except:
            return False
        return False

    def GetSelections(self):
        return self.brainselections
        
def main():

    # Create the Monitor object
    monitor = Monitor()
    # Validate configuration
    if (not monitor.CheckConfig()):
        print ("The file 'pipemonitor.cfg' should have two lines:")
        print ("line 1: The full path and name of the Main Configuration File (see below)")
        print ("        Note that this file must be accessible from both Monitor and Workers")
        print ("line 2: The Recipe Folder where the job descriptions are located.")
        print ("        This folder may be local to the computer running the Monitor.")
        print ("        It is never used by the Workers.");
        print ("")
        print ("The Main Configuration File should have the following layout")
        print ("line 1: The Job Folder which will be used to communicate information about")
        print ("        jobs. This folder must be the same on every computer used. This can")
        print ("        be accomplished by using symbolic links on linux (the ln -s command) or")
        print ("        on Windows by selecting shared folders in a smart way.")
        print ("        NOTE: Each used computer MUST have write access to this folder and subfolders")
        print ("line 2: The Brains Folder (where the data for processing will be available")
        print ("        See the Job Folder above: same rules for naming and access")
        print ("")
        print ("******************************************************************")
        print (monitor.errormessage)
        print ("******************************************************************")
        sys.exit();

    app = wx.App(False)
    frame = MainWindow(None, monitor)
    frame.Show()
    app.MainLoop()    


if __name__ == '__main__':
    main()

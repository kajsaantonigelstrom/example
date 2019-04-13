# -*- coding: utf-8 -*-
# This file contains two classes
# The Worker which watches the job folder for new jobs to grab
# The PipeJob represents a job and performs the actual process
# handling: It spawns a process for each step in the 'recipe'
import sys
import os
import uuid
from time import sleep
import random
import subprocess
lastcallnewline = True
def consoleprint_cr(s):
    global lastcallnewline
    sys.stdout.write("\r")
    sys.stdout.write(s)
    sys.stdout.flush()
    lastcallnewline = False

def consoleprint_nl(s):
    global lastcallnewline
    if not lastcallnewline:
        print("\n")
    print (s)
    lastcallnewline = True

class PipeJobLauncher:
    def __init__(self, jobfile):
        self.running = True
        self.jobname = jobfile
        # create logfile where the pythonprocess pipejob will print
        self.logfilename = os.path.basename(jobfile)+".log"
        self.logfile = open(self.logfilename, "w");
    def start(self):
        args = []
        args.append("python")
        args.append("pipejob.py")
        args.append(self.jobname)
        if (os.name == 'nt'):
            self.process = subprocess.Popen(args, 0, None, None, self.logfile, shell=True)
        else:
            self.process = subprocess.Popen(args, 0, None, None, self.logfile)
        consoleprint_nl("job started "+self.jobname)
        return
        
    def poll(self):
        # poll the process
        self.returncode = self.process.poll()
        if (self.returncode == None):
            return
        self.logfile.close()
        self.running = False
        return

class Worker:
    def __init__(self):
        self.logfilestoremove = []
        self.logfilename = os.getcwd()+"/pipeworker.log"
        # Empty the logfile
        self.logfile = open(self.logfilename,'w')
        self.logfile.close()

        self.errormessage = ""
    def grabjob(self):
        # Find a jobfile and move it to 'current
        savedir = os.getcwd();
        os.chdir(self.jobfolder)
        joblist = list(filter(os.path.isfile, os.listdir(self.jobfolder)))
        os.chdir(savedir)
        for jobfile in joblist:
            fromfile = self.jobfolder + "/" + jobfile
            to = self.jobfolder + "/current/" + jobfile
            try:
                os.rename(fromfile, to)
                return to
            except:
                self.logmessage("Failed to move "+fromfile+" to "+tofile)
                pass
        return ""
        
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
        # Find the configuration file
        self.startfolder = os.getcwd()
        try:
            f = open("pipeworker.cfg", "r");
        except:
            self.errormessage = "Configuration file 'pipeworker.cfg' is missing"
            return False;
        # First line is the path to the Main Config file
        mconfigfilename = f.readline().rstrip();
        # Second line is a digit for number of max concurrent processes
        processes = f.readline().rstrip();
        f.close();
        # Open the main config file
        try:
            f = open(mconfigfilename,"r");
        except:
            self.errormessage = "Main Configuration file '"+mconfigfilename+"' not found"
            return False;

        # Main config file has jobfolder and brainsfolder
        self.jobfolder = f.readline().rstrip();
        self.braintopfolder = f.readline().rstrip();
        f.close()
        
        # Check that we can create files in the jobfolder
        if (self.CheckWritable(self.jobfolder)==False):
            self.errormessage = "Not allowed to write in folder " + self.jobfolder
            return False
        # Check that we can create files in the brainsfolder
        if (self.CheckWritable(self.braintopfolder)==False):
            self.errormessage = "Not allowed to write in folder " + self.braintopfolder
            return False
            
        self.concurrent = 1;
        if (processes!=""):
            try:
                self.concurrent = int(processes)
                self.errormessage = "Number of concurrent processes is set to " + str(self.concurrent)
            except:
                print ("'"+processes+"' is not a number (defines no of concurrent processes)")
                print ("Number of concurrent processes will default to " + str(self.concurrent))
        else:
            print ("Number of concurrent processes will default to " + str(self.concurrent))
        return 1

    def Run(self):
        running = [] # list of running 'pipejob'
        loopcount = 0
        jobcount = 0;
        while (1):
            prevjobcount = jobcount
            jobcount = len(running)
            if (jobcount == prevjobcount):
                consoleprint_cr("loop " + str(jobcount) + " : " + str(loopcount))
                loopcount = loopcount + 1
            else:
                consoleprint_nl("loop : " + str(len(running)))
            # First make sure all possible jobs has been started
            while (len(running) < self.concurrent):
                newjob = self.grabjob()
                if (newjob != ""):
                    jobobject = PipeJobLauncher(newjob)
                    jobobject.start();
                    self.logmessage("Job "+newjob+" started")
                    running.append(jobobject)
                else:
                    break;
            # check if any job is finished
            for x in running:
                x.poll()
                if (x.running == False):
                    # move the job file to 'finished'
                    fromfile = x.jobname
                    to = self.jobfolder + "/finished/" + os.path.basename(fromfile)
                    try:
                        os.rename(fromfile, to);
                    except:
                        self.logmessage("Failed to move "+fromfile+" to "+tofile);
                    if x.returncode == 0:
                        consoleprint_nl(x.jobname+" finished")
                    else:
                        consoleprint_nl("Error in "+x.jobname+", Check \"the brain's\" logfile")
                        
                    # print the output from pipejob.py
                    try:
                        self.logmessage("log from "+x.logfilename)
                        with open(x.logfilename, "r") as f:
                            self.logmessage(f.read());
                    except:
                        estring = "Error reading "+ x.logfilename;
                        print (estring)
                        self.logmessage(estring)
                    self.logfilestoremove.append(x.logfilename)
                    running.remove(x);
            sleep(1);
            self.removelogfiles()
            
    def logmessage(self, s):
        try:
            self.logfile = open(self.logfilename,'a')
        except:
            self.logfile = open(self.logfilename,'w')
        self.logfile.write(s+"\n")
        self.logfile.close()

    def removelogfiles(self):
        # unknown timing problem sometimes refuse to remove log file
        if len(self.logfilestoremove) == 0:
            return;
        for lf in self.logfilestoremove:
            self.logfilestoremove.remove(lf)
            try:
                os.remove(lf)
                self.logmessage(lf+" removed")
            except:
                # couldnt: add it again
                self.logfilestoremove.append(lf)
                self.logmessage(lf+" NOT removed")
            return; # remove only one per loop

def main():
    # Create a Worker object
    w = Worker()
    # Validate configuration
    if (not w.CheckConfig()):
        print ("The file 'pipeworker.cfg' should have two lines:")
        print ("line 1: The folder where the main configuration file 'pipeline.cfg' is located")
        print ("line 2: The number of allowed concurrent processes for this server")
        print ("")
        print ("The main configuration file should have the following layout")
        print ("line 1: The Job Folder which will be used to communicate information about")
        print ("        jobs. This folder must be the same on every computer used. This can")
        print ("        be accomplished by using symbolic links on linux (the ln -s command) or")
        print ("        on Windows by selecting shared folders in a smart way.")
        print ("        NOTE: Each used computer MUST have write access to this folder and subfolders")
        print ("line 2: The Brains Folder (where the data for processing will be available")
        print ("        See the Job Folder above: same rules for naming and access")
        print ("")
        print ("******************************************************************")
        print (w.errormessage)
        print ("******************************************************************")
        sys.exit();

    w.Run()
    
if __name__ == '__main__':
    main()

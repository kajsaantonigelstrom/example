# -*- coding: utf-8 -*-
import sys
import os
import uuid
from time import sleep
import random
import subprocess

class PipeJob:
    def __init__(self, jobfile):
        self.running = True
        self.jobname = jobfile
        self.c = random.randint(2,6);
        # Get the recipe
        f = open(jobfile,"r");
        self.jobfolder = f.readline().rstrip();
        self.logfilename = self.jobfolder+"/"+os.path.basename(self.jobfolder)+".log"
        self.command = []
        while(1):
            cmd = f.readline().rstrip()
            if cmd == "":
                break;
            self.command.append(cmd);
        self.currentstep = 0
        self.logfile = open(self.logfilename,'w')

    def start(self):
        self.currentcommand = self.command[self.currentstep]
        os.chdir(self.jobfolder)
        print self.jobfolder
        args = self.currentcommand.split()
        print os.path.basename(self.jobfolder), self.c, args
        if (os.name == 'nt'):
            self.process = subprocess.Popen(args, 0, None, None, self.logfile, shell=True)
        else:
            self.process = subprocess.Popen(args, 0, None, None, self.logfile)

        self.currentstep = self.currentstep + 1
        return

    def poll(self):
        # Check the delay
        if self.c > 0:
            self.c = self.c - 1;
        if self.c<=0:
            # poll the process
            self.returncode = self.process.poll()
            if (self.returncode == None):
                return
            self.logfile = open(self.logfilename,'a')
            self.logfile.write(self.currentcommand+" terminated with return code "+str(self.returncode)+"\n")
            # More commands
            if (len(self.command) <= self.currentstep):
                self.running = False
                self.logfile.close()
                return
            # Yes !
            self.c = random.randint(2,6);
            self.start()
class Worker:
    def grabjob(self):
        # Find a jobfile and move it to 'current
        os.chdir(self.jobfolder);
        joblist = filter(os.path.isfile, os.listdir(self.jobfolder))
        for jobfile in joblist:
            fromfile = self.jobfolder + "/" + jobfile
            to = self.jobfolder + "/current/" + jobfile
            try:
                os.rename(fromfile, to)
                return to
            except:
                pass
        return ""
        
    def CheckConfig(self):
        # Find the configuration file
        try:
            f = open("pipeworker.cfg", "r");
        except:
            print "Configuration file 'pipeworker.cfg' is missing"
            return 0;
        # First line is the path to the Monitor folder/main config
        mconfigfilename = f.readline().rstrip();
        # Second line is a digit for number of max concurrent processes
        processes = f.readline().rstrip();
        f.close();
        # Open the main config file
        try:
            f = open(mconfigfilename,"r");
        except:
            estring = "Monitor Configuration file '"+mconfigfilename+"' not found"
            print estring
            return 0;

        # First line in pipemonitor.cfg is the Job folder
        self.jobfolder = f.readline().rstrip();
#        self.recipefolder = f.readline().rstrip();
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
            print "Not allowed to write in folder", jobfolder
            return 0
        
        # Check that we can read the recipefolder
#        self.recipelist = os.listdir(self.recipefolder)
#        try:
#            self.recipelist = os.listdir(self.recipefolder)
#        except:
#            estring = "Cannot reach the folder '"+self.recipefolder+"'"
#            print estring
#            return 0

        self.concurrent = 1;
        if (processes!=""):
            try:
                self.concurrent = int(processes)
                print "Number of concurrent processes is set to", self.concurrent
            except:
                estring = "'"+processes+"' is not a number (defines no of concurrent processes)"
                print estring
                print "Number of concurrent processes will default to", self.concurrent
        else:
            print "Number of concurrent processes will default to", self.concurrent
        return 1

    def Run(self):
        running = [] # list of running 'pipejob'
        while (1):
            print "loop", len(running)
            # First make sure all possible jobs has been started
            while (len(running) < self.concurrent):
                newjob = self.grabjob()
                if (newjob != ""):
                    jobobject = PipeJob(newjob)
                    jobobject.start();
                    running.append(jobobject)
                else:
                    break;
            # check if any job is finished
            for x in running:
                x.poll()
                if (x.running == False):
                    running.remove(x);
                    print x.jobname, "finished"
                    fromfile = x.jobname
                    to = self.jobfolder + "/finished/" + os.path.basename(fromfile)
                    os.rename(fromfile, to);
            sleep(1);

def main():
    # Create a Worker object
    w = Worker()
    # Validate configuration
    if (not w.CheckConfig()):
        sys.exit();

    w.Run()
    
if __name__ == '__main__':
    main()


# -*- coding: utf-8 -*-
# This file contains two classes
# The Worker which watches the job folder for new jobs to grab
# The PipeJob represents a job and performs the actual process
# handling: It spawns a process for each step in the 'recipe'
import sys
import os
import ntpath
from time import sleep
import subprocess
import matlab.engine
import platform
import StringIO

lastcallnewline = True
class Dictionary:
    def __init__(self):
        self.mydict = {}
        self.errorstring = ""
        return
    def Translate(self, cmd):
        restofstring = cmd
        reply = ""
        pos=restofstring.find("%")
        if pos < 0:
            return cmd
        pos2 = -1
        while pos >= 0:
            if pos >= 0:
                reply = reply + restofstring[:pos]
            restofstring = restofstring[pos+1:]
            pos2 = restofstring.find("%")
            if pos2 < 0:    
                self.errorstring = "ERROR: Uneven number of '%' in "+cmd
                raise "Syntax error"
            keyword = restofstring[:pos2]
            try:
                reply = reply + self.mydict[keyword]
            except:
                self.errorstring = "ERROR: Cannot find replacement for "+keyword+ " in "+cmd
                raise "Syntax error"
                
            restofstring = restofstring[pos2+1:]

            pos=restofstring.find("%")
        print reply
        return reply

    def addDefine(self, define):
        param = define.split('=')
        if len(param) == 1:
            self.errorstring = "ERROR: Missing '=' in .DEFINE "+define
            raise "Syntax error"
        if len(param) > 2:
            self.errorstring = "ERROR: Too many '=' in .DEFINE "+define
            raise "Syntax error"

        self.mydict[param[0]] = param[1]
        print self.mydict
        return

class PipeJob:
    def __init__(self, jobfile):
        self.replacer = Dictionary()
        self.pendingerror = False
        
        self.myid = platform.node() # id of this computer
        self.running = True
        self.jobname = jobfile
        # Get the recipe
        f = open(jobfile,"r");
        self.brainfolder = f.readline().rstrip();
        self.logfilename = self.brainfolder+"/"+os.path.basename(self.brainfolder)+".log"
        self.logfilename_stdout = self.brainfolder+"/"+os.path.basename(self.brainfolder)+"_stdout.log"
        self.logfilename_stderr = self.brainfolder+"/"+os.path.basename(self.brainfolder)+"_stderr.log"
        self.statefilename = self.brainfolder+"/"+os.path.basename(self.brainfolder)+".state"
        self.brainname = os.path.basename(self.brainfolder);
        self.command = []
        self.matlabused = False
        self.replacer.addDefine("BRAIN="+os.path.basename(self.brainfolder))
        self.replacer.addDefine("BRAINFOLDER="+self.brainfolder)

        while(1):
            cmd = f.readline().rstrip()
            if cmd == "":
                break;
            if cmd[0]=="#":
                continue
            try:
                if cmd.find(".DEFINE") >= 0:
                    self.replacer.addDefine(cmd[8:])
                else:
                    self.command.append(self.replacer.Translate(cmd))
            except:
                print (self.replacer.errorstring)
                self.writestate(self.replacer.errorstring)
                sys.exit(-1)

            if cmd.find("MATLAB") >= 0:
                self.matlabused = True
        self.currentstep = 0
        self.matlabengine = None
        # open a fresh logfile
        self.logfile = open(self.logfilename,'w')
        self.logfile.close()
        print 153513
        print self.command

    def startmatlab(self, command):
        print "start matlab"
        scriptpath, scriptname = ntpath.split(command[1])
        parameterlist = []
        self.matlabreturnvariable = ""
        for i in range(2, len(command)):
            param = command[i].split('=')
            if len(param) != 2:
                print('syntax error: '+command[i])
            if param[0]=='RET':
                self.matlabreturnvariable = param[1]
            else:
                parameterlist.append(param)

        for i in range(0,len(parameterlist)):
            print(parameterlist[i][0] + " = " + parameterlist[i][1])
            self.matlabengine.workspace[parameterlist[i][0]] = parameterlist[i][1]

        self.matlabengine.chdir(self.brainfolder);
        if len(scriptpath) > 0:
            self.matlabengine.addpath(scriptpath)
        self.out = StringIO.StringIO()
        self.err = StringIO.StringIO()
        print ("Run MATLAB "+scriptname)
        self.future = self.matlabengine.run(scriptname, nargout=0, async=True, stdout=self.out,stderr=self.err)
        
    def writestate(self, str):
        f = open(self.statefilename, "w");
        f.write(str);
        f.close()
        
    def start(self):
        if self.matlabused and self.currentstep == 0:
            self.writestate("Starting the Matlab engine" + "    " + self.brainname + "    " + self.myid)
            print "Starting Matlab Engine"
            self.matlabengine = matlab.engine.start_matlab()
            print "Matlab Started"

        self.currentcommand = self.command[self.currentstep]
        args = self.currentcommand.split()

        self.writestate(str(self.currentstep+1)+"/"+str(len(self.command)) + " "+self.brainname + " " + self.myid + " '" + self.currentcommand +"'")

        self.matlabcommand = False
        self.logmessage("started " + self.currentcommand)
        os.chdir(self.brainfolder);
        print(self.brainfolder+" "+os.path.basename(self.brainfolder))
        print("before "+self.currentcommand)
        if (args[0] == "MATLAB"):
            self.matlabcommand = True
            self.startmatlab(args)
        else:
            # open the logfile for use in subprocess
            self.logfile_stdout = open(self.logfilename_stdout,'w')
            self.logfile_stderr = open(self.logfilename_stderr,'w')
            if (os.name == 'nt'):
                self.process = subprocess.Popen(args, 0, None, None, self.logfile_stdout, self.logfile_stderr, shell=True)
            else:
                self.process = subprocess.Popen(args, 0, None, None, self.logfile_stdout, self.logfile_stderr)
        print("after "+self.currentcommand)
        return

    def pollmatlab(self):
        isdone = self.future.done();
        if (isdone):
            try:
                result = self.future.result()
                outstr = self.out.getvalue()
                errstr = self.err.getvalue()
                
                self.logmessage("Output from MATLAB", False)
                self.logmessage(outstr, False)
                if len(errstr) > 0:
                    self.logmessage("Error from MATLAB")
                    self.logmessage(errstr, True)
                    self.pendingerror = True
                if (result == None):
                    self.logmessage("Result = None"); 
                else:
                    self.logmessage("Result = "+ str(result))
                if self.matlabreturnvariable != "":
                    self.logmessage("RET="+self.matlabengine.workspace[self.matlabreturnvariable])
                    return self.matlabengine.workspace[self.matlabreturnvariable]
                else:
                    self.logmessage("No return value from MATLAB");
                    return 'ready'
            except:
                self.logmessage("Exception from MATLAB")
                self.logmessage("Output from MATLAB")
                self.logmessage(self.out.getvalue())
                errstr = self.err.getvalue()
                if len(errstr) > 0:
                    self.logmessage("Error from MATLAB")
                    self.logmessage(errstr)
                return 'exception'
        return None

    def logmessage(self, s, doprint=True):
        self.logfile = open(self.logfilename,'a')
        self.logfile.write(s+"\n")
        self.logfile.close()
        if doprint:
            print s
        
    def poll(self):
            # poll the process
            if (self.matlabcommand):
                self.returncode = self.pollmatlab()
            else:
                self.returncode = self.process.poll()
                if self.returncode != 0:
                    self.pendingerror = True
                    
            if (self.returncode == None):
                return

            if (not self.matlabcommand):
                self.logfile_stdout.close() # close the logfile after use in subprocess
                self.logfile_stdout = open(self.logfilename_stdout,'r')
                l = self.logfile_stdout.read()
                self.logmessage(l)

                self.logfile_stderr.close() # close the logfile after use in subprocess
                self.logfile_stderr = open(self.logfilename_stderr,'r')
                l = self.logfile_stderr.read()
                if len(l) > 0:
                    self.logmessage("Error");
                    self.logmessage(l)

                self.logfile_stdout.close() # close the logfile after use in subprocess
                self.logfile_stdout.close() # close the logfile after use in subprocess
                try:
                    os.remove(self.logfilename_stdout)
                    os.remove(self.logfilename_stderr)
                except:
                    pass
            self.logmessage(self.currentcommand+" terminated with return code "+str(self.returncode))
    
            # More commands
            self.currentstep = self.currentstep + 1
            if (len(self.command) <= self.currentstep):
                self.running = False
                if (self.matlabengine != None):
                    self.matlabengine.quit()
                if self.pendingerror:
                    self.writestate("ERROR: possible error "+self.brainname + " " + self.myid + " Check logfile")
                else:
                    self.writestate("Finished "+self.brainname + " " + self.myid)

                return
            # Yes !
            self.start()

def main():
    if len(sys.argv) < 2:
        print ("syntax: pipejob jobfile")
        sys.exit(-1)
    jobfile = sys.argv[1]
    job = PipeJob(jobfile);
    job.start();
    while (job.running):
        job.poll();
        sleep(1)
    sys.exit(0)
    
if __name__ == '__main__':
    main()

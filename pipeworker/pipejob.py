
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
matlabinstalled = True
try:
    import matlab.engine
except:
    matlabinstalled = False
import platform
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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
                raise BaseException("Syntax error")
            keyword = restofstring[:pos2]
            try:
                reply = reply + self.mydict[keyword]
            except:
                self.errorstring = "ERROR: Cannot find replacement for "+keyword+ " in "+cmd
                raise BaseException("Syntax error")
                
            restofstring = restofstring[pos2+1:]

            pos=restofstring.find("%")
        print (reply)
        return reply

    def addDefine(self, define):
        param = define.split('=')
        if len(param) == 1:
            self.errorstring = "ERROR: Missing '=' in .DEFINE "+define
            raise BaseException("Syntax error")
        if len(param) > 2:
            self.errorstring = "ERROR: Too many '=' in .DEFINE "+define
            raise BaseException("Syntax error")

        self.mydict[param[0]] = param[1]
        return
    def printit(self):
        for x in self.mydict:
            print (x, "=", self.mydict[x])
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
        self.shellcommand = False
        self.matlabcommand = False
        self.process = None
        self.replacer.addDefine("BRAIN="+os.path.basename(self.brainfolder))
        self.replacer.addDefine("BRAINFOLDER="+self.brainfolder)
        for x in os.environ:
            try:
                self.replacer.addDefine(x+"="+os.environ[x])
            except:
                pass # More than one '=' in environment variable, just skip
        os.chdir(self.brainfolder);
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
        print (self.command)

    def startmatlab(self, command):
        print ("start matlab")
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
        global matlabinstalled
        if self.matlabused and self.currentstep == 0:
            if (not matlabinstalled):
                self.logmessage("MatLab needed but not installed")
                self.writestate("ERROR: MatLab needed but not installed")
                self.running = False
                return 'exception'
            self.writestate("Starting the Matlab engine" + "    " + self.brainname + "    " + self.myid)
            print ("Starting Matlab Engine")
            self.matlabengine = matlab.engine.start_matlab()
            print ("Matlab Started")
            self.matlabengine.chdir(self.brainfolder);
 
        self.currentcommand = self.command[self.currentstep]
        args = self.currentcommand.split()
        self.writestate(str(self.currentstep+1)+"/"+str(len(self.command)) + " "+self.brainname + " " + self.myid + " '" + self.currentcommand +"'")
        self.matlabcommand = False
        self.shellcommand = False
        self.logmessage("started " + self.currentcommand)
        print(self.brainfolder+" "+os.path.basename(self.brainfolder))
        print("before "+self.currentcommand)
        if (args[0] == "MATLAB"):
            self.matlabcommand = True
            self.startmatlab(args)
        elif args[0] == 'cd' or args[0] == 'export':
            self.shellcommand = True
            if (len(args) != 2):
                self.logmessage(args[0]+": syntax error")
                self.running = False
                return 'exception'
            if args[0] == 'cd':
                os.chdir(args[1])
            else: # export
                env = args[1].split('=')
                self.replacer.addDefine(args[1])
                if (len(env) != 2):
                    self.logmessage(args[0]+": syntax error")
                    self.running = False
                    return 'exception'
                os.environ[env[0]]=env[1]
        else:
            # open the logfile for use in subprocess
            self.logfile_stdout = open(self.logfilename_stdout,'w')
            self.logfile_stderr = open(self.logfilename_stderr,'w')
            if (os.name == 'nt'):
                self.process = subprocess.Popen(args, 0, None, None, self.logfile_stdout, self.logfile_stderr, cwd=os.getcwd(), env=os.environ, shell=True)
            else:
                self.process = subprocess.Popen(args, 0, None, None, self.logfile_stdout, self.logfile_stderr, cwd=os.getcwd(), env=os.environ)
        print("after "+self.currentcommand)
        return 0

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
            print (s)
        
    def poll(self):
            # poll the process
            if (self.shellcommand):
                self.returncode = 0
            elif (self.matlabcommand):
                self.returncode = self.pollmatlab()
            else:
                self.returncode = self.process.poll()
                if self.returncode != None and self.returncode != 0:
                    self.pendingerror = True
                    
            if (self.returncode == None):
                return

            if (not self.matlabcommand and not self.shellcommand):
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
            print(555)
            self.start()

def main():
    if len(sys.argv) < 2:
        print ("syntax: pipejob jobfile")
        sys.exit(-1)
    jobfile = sys.argv[1]
    job = PipeJob(jobfile);
    if (job.start() != 0):
        sys.exit(-1)
    while (job.running):
        job.poll();
        sleep(1)
#    job.replacer.printit()
    sys.exit(0)
    
if __name__ == '__main__':
    main()

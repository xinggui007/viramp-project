import subprocess, argparse
import os, re

def run_cmd(cmds, getval=True):
        DEVNULL = open(os.devnull, 'wb')
        p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=DEVNULL)
        out, err = p.communicate()
        if getval:
                return out
def purge(dir, pattern):
        for f in os.listdir(dir):
                if re.search(pattern, f):
                        try:
                                os.remove(os.path.join(dir,f))
                        except:
                                shutil.rmtree(os.path.join(dir,f))

def wrap():
	parser = argparse.ArugmentParser(description='BWA for mapping')	

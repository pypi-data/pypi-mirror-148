import sys
import time
from subprocess import Popen, PIPE 

def exec(command, forward=False, pipe=True, in_=""):
    '''
    Popen support with input,out and error support 
    
    Params:
    ---
    command: string     Command to execute.
    forward: bool       Doen't wait for command to complete.
    pipe: bool          If True runs command in backend, else truns command interactively.     
    in_: string         Stdin for PIPEd process call.
    '''
    if pipe:
        stdout, stdin, stderr = PIPE, PIPE, PIPE
    else:
        stdout = sys.stdout
        stdin = sys.stdin
        stderr = sys.stderr
    while True:
        p = Popen(command, shell=True, stdout=stdout, stderr=stderr, stdin=stdin)
        out, err = "", ""
        if not pipe:
            p.wait()
            return out, err
        if len(in_) > 0:
            out, err = p.communicate(input=in_.encode('utf-8'))
            out, err = out.decode('utf-8'), err.decode('utf-8')
            if "pip install" in out.lower():
                continue
            return out, err
        if not forward and len(in_) == 0:
            p.wait()
            out, err = p.stdout.read().decode('utf-8'), p.stderr.read().decode('utf-8')
            return out, err
        else:
            time.sleep(1)
            return "", ""
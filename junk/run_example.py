#! /usr/bin/env python
#PBS -S /bin/tcsh
"""
run_galacticus.py -- run-script for an example PBS job.

USAGE: ./run_example.py -arg1 <value> -arg2 <value>
                           
"""

import os,sys,subprocess,glob
import fnmatch
import datetime
import numpy as np
from hpyc.pbs import PBSjob

# Get basic environment variables
USER = os.environ['USER']

# Initialise job class to extract necessary environment variables
JOB = None
JOB = PBSjob(verbose=True)

if "JOB_MANAGER" in os.environ.keys():
    if os.environ['JOB_MANAGER'].upper() == "PBS":
        JOB = PBSjob(verbose=True)
    if os.environ['JOB_MANAGER'].upper() == "SLURM":
        JOB = SLURMjob(verbose=True)
else:
    if len(fnmatch.filter(os.environ.keys(),"PBS*"))>0:
        JOB = PBSjob(verbose=True)
    elif len(fnmatch.filter(os.environ.keys(),"SLURM*"))>0:
        JOB = SLURMjob(verbose=True)
    else:
        JOB = None
if JOB is None:
    JOB = NULLjob(verbose=True)

# Get interactive jobs have arguments
if JOB.interactive and len(sys.argv) == 1:
    print(__doc__)
    quit()

# Print the job name and ID
print("The name of this job is "+str(JOB.jobName)+" and the ID of the job is "+str(JOB.jobID)+".")
# Is this an interactive job? Print machine name.
if JOB.interactive:
    print("This job is interactive.")
    print("This job is hosted on "+str(JOB.machine)+".")
else:
    print("This job is not interactive.")
    print("This job was hosted on "+str(JOB.machine)+".")
# Is the job a job array
if JOB.jobArray:
    print("This job is a job array. The array ID is "+str(JOB.jobArrayID)+".")
    print("This particular task corresponds to index "+str(JOB.jobArrayIndex)+" of that job array.")
# Print queue and resources
print("This job was submitted to the queue "+str(JOB.queue)+" from the directory "+str(JOB.workDir)+".")
print("This job is running on "+str(JOB.nodes)+" nodes with a total of "+str(JOB.cpus)+" processors.")
print("This corresponds to "+str(JOB.ppn)+" processors per node.")
print("The walltime requested for this job is "+str(JOB.walltime)+".")


# Print arguments
EXAMPLE1 = None
EXAMPLE2 = None
if not JOB.interactive:    
    try:
        EXAMPLE1 = os.environ["EXAMPLE_ARGUMENT_1"]
    except KeyError:
        pass
    try:
        EXAMPLE2 = os.environ["EXAMPLE_ARGUMENT_2"]
    except KeyError:
        pass
else:
    iarg = 0
    while iarg < len(sys.argv):
        if fnmatch.fnmatch(sys.argv[iarg],"-arg1"):
            iarg += 1
            EXAMPLE1 = sys.argv[iarg]
        if fnmatch.fnmatch(sys.argv[iarg],"-arg2"):
            iarg += 1
            EXAMPLE2 = sys.argv[iarg]
        iarg += 1

print("Example argument 1 = "+str(EXAMPLE1))
print("Example argument 2 = "+str(EXAMPLE2))

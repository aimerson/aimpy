#! /usr/bin/env python

import sys,os,getpass,fnmatch,subprocess,glob
import numpy as np
import datetime
from batchJobs import submitPBS


# Example 1. Submit a job array to queue 'mediumq' with indices 1-5.
ARRAY = "1-5"
QUEUE = "mediumq"

# Initialise PBS class
SUBMIT = submitPBS(overwrite=True)

# Set job array
SUBMIT.specifyJobArray(ARRAY)


# Set job name
JOBNAME = "exampleJob1"
SUBMIT.addJobName(JOBNAME)

# Set PBS queue

SUBMIT.addQueue(QUEUE)

# Create logs directory
LOGDIR = "./Logs/pbsExample/"
subprocess.call(["mkdir","-p",LOGDIR])        
SUBMIT.addOutputPath(LOGDIR)
SUBMIT.addErrorPath(LOGDIR)
SUBMIT.joinOutErr()

# Two example arguements to pass to the job
ARGS = {"EXAMPLE_ARGUMENT_1":"helloWorld"}
ARGS["EXAMPLE_ARGUMENT_2"] = 3.14159
SUBMIT.passScriptArguments(ARGS)

# Set the 
SUBMIT.setScript("run_example.py")

# Print command
SUBMIT.printJobString()
# Submit job
print("Submitting example job...")
SUBMIT.submitJob()









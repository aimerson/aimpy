#! /usr/bin/env python

import sys,os,getpass,fnmatch,subprocess,glob
import numpy as np
import datetime
from batchJobs import submitPBS


# Example 1. Submit a job to queue 'shortq' requesting 1 node with 2 processors.
RESOURCE = "select=1:ncpus=2"

# Initialise PBS class
SUBMIT = submitPBS(overwrite=True)

# Set job name
JOBNAME = "exampleJob2"
SUBMIT.addJobName(JOBNAME)

# Set resource
SUBMIT.addResource(RESOURCE)

# Set PBS queue
QUEUE = "shortq"
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









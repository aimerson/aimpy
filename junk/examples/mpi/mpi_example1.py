#! /usr/bin/env python


import numpy as np
from mpi4py import MPI


def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)



# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')
# Initializations and preliminaries
comm = MPI.COMM_WORLD # get MPI communicator object
size = comm.size # total number of processes
rank = comm.rank # rank of this process
print size,rank
status = MPI.Status() # get MPI status object

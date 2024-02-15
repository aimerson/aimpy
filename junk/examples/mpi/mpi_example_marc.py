#!/usr/bin/env python

"""Demonstrate the task-pull paradigm for high-throughput computing
using mpi4py. Task pull is an efficient way to perform a large number of
independent tasks when there are more tasks than processors, especially
when the run times vary for each task.
This code is over-commented for instructional purposes.
This example was contributed by Craig Finch (cfinch@ieee.org).
Inspired by http://math.acadiau.ca/ACMMaC/Rmpi/index.html
"""

import glob
import numpy as np
from mpi4py import MPI
def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
#---------------------------------------------------
# Define MPI message tags
tags = enum('READY', 'DONE', 'EXIT', 'START')
# Initializations and preliminaries
comm = MPI.COMM_WORLD # get MPI communicator object
size = comm.size # total number of processes
rank = comm.rank # rank of this process
status = MPI.Status() # get MPI status object
#---------------------------------------------------


def read_halo_binary_file(ifile):
    f = open(ifile,"rb")
    d = f.read(4)
    nread = struct.unpack('i', f.read(4))[0]
    d = f.read(8)
    data = np.fromfile(f,'<f4')
    data = data[:-1]
    data = data.reshape(-1,13)
    names = "NP, X, Y, Z, VX, VY, VZ, SXX, SYY, SZZ, SXY, SXZ, SYZ"
    formats = "i4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4, f4"
    return np.core.records.fromarrays(data.transpose(),\
                                      names=names,formats=formats)
                                    



mbins = np.arange(12.0,15.0,0.2)
MPART = 1.099e10


if rank == 0:
    # Master process executes code below
    files = glob.glob("/my/dir/with/bin/files/in/it/*.dat")
    result = None
    tasks = np.arange(size*2)
    task_index = 0
    num_workers = size - 1
    closed_workers = 0
    hmf_global = None
    print("Master starting with %d workers" % num_workers)
    while closed_workers < num_workers:
        result = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == tags.READY:
            # Worker is ready, so send it a task (i.e. give it a file to read)
            if task_index < len(files):
                binfile = files[task_index]
                comm.send(binfile, dest=source, tag=tags.START)
                print("Sending task %d to worker %d" % (task_index, source))
                task_index += 1
            else:
                comm.send(None, dest=source, tag=tags.EXIT)
        elif tag == tags.DONE:
            if hmf_global is None:
                hmf_global = np.copy(result)
            else:
                hmf_global += np.copy(result)
            print("Got data from worker %d" % source)
        elif tag == tags.EXIT:
            print("Worker %d exited." % source)
            closed_workers += 1
    print result

    print len(result["a"])
    print("Master finishing")
else:
    # Worker processes execute code below
    name = MPI.Get_processor_name()
    print("I am a worker with rank %d on %s." % (rank, name))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        binfile = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        #print "%d"%rank,task
        tag = status.Get_tag()
        if tag == tags.START:
            # Read binary file
            data = read_halo_binary_file(binfile)
            # Construct HMF
            #hmf = np.zeros_like(data.NP)
            bw = mbins[1] - mbins[0]
            wgts = np.ones_like(data.X)/bw
            hmf,bins = np.histogram(data.NP*MPART,bins=mbins,weights=wgts)
            comm.send(hmf, dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            break
    comm.send(None, dest=0, tag=tags.EXIT)

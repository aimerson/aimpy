#! /usr/bin/env python


import sys
import h5py
import numpy as np




def check_readonly(func):
    def wrapper(self,*args,**kwargs):               
        funcname = self.__class__.__name__+"."+func.__name__
        if self.read_only:
            raise IOError(funcname+"(): HDF5 file "+self.filename+" is READ ONLY!")        
        return func(self,*args,**kwargs)
    return wrapper



class HDF5(object):
   
    def __init__(self,*args):
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        self.unit = h5py.File(*args)
        self.filename = self.unit.filename
        if self.unit.mode == "r":
            self.read_only = True
        elif self.unit.mode == "r+":
            self.read_only = False
        return
    
    def close(self):
        self.unit.close()
        return

    ##############################################################################
    # GROUPS
    ##############################################################################
    
    @check_readonly
    def mkdir(self,hdfdir):        
        """
        HDF5.mkdir(): create HDF5 group with specified path.
        
        USAGE:  HDF5.mkdir(dir)

              Input: dir -- path to HDF5 group.       
        """
        if hdfdir not in self.unit:
            g = self.unit.create_group(hdfdir)
        return

    
    @check_readonly
    def rmdir(self,hdfdir):
        """
        HDF5.mkdir(): remove HDF5 group at specified path.
        
        USAGE:  HDF5.rmdir(dir)

              Input: dir -- path to HDF5 group.       
        """
        if hdfdir in self.unit:
            del self.unit[hdfdir]
        return


    @check_readonly
    def cpdir(self,srcfile,srcdir,dstdir=None):        
        """
        HDF5.cpdir(): copy HDF5 group with specified path from specified file.
        
        USAGE:  HDF5.cpdir(srcfile,srcdir,[dstdir])

              Input: srcfile -- Path to source HDF5 file.       
                     srcdir -- Path to source HDF5 group inside source file.
                     dstdir -- Path to group to store copy of source group. 
                               Default = srcdir.

              Note that this function will create in the current file a parent 
              group with the same path as the parent group of the source group
              in the source file.
                                              
        """
        # Open second file and get path to group that we want to copy
        unit = h5py.File(srcfile,"r")        
        group_path = unit[srcdir].parent.name
        # Create same parent group in current file
        group_id = self.unit.require_group(group_path)
        # Set name of new group
        if dstdir is None:
            dstdir = srcdir
        unit.copy(srcdir,group_id,name=dstdir)
        unit.close()   
        return


    ##############################################################################
    # DATASETS
    ##############################################################################
    
    @check_readonly
    def add_dataset(self,hdfdir,name,data,append=False,overwrite=False,\
                        maxshape=tuple([None]),chunks=True,compression="gzip",\
                        compression_opts=6,**kwargs):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        # Select HDF5 group
        if hdfdir not in self.unit.keys():
            self.mkdir(hdfdir)
        g = self.unit[hdfdir]
        # Write data to group
        value = np.copy(data)
        if name in g.keys():
            write_key = False
            if append:
                value = np.append(np.copy(g[name]),value)
                del g[name]
                write_key = True
            if overwrite:
                del g[name]
                write_key = True
        else:
            write_key = True
        if write_key:                
            dset = g.create_dataset(name,data=value,maxshape=maxshape,\
                                        chunks=chunks,compression=compression,\
                                        compression_opts=compression_opts,**kwargs)
        del value            
        return

    @check_readonly
    def add_datasets(self,hdfdir,data,append=False,overwrite=False,\
                        maxshape=tuple([None]),chunks=True,compression="gzip",\
                        compression_opts=6,**kwargs):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        # Select HDF5 group
        if hdfdir not in self.unit.keys():
            self.mkdir(hdfdir)
        g = self.unit[hdfdir]
        # Write data to group
        for n in data.dtype.names:
            value = data[n]
            if n in g.keys():
                write_key = False
                if append:
                    value = np.append(np.copy(g[n]),value)
                    del g[n]
                    write_key = True
                if overwrite:
                    del g[n]
                    write_key = True
            else:
                write_key = True
            if write_key:                
                dset = g.create_dataset(n,data=value,maxshape=maxshape,\
                                            chunks=chunks,compression=compression,\
                                            compression_opts=compression_opts,**kwargs)
            del value            
        return

#! /usr/bin/env python

import numpy as np
from aimpy.fileFormats.hdf5 import HDF5


# Create file called 'example.hdf5' and open new HDF5 instance
fname = "example.hdf5"
F = HDF5(fname,'w') 

# Make some example HDF5 directories (make recursively)
F.mkGroup("base/randomNumbers")
# Write some example attributes
F.addAttributes("base",{"exampleAttribute":"helloWorld"})
# Generate some example data and write the dataset to the file.
seed = 1000
np.random.seed(seed)
r = np.random.rand(50)
F.addDataset("base/randomNumbers","numbers",r)
# Write the random seed as an attribute of the dataset
F.addAttributes("base/randomNumbers/numbers",{"seed":seed})
# Close the file
F.fileObj.close()

# Re-open the file in READ-ONLY mode
F = HDF5(fname,'r')
# Print all of the groups found in the upper directory
print(F.lsGroups("/"))
# Read attributes in 'base' directory into dictionary
attrib = F.readAttributes("base")
print attrib
# Can specify list of select attributes to read
attrib = F.readAttributes("base",required=["exampleAttribute"])
print attrib
# Print list of groups in 'base' sub-directory
print(F.lsGroups("base"))
# Print list of datasets found in 'randomNumbers' sub-directory.
print(F.lsDatasets("base/randomNumbers"))
# Extract into a dictionary all of the datsets in the 'randomNumbers' sub-directory.
data = F.readDatasets("base/randomNumbers/")
print data
# Extract as a numpy array just the 'numbers' dataset.
data = F.readDatasets("base/randomNumbers/numbers")
print data
# Close the file
F.fileObj.close()

# Open the file in 'append' mode.
F = HDF5(fname,'a')
# Generate some more random numbers and append them to the existing 'numbers' dataset
s = np.random.rand(50)
F.addDataset("base/randomNumbers","numbers",s,append=True)
# Create a second dataset of numbers
s = np.random.rand(50)
F.addDataset("base/randomNumbers","moreNumbers",s)
# Extract subdirectory as HDF object
NUM = F.fileObj["base/randomNumbers"]
# Extract example numbers as a numpy array
data = np.array(NUM["moreNumbers"])
print data
# Close file
F.fileObj.close()










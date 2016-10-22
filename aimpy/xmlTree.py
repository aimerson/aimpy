#! /usr/bin/env python

import os,sys
import numpy as np
import xml.etree.ElementTree as ET

def formatFile(ifile,ofile=None):
    import shutil
    tmpfile = ifile.replace(".xml","_copy.xml")
    if ofile is not None:
        cmd = "xmllint --format "+ifile+" > "+ofile
    else:
        cmd = "xmllint --format "+ifile+" > "+tmpfile
    os.system(cmd)
    if ofile is None:
        shutil.move(tmpfile,ifile)
    return


class xmlTree(object):
    
    def __init__(self,xmlfile=None,root="root",verbose=False):
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        self._verbose = verbose
        self.xmlfile = xmlfile         
        if self.xmlfile is None:
            root = ET.Element("root")
            self.tree = ET.ElementTree(element=root)
        else:
            self.tree = ET.parse(self.xmlfile)
        self.root = self.tree.getroot()        
        self.treeMap = {}
        if self._verbose:
            print(classname+"(): Root is '"+self.root.tag+"'")            
        return
        
    def getElement(self,path):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        nodes = path.split("/")     
        if len(nodes) == 1:
            elem = self.root
        else:
            node = nodes.pop()
            elem = self.getElement("/".join(nodes)).find(node)                        
        return elem

    def createElement(self,name,attrib={},parent=None):        
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        if parent is None or parent==self.root.tag:
            path = self.root.tag
            parent = self.root
        else:
            path = self.treeMap[parent]
            parent = self.getElement(path)
        ET.SubElement(parent,name,attrib=attrib)
        self.treeMap[name] = path+"/"+name
        return
    
    def appendElement(self,newBranch,parent=None):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name
        if parent is None:
            parent = self.root
        if parent.endswith("/"):
            parent = parent[:-1]
        nodes = parent.split("/")
        if nodes[0] == self.root.tag:
            nodes = nodes[1:]
        parentNode = self.root
        for nodeName in nodes:
            node = parentNode.find(nodeName)
            if node is None:
                self.createBranch(nodeName,parent=parentNode.tag)
            else:
                parentNode = node
        node.append(newBranch)
        return
                       
    def writeToFile(self,outFile,format=True):
        self.tree.write(outFile)
        if format:
            formatFile(outFile)
        return


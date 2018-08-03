#! /usr/bin/env python

import os,sys,fnmatch
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

    def __init__(self,root="root",file=None):        
        classname = self.__class__.__name__
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        ROOT = ET.Element(root)            
        self.tree = ET.ElementTree(element=ROOT,file=file)
        self.map = None
        return

    def loadFromFile(self,xmlfile):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        self.tree = ET.parse(xmlfile)
        self.mapTree()
        return

    def lsElements(self,OBJ):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        result = None
        if type(OBJ) is ET.ElementTree:
            result = OBJ.findall(".")
        elif type(OBJ) is ET.Element:
            result = list(OBJ)
        else:
            raise TypeError("Object is not an ElementTree or an Element!")
        return result
        
    def mapTree(self):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        self.map = ["/"]
        path = ""
        dummy = [self.addElementToMap(E,path=path) for E in self.lsElements(self.tree)]
        return 

    def addElementToMap(self,ELEM,path="/"):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        if self.lsElements(ELEM) > 0:
            dummy = [self.addElementToMap(E,path=path+"/"+ELEM.tag) for E in self.lsElements(ELEM)]
        self.map.append(path+"/"+ELEM.tag)
        return
    
    def matchPath(self,path):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        if self.map is None:
            self.mapTree()
        return fnmatch.filter(self.map,path)        
        
    
    def getElementAttribute(self,path,attrib=None):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        OBJ = self.getElement(path)
        value = None
        if attrib is None:
            return OBJ.attrib
        if attrib in OBJ.attrib.keys():
            value = OBJ.attrib[attrib]
        return value


    def getElement(self,querypath):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        matches = self.matchPath(querypath)
        if len(matches)==0:
            return None
        if len(matches) > 1:
            msg = "Multiple matches found!"
            msg = "/n   "+"/n   ".join(matches)
            raise ValueError(msg)
        path = matches[0]
        ROOT = self.tree.getroot()
        path = path.replace("/"+ROOT.tag,"")
        OBJ = ROOT
        levels = path.split("/")[1:]
        if len(levels) > 0:
            for dir in levels:
                OBJ = OBJ.find(dir)
        return OBJ


    def createElement(self,path,name,attrib={},buildIfMissing=True):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        matches = self.matchPath(path)
        if len(matches) > 1:
            raise ValueError("Multiple path options found!")
        if len(matches) == 0:
            if buildIfMissing:          
                parentPath = "/".join(path.split("/")[:-1])
                if parentPath == "":
                    parentPath = "/"
                parentName = path.split("/")[-1]
                self.createElement(parentPath,parentName)
        PARENT = self.getElement(path)
        ET.SubElement(PARENT,name,attrib=attrib)
        self.map.append(path+"/"+name)
        return

    def updateElement(self,path,attrib={}):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        matches = self.matchPath(path)        
        if len(matches) == 0:
            parentPath = "/".join(path.split("/")[:-1])
            if parentPath == "":
                parentPath = "/"
            parentName = path.split("/")[-1]
            self.createElement(parentPath,parentName)
        ELEM = self.getElement(path)
        for key in attrib.keys():
            if key in ELEM.attrib.keys():
                ELEM.attrib[key] = attrib[key]
        return
        
    def writeToFile(self,outFile,format=True):
        self.tree.write(outFile)
        if format:
            formatFile(outFile)
        return

        





class oldtree(object):

    
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

    def createElement(self,name,attrib={},parent=None,text=None,overwrite=False):        
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        if name in self.treeMap.keys() and not overwrite:
            return
        if name in self.treeMap.keys() and overwrite:
            elem = getElement(self.treeMap[name]).clear
        if parent is None or parent==self.root.tag:
            path = self.root.tag
            parent = self.root
        else:
            path = self.treeMap[parent]
            parent = self.getElement(path)
        if parent is None:
            raise ValueError(funcname+"(): error in path to parent element -- some nodes missing?"+\
                                 "    \nParent path = "+path)        
        if text is None:
            ET.SubElement(parent,name,attrib=attrib)
        else:
            ET.SubElement(parent,name,attrib=attrib).text = str(text)
        self.treeMap[name] = path+"/"+name
        return
    
    def setElement(self,name,attrib={},text=None,parent=None,selfCreate=False):
        funcname = self.__class__.__name__+"."+sys._getframe().f_code.co_name        
        if name not in self.treeMap.keys():
            if selfCreate:
                self.createElement(name,attrib=attrib,parent=parent,text=text)
            else:
                raise KeyError(funcname+"(): element does not exist!")
        elem = self.getElement(self.treeMap[name])
        dummy = [elem.set(k,attrib[k]) for k in attrib.keys()]
        del dummy
        if text is not None:
            elem.text = text
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
                self.createElement(nodeName,parent=parentNode.tag)
            else:
                parentNode = node
        node.append(newBranch)
        return
                       

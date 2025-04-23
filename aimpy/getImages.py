#! /usr/bin/env python

import os
import glob
import json
import re
import urllib
import random
from urllib import request
from bs4 import BeautifulSoup
from .utils.progress import Progress


def getFile(url,ofile):
    request.urlretrieve(url,ofile)
    return

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'


class Downloader(object):

    def __init__(self,urlbase,verbose=False):
        self.base = urlbase
        self.verbose = verbose
        return

    @classmethod
    def iterate_filename(cls,filename):
        i = 1
        while i is not None:
            fname = filename.replace(".jpg","-"+str(i)+".jpg")
            if os.path.exists(fname):
                i += 1
            else:
                i = None
        return fname

    @classmethod
    def get_hrefs(cls,url):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        #print(url)
        REQ = request.Request(url,headers=headers)
        website = request.urlopen(REQ)
        html = website.read()
        #print(html)
        soup = BeautifulSoup(html,features="lxml")
        return [str(link.get("href")) for link in soup.findAll("a")] 


    @classmethod
    def get_pids(cls,url):
        #user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}
        REQ = request.Request(url,headers=headers)
        website = request.urlopen(REQ)        
        html = website.read()
        soup = BeautifulSoup(html,features="lxml")
        pids = []
        for link in soup.findAll("a"):
            href = str(link.get("href"))
            if href.startswith("displayimage"):
                pids.append(href.split("#")[0])            
        return pids


    @classmethod
    def count_pages(cls,url):
        hrefs = cls.get_hrefs(url)
        maxpage = 1
        for href in hrefs:
            if "page" in str(href):
                pg = int(href.split("page=")[-1])
                maxpage = max(maxpage,pg)
        return maxpage
    

    @classmethod
    def get_pids_in_album(cls,url):
        maxpage = cls.count_pages(url)
        allpids = []
        for pg in range(maxpage):
            pgurl = url+"&page="+str(pg+1)
            allpids += cls.get_pids(pgurl)
        return allpids


    def sample_album(self,albumID,outdir,sample=0.01):
        os.makedirs(outdir,exist_ok=True)
        url = self.base+"thumbnails.php?album="+str(albumID)
        allpids = self.get_pids_in_album(url)
        n = int(len(allpids)*sample)
        n = max(n,1)
        pids = random.sample(allpids,n)
        self.get_album(albumID,outdir,pids=pids)
        return


    def get_album(self,albumID,outdir,pids=None,skipIfFound=False):
        os.makedirs(outdir,exist_ok=True)
        url = self.base+"thumbnails.php?album="+str(albumID)
        urlframe = self.base+"displayimage.php?pid={0}&fullsize=1"
        if pids is None:
            print("Getting image IDs...")
            allpids = self.get_pids_in_album(url)
        else:
            allpids = ["displayimage.php?pid="+str(pid) for pid in pids]
        print("Downloading images from album "+str(albumID)+"...")
        PROGRESS = Progress(len(allpids))
        for pid in allpids:
            pidStr = pid.split("pid=")[-1]
            if os.path.exists(outdir+pidStr+".*") and skipIfFound:
                continue
            urlframe = self.base+pid+"&fullsize=1"
            if self.verbose:
                print(urlframe)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                REQ = request.Request(urlframe,headers=headers)
                website = request.urlopen(REQ)        
                html = website.read()
                pat = re.compile (rb'<img [^>]*src="([^"]+.jpg)')
                img = pat.findall(html)[0].decode('ascii')
                newurl = self.base+img
                filefmt = newurl.split(".")[-1]
                filename = pidStr+"."+filefmt
                ofile = outdir+filename
                if not os.path.exists(ofile):
                    request.urlretrieve(newurl,ofile)
            except IndexError:
                continue
            PROGRESS.increment()
            PROGRESS.print_status_bar()
        return

    @classmethod
    def iterate_filename(cls,filename):
        i = 1
        while i is not None:
            fname = filename.replace(".jpg","-"+str(i)+".jpg")
            if os.path.exists(fname):
                i += 1
            else:
                i = None
        return fname


    def get_images(self,pids,outdir,overwrite=False):
        os.makedirs(outdir,exist_ok=True)
        allpids = ["displayimage.php?pid="+str(pid) for pid in pids]
        print("Downloading images...")
        PROGRESS = Progress(len(allpids))
        for pid in pids:
            urlframe = self.base+"displayimage.php?pid="+str(pid)+"&fullsize=1"
            if self.verbose:
                print(urlframe)
            website = request.urlopen(urlframe)
            html = website.read()
            pat = re.compile (rb'<img [^>]*src="([^"]+.jpg)')
            try:
                img = pat.findall(html)[0].decode('ascii')
                newurl = self.base+img
                ofile = outdir+str(pid)+".jpg"
                if not overwrite:
                    ofile = self.iterate_filename(ofile)
                try:
                    opener = request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    request.install_opener(opener)
                    request.urlretrieve(newurl,ofile)
                except urllib.error.HTTPError:
                    print(pid,urlframe)
            except IndexError:
                print("pid="+str(pid))
            PROGRESS.increment()
            PROGRESS.print_status_line()
        return


class Gallery(Downloader):

    def __init__(self,name,url,outdir=None,verbose=False):
        self.name = name
        self.url = url
        if outdir is None:            
            self.outdir = "gallery/"+self.name+"/"
        else:
            if not outdir.endswith("/"):
                outdir = outdir + "/"
            self.outdir = outdir
        os.makedirs(self.outdir,exist_ok=True)
        super().__init__(self.url,verbose=verbose)
        return

    def getAlbums(self,albums,skipIfFound=False):
        for albumID in list(albums.keys()):
            pids = albums[albumID]
            outdir = self.outdir+str(albumID)+"/"
            self.get_album(str(albumID),outdir,pids=pids,skipIfFound=skipIfFound)
        return

    def sampleAlbums(self,albumIDs,sample=0.01):
        for albumID in albumIDs:
            outdir = self.outdir+"/"+str(albumID)+"/"
            self.sample_album(albumID,outdir,sample=sample)
        return


    def listFiles(self,albumID,fileExtensions=True):
        outdir = self.outdir+"/"+str(albumID)+"/"
        files = os.listdir(outdir)
        files.sort()
        if not fileExtensions:
            for i in range(len(files)):
                f = files[i]
                j = f.rfind(".")
                files[i] = f[:j]
        return files
                
    

def get_pids_from_filenames(dir,fmt="jpg"):
    if not dir.endswith("/"):
        dir = dir + "/"
    files = glob.glob(dir+"*."+fmt)
    pids = [int(f.split("/")[-1].replace("."+fmt,"")) for f in files]
    return pids


class JsonImages(object):

    def __init__(self,jsonfile):
        self.file = jsonfile
        return

    
    def write(self,new_data):
        if type(new_data) != list:
            new_data = [new_data]
        if os.path.exists(self.file):
            with open(self.file,'r+') as file:
                file_data = json.load(file)
                file_data += new_data
                file.seek(0)
                json.dump(file_data,file)
        else:
            with open(self.file,'w') as file:
                json.dump(new_data,file)
        return

    def downloadImages(self,path,overwrite=False):
        with open(self.file) as inp:
            data = json.load(inp)[0]
        for imgset in data.keys():
            name = imgset
            outdir = path +"/"+name+"/"
            urlbase = data[name]["url"]
            GAL = GalleryGrab(urlbase)
            albums = list(data[name].keys())
            albums.remove("url")
            for albID in albums:
                albdir = outdir+str(albID)+"/"                
                pids = data[name][albID]
                GAL.get_images(pids,albdir,overwrite=overwrite)
        return

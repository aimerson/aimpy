#! /usr/bin/env python


import copy
import re

class SigFig(object):

    @classmethod
    def frexp10(cls,x):
        exp = int(math.log10(x))
        return x / 10**exp, exp

    @classmethod
    def count_digits(cls,num):
        search = list(str(num))
        n = 0
        for i in range(len(search)):
            if search[i].isdigit():
                if search[i]=="0" and n==0:
                    continue
                n += 1
        return n

    @classmethod
    def locate_nsf(cls,num,id):
        search = list(str(num))
        ith = 0
        loc = None
        for i in range(len(search)):
            if search[i].isdigit():
                if search[i]=="0" and ith==0:
                    continue
                ith += 1
            if ith == id:
                loc = i
                break
        if loc is None:
            loc = len(search)
        return loc
            
    @classmethod
    def modify_number(cls,num,loc):
        search = list(copy.copy(str(num)))
        if loc == len(search):            
            return num
        next = loc + 1
        if search[next] == ".":
            next += 1
        if int(search[next]) > 5:
            search[loc] = str(int(search[loc])+1)
        cut = False
        for i in range(loc+1,len(search)):            
            if search[i].isdigit():
                search[i] = "0"
            if search[i] == ".":
                cut = True
        result = "".join(search)
        if cut:
            result = result.split(".")[0]
        return result

    @classmethod
    def round(cls,number,nsf):        
        if type(number) is not str:
            num = str(copy.copy(number))
        else:
            num = copy.copy(number)
        M = re.search('(?P<sign>-)?(?P<mantissa>[\d\.]+)(?P<exp>[Ee]-?\+?[\d]+)?',num)
        loc = cls.locate_nsf(M.group('mantissa'),nsf)
        mantissa = cls.modify_number(M.group('mantissa'),loc)
        if cls.count_digits(mantissa) < nsf:            
            diff = nsf - cls.count_digits(mantissa)
            if "." not in mantissa:
                mantissa = mantissa +"."
            mantissa = mantissa + "".join(["0"]*diff)
        sign = ""
        if M.group('sign') is not None:
            sign = "-"
        exponent = ""
        if M.group('exp') is not None:        
            exponent = M.group('exp')
        result = sign+mantissa+exponent
        return result
    
    @classmethod
    def latex(cls,number):
        M = re.search('(?P<sign>-)?(?P<mantissa>[\d\.]+)(?P<exp>[Ee]-?\+?[\d]+)?',number)
        mantissa = M.group('mantissa')
        sign = ""
        if M.group('sign') is not None:
            sign = "-"
        exponent = ""
        if M.group('exp') is not None:
            exponent = M.group('exp').lower()
            exponent = exponent.replace("+","").replace("e","\\times\,10^{")+"}"
        result = sign+mantissa+exponent        
        return result

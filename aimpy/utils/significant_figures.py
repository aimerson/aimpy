#! /usr/bin/env python

import copy
import re
import numpy as np
from decimal import Decimal

class SigFig(object):
    
    @classmethod
    def fman(cls,number):
        return float(Decimal(number).scaleb(-cls.fexp(number)).normalize())

    @classmethod
    def fexp(cls,number):
        (sign, digits, exponent) = Decimal(number).as_tuple()
        return len(digits) + exponent - 1

    @classmethod
    def frexp10(cls,x):        
        man = cls.fman(x)
        exp = cls.fexp(x)
        return man, exp

    @classmethod
    def count_digits(cls,num):
        if type(num) is not str:
            raise TypeError("Number must be expressed as type string!")
        search = list(num.split("e")[0])
        n = 0
        for i in range(len(search)):
            if search[i].isdigit():
                if search[i]=="0" and n==0:
                    continue
                n += 1
        return n

    @classmethod
    def count_sf(cls,num):
        search = list(str(num))
        isf = 0
        for i in range(len(search)):
            if search[i].isdigit():
                if search[i]=="0" and isf==0:
                    continue
                isf += 1
        return isf

    @classmethod
    def locate_nsf(cls,num,nsf):
        search = list(str(num))
        ith = 0
        loc = None
        for i in range(len(search)):
            if search[i].isdigit():
                if search[i]=="0" and ith==0:
                    continue
                ith += 1
            if ith == nsf:
                loc = i
                break
        if loc is None:
            diff = nsf - ith
            if "." not in search:
                search = search + ["."]
            search = search + ["0"]*diff
            loc = len(search)-1
        return loc


    @classmethod
    def tidyup(cls,search,loc):
        if "." in search:
            pnt = search.index(".")
            if pnt > loc:
                search = search[:pnt]
            else:
                search = search[:loc+1]
        return search
        

    @classmethod
    def round_up_9s(cls,search,loc):
        if search[loc] != "9":
            return search,loc
        prev = loc - 1
        if search[prev] == ".":
            prev -= 1
        search[loc] = "0"
        while search[prev] == "9":            
            search[prev] = "0"
            prev -= 1
            if search[prev] == ".":
                prev -= 1
            if prev == -1:
                break
        if prev == -1:
            search = ["1"] + search
        else:
            if search[prev] == "-":
                search.insert(1,"1")
            else:                
                search[prev] = str(int(search[prev])+1)            
        if search[loc] == ".":
            loc -= 1
        return search,loc


    @classmethod
    def modify_number(cls,num,nsf):
        loc = cls.locate_nsf(num,nsf)
        search = list(copy.copy(str(num)))
        isf = cls.count_sf(num)
        # Require more significant figures than currently shown in number
        if nsf > isf:
            if "." not in search:
                search = search + ["."]
            diff = int(nsf - isf)
            search = search + ["0"]*diff
            result = "".join(search)
        # Exactly the correct number of significant figures already shown
        elif nsf == isf:
            result = "".join(search)
        # More significant figures being shown than required so
        # number needs to be trimmed
        else:
            next = loc + 1
            prev = loc - 1
            if search[next] == ".":
                next += 1
            if search[prev] == ".":            
                prev -= 1
            if int(search[next]) > 5:
                if int(search[loc]) == 9:
                    search,loc = cls.round_up_9s(search,loc)
                else:
                    search[loc] = str(int(search[loc])+1)
            for i in range(loc+1,len(search)):            
                if search[i].isdigit():
                    search[i] = "0"
            search = cls.tidyup(search,loc)
            result = "".join(search)
        return result

    @classmethod
    def force_float(cls,number):
        M = re.search('(?P<sign>-)?(?P<mantissa>[\d\.]+)(?P<exp>[Ee]-?\+?[\d]+)?',str(number))
        if M.group('exp') is None:
            return str(number)
        exp = int(M.group('exp').lower().replace("e",""))        
        digits = M.group('mantissa').replace(".","")
        if exp < 0:
            result = "0."+"".join(["0"]*(int(np.fabs(exp)-1)))+digits
        else:
            result = digits + "".join(["0"]*(exp-len(digits)))
        sign = ""
        if M.group('sign') is not None:
            sign = "-"
        result = sign + result
        return result

    @classmethod
    def round(cls,number,nsf):        
        if type(number) is not str:
            num = str(copy.copy(number))
        else:
            num = copy.copy(number)
        M = re.search('(?P<sign>-)?(?P<mantissa>[\d\.]+)(?P<exp>[Ee]-?\+?[\d]+)?',num)
        mantissa = cls.modify_number(M.group('mantissa'),nsf)
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
        if type(number) is not str:
            raise TypeError("Number is not expressed as a string!")
        M = re.search('(?P<sign>-)?(?P<mantissa>[\d\.]+)(?P<exp>[Ee]-?\+?[\d]+)?',number)
        mantissa = M.group('mantissa')
        sign = ""
        if M.group('sign') is not None:
            sign = "-"
        exponent = ""
        if M.group('exp') is not None:
            exponent = M.group('exp').lower()
            exponent = exponent.replace("+","").replace("e","\,\\times\,10^{")+"}"
        result = sign+mantissa+exponent        
        return result

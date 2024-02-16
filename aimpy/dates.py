#! /usr/bin/env python

import sys
import datetime
from dateutil.relativedelta import relativedelta 
import pytz
from pytz import timezone
from datetime import timedelta
from dateutil.parser import parse as parse_datetime

# https://stackabuse.com/converting-strings-to-datetime-in-python/ -- useful page for converting dates in different string formats.


class DatetimeRange:
    def __init__(self, dt1, dt2):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        return self._dt1 < dt < self._dt2

class DayLightSavings(object):

    def __init__(self,timeZoneName="Europe/London"):
        self.TIMEZONE = timezone(timeZoneName)
        return

    def _getTransitionIndex(self,year):
        dt = datetime.datetime(year,1,1)
        transitions = self.TIMEZONE._utc_transition_times
        index = next(i for i in range(len(transitions)) if transitions[i]-dt > timedelta(0))
        return index
    
    def getTransitionDatesInYear(self,year):
        index = self._getTransitionIndex(year)
        start = self.TIMEZONE._utc_transition_times[index]
        end = self.TIMEZONE._utc_transition_times[index+1]
        return (start,end)

    def insideDST(self,dt):
        dstRange = self.getTransitionDatesInYear(dt.year)
        INTERVAL = DatetimeRange(dstRange[0],dstRange[1])
        return dt in INTERVAL

    def offsetAtDateTime(self,dt):
        index = self._getTransitionIndex(dt.year)
        if self.insideDST(dt):
            offset = self.TIMEZONE._transition_info[index][1]
        else:
            offset = self.TIMEZONE._transition_info[index+1][1]
        return offset


class Dates(object):

    @classmethod
    def academicYear(cls,dateObj=None):
        years = []
        if dateObj is None:
            dateObj = cls.today()
        if dateObj.month >= 9:
            years = [dateObj.year,dateObj.year+1]
        else:
             years = [dateObj.year-1,dateObj.year]
        return years

    @classmethod
    def correctDayLightSaving(cls,dateObj,timeZoneName="Europe/London",fmt=None):
        DST = DayLightSavings(timeZoneName="Europe/London")
        offset = DST.offsetAtDateTime(dateObj)
        dateObj += offset
        if fmt is not None:
            output = cls.getDateString(dateObj,fmt=fmt)
        else:
            output = dateObj
        return output

    @classmethod
    def datebreak(cls,begin,end):
        """
        Dates.datebreak():  Return breakdown of months between two user specified dates. 
                            Returns a list containing start and end dates for for each month. 
        
            USAGE: breakdown = Dates.datebreak(begin,end)

                INPUT
                begin,end <str OR obj> = User-specified dates as either strings or datetime objects.
                OUTPUT
                breakdown <list> = Start and end dates, specified as strings, for each month that falls
                                    with the two specified dates inclusively.
        
        """
        ranges = []
        # Read in start and end dates (convert to datetime object if necessary).
        dt_start = cls.getDateObject(begin)
        dt_end = cls.getDateObject(end)
        # Get difference in months
        number_months = cls.differenceInMonths(dt_end,dt_start)+1
        ranges = []     
        out_fmt = '%Y-%m-%d'
        # Loop over number of months
        for i in range(number_months):
            start = dt_start + relativedelta(months=i)
            end = start
            if i < number_months-1:
                end = start + relativedelta(months=1)
            if i > 0:
                start = start.replace(day=1)
            end = end.replace(day=1)
            if i == number_months-1:
                end = end.replace(day=dt_start.day+1)
            ranges.append([start.strftime(out_fmt),end.strftime(out_fmt)])
        return ranges

    @classmethod
    def differenceInMonths(cls,d1,d2): 
        return (d1.year - d2.year)*12 + d1.month - d2.month

    @classmethod
    def getStartOfMonth(cls,dateObj):
        month = int(dateObj.strftime("%m"))
        year = int(dateObj.strftime("%Y"))
        return datetime.datetime.date(year,month,1)

    @classmethod
    def getDateFromTimestamp(cls,ts):
        return datetime.date.fromtimestamp(ts)

    @classmethod
    def getDateObject(cls,strdate):
        # fmtopts = ["%Y-%m-%dT%H:%M:%SZ","%Y-%m-%d","%Y-%m-%d %H:%M:%S",'%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y-%m-%dT%H:%M:%S.%f']
        return parse_datetime(strdate)
    
    @classmethod
    def getDateTimeFromTimestamp(cls,ts):
        return datetime.datetime.fromtimestamp(ts).astimezone(pytz.utc)

    @classmethod
    def getDateString(cls,dateObj,fmt='%Y-%m-%d %H:%M:%S'):
        if type(dateObj) is str:
            dateObj = cls.getDateObject(dateObj)
        dateStr = datetime.datetime.strftime(dateObj,fmt)
        return dateStr
    
    @classmethod
    def getEndOfMonth(cls,month,year=None):
        if year is None:
            year = int(cls.today().strftime("%Y"))
        d = datetime.datetime.date(int(year),int(month),1)
        return d - datetime.timedelta(days=1)
    
    @classmethod
    def getUnixTimestamp(cls,date):
        sdate = cls.getDateString(date,fmt="%Y-%m-%d")+" 00:00:00"
        corrected_date = cls.getDateObject(sdate).astimezone(pytz.utc)
        return int(corrected_date.timestamp())

    @classmethod
    def offsetMonths(cls,months,date=None):
        """Dates.offset_months(): Return the date today offset by a specified number of months.

            USAGE: offset = Dates.offset_months(months,[output_as_string=True])

                INPUT
                months <int> = Number of months to offset by.
                fmt <str> = Set format to return the output as a string (or leave as a datetime object if None).
                            (Default = None)
                OUTPUT
                offset <str OR obj> = Date that is offset by specified number of months, either as a datetime object or a string.

        """
        if date is None:
            date = datetime.datetime.today()
        output = date + relativedelta(months=months)
        return output

    @classmethod
    def today(cls,time=True):
        """
        Dates.today() : Returns today's date as a datetime object.

        USAGE: this_day = Dates.today([time=False])

        INPUT
            time <bool> [False] : Include the time in the datetime object.
        OUTPUT
            this_day <datetime> : Today's date as a datetime object.
        """
        if time:
            today = datetime.datetime.today()
        else:
            today = datetime.date.today()
        return today

    @classmethod
    def same_week(cls,ref_date_in,test_date_in):
        """
        Dates.same_week(); Determine whether two dates are in the same week.

            USAGE: sameweek = Dates.same_week(date1,date2)

            INPUT
            date1,date2 <str OR obj> = Dates to compare.
            OUTPUT
            sameweek <bool> = Boolean indicating whether the dates are in the same week (True) or not (False).

        """
        ref_date = cls.getDateObject(ref_date_in)
        test_date = cls.getDateObject(test_date_in)
        one_day = datetime.timedelta(days=1)
        # Determine the day of the week of the reference date
        day = ref_date.weekday()
        # Find start and end of the week
        startofweek = ref_date - day*one_day
        endofweek = ref_date + one_day*(6-day)
        # Test to see whether the test date falls between the dates 
        # corresponding to the start and end of the week
        sameweek = (test_date>=startofweek) and (test_date<=endofweek)
        return sameweek

    @classmethod
    def start_of_the_week(cls,input_date):
        """
        Dates.start_of_the_week():  For a specified date, returns the date that corresponds to
                                    the start of that week (assuming Monday as the first day).

            USAGE: startofweek = Dates.start_of_the_week(input_date)

            INPUT
            input_date [<str> or <datetime.datetime>] : Input date either as a formatted string or a datetime object.
            OUTPUT
            startofweek [<datetime.datetime>] : Date corresponding to start of the week as a datetime object.

        """
        one_day = datetime.timedelta(days=1)
        this_date = cls.str_to_datetimeobject(input_date,"%Y-%m-%d")
        # Determine the day of the week of the reference date
        day = this_date.weekday()
        # Date corresponding to start of the week
        startofweek = this_date - day*one_day
        return startofweek
    
    @classmethod
    def startOfWeek(cls,date):
        n = date.weekday()
        start = date - relativedelta(days=n)
        return start

    @classmethod
    def str_to_datetimeobject(cls,strdate,fmt):
        if type(strdate)!=str:
            return strdate
        try:
            objdate = datetime.datetime.strptime(strdate,fmt)
        except ValueError:
            objdate = None
        return objdate


    @classmethod
    def getChMSDateString(cls,dateObj):
        funcname = cls.__name__+"."+sys._getframe().f_code.co_name
        return cls.getDateString(dateObj,fmt="%Y-%m-%d %H:%M:%S")


    @classmethod
    def convertSharePointDate(cls,dateStr):
        funcname = cls.__name__+"."+sys._getframe().f_code.co_name
        dateObj = datetime.datetime.strptime(dateStr,"%Y-%m-%dT%H:%M:%SZ")
        return dateObj

    @classmethod
    def convertOutlookDate(cls,dateStr):
        dateObj = datetime.datetime.strptime(dateStr,"%Y-%m-%dT%H:%M:%SZ")
        return dateObj

    @classmethod
    def datesDiffer(cls,date1,date2,tolerance=60):
        dateObj1 = cls.getDateObject(date1)
        dateObj2 = cls.getDateObject(date2)
        diff = abs(dateObj2-dateObj1)
        result = diff > datetime.timedelta(seconds=tolerance)
        return result

    @classmethod
    def getEndDate(cls,month):
        date_time_obj = datetime.datetime.strptime(month[1],'%Y-%m-%d')
        date_time_obj = date_time_obj + datetime.timedelta(days=1)
        end_date = str(date_time_obj.date())        
        return end_date
    

class Months(object):

    def __init__(self,startDate,endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.months = Dates.datebreak(self.startDate,self.endDate)
        self.number = len(self.months)
        self.firstDay = [Dates.getDateObject(m[0]) for m in self.months]
        self.lastDay = [Dates.getDateObject(m[1]) for m in self.months]
        self.complete = [0 for m in self.months]
        return

    def findMonth(self,date):
        dateObj = Dates.getDateObject(date)
        if dateObj < self.firstDay[0] or dateObj > self.lastDay[-1]:
            index = None
        else:
            index = [i for i in range(len(self.firstDay)) if dateObj>=self.firstDay[i]][-1]
        return index
    

class TimePeriod(object):

    def __init__(self,dtStart,dtEnd):
        self.dtStart = dtStart
        self.dtEnd = dtEnd
        tsStart = dtStart.astimezone(pytz.utc).timestamp()
        tsEnd = dtEnd.astimezone(pytz.utc).timestamp()
        self.tsStart = tsStart
        self.tsEnd = tsEnd
        self.dateStart = datetime.datetime.fromtimestamp(self.tsStart)
        self.dateEnd = datetime.datetime.fromtimestamp(self.tsEnd)
        return
    
    def __contains__(self, dt):
        return self.datetimeInPeriod(dt)
    
    def datetimeInPeriod(self,dt):
        ts = dt.astimezone(pytz.utc).timestamp()
        inPeriod = ts >= self.tsStart and ts < self.tsEnd
        return inPeriod
    

    

class Month(TimePeriod):

    def __init__(self,date):
        sdate = Dates.getDateString(date.replace(day=1),fmt="%Y-%m-%d") + " 00:00:00"
        self.firstDay = Dates.getDateObject(sdate).astimezone(pytz.utc)
        self.firstDayNextMonth = self.firstDay + relativedelta(months=1)
        super().__init__(self.firstDay,self.firstDayNextMonth)
        self.lastDay = self.firstDayNextMonth + relativedelta(days=-1)
        self.numberDays = (self.firstDayNextMonth-self.firstDay).days
        return
    
    def dateInMonth(self,date):
        return self.datetimeInPeriod(date.astimezone(pytz.utc))




#begin = "2022-02-04 14:47:24.379590"
#end = "2023-07-04 14:47:24.379590"
#bobj = Dates.getDateObject(begin)
#eobj = Dates.getDateObject(end)

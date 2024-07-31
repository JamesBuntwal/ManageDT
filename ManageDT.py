"""
ManageDT.py
"""

#------------------------------------------------------------------------------#
# Imports
#------------------------------------------------------------------------------#

from datetime import datetime
from dateutil.relativedelta import relativedelta
import copy



#------------------------------------------------------------------------------#
# dt class
#------------------------------------------------------------------------------#

class dt():
    def __init__(   self,
                    value = None,
                    year = None,
                    month = None,
                    day = None,
                    hour = None):

        # init based on value or args
        if value is not None:
            self.value_init(value)
            # run asserts to make sure valid dt
            self.value_assert()
        else:
            self.arg_init(year, month, day, hour)

    # string represenation
    def __repr__(self):
        return (    f"{self.year or '0000'}"
                    f"{self.month or '00'}"
                    f"{self.day or '00'}"
                    f"{self.hour or '00'}" )

    # string represenation
    def __str__(self):
        return self.__repr__()
    
    def __int__(self):
        return int(str(self))

    @property
    def str(self):
        return repr(self)
    @property
    def int(self):
        return int(self)
    
    # init when using full value
    def value_init(self, value):
        value = str(value)
        assert len(value) == 10, 'required value format YYYYMMDDHH.'
        self.year = f"{int(value[:4]):04d}"
        self.month = f"{int(value[4:6]):02d}"
        self.day = f"{int(value[6:8]):02d}"
        self.hour = f"{int(value[8:10]):02d}"

    # init when using args
    def arg_init(self, year, month, day, hour):
        self.year = f"{int(year):04d}" if year is not None else None
        self.month = f"{int(month):02d}" if month is not None else None
        self.day = f"{int(day):02d}" if day is not None else None
        self.hour = f"{int(hour):02d}" if hour is not None else None

    # make sure vlaid dt obj
    def value_assert(self):
        if self.year is not None:
            assert (int(self.year) >= 0), "Year must be positive."
        if self.month is not None:
            assert (0 <= int(self.month) <= 12), "Month must be 0 <= x <= 12."
        if self.day is not None:
            assert (0 <= int(self.day) <= 31), "Day must be 0 <= x <= 31."
        if self.hour is not None:
            assert (0 <= int(self.hour) <= 23), "Hour must be 0 <= x <= 23."

    # properties useful for conversions
    @property
    def datetime(self):
        return datetime(    year = int(self.year),
                            month = int(self.month),
                            day = int(self.day),
                            hour = int(self.hour))


    # static methods for quick access
    @staticmethod
    def Y(x): return dt(year = x)

    @staticmethod
    def M(x): return dt(month = x)

    @staticmethod
    def D(x): return dt(day = x)

    @staticmethod
    def H(x): return dt(hour = x)

    @staticmethod
    def from_datetime(datetime_obj):
        return dt(
            year = datetime_obj.year,
            month = datetime_obj.month,
            day = datetime_obj.day,
            hour = datetime_obj.hour)
    
    @staticmethod
    def from_relativedelta(datetime_obj):
        return dt(
            year = datetime_obj.years,
            month = datetime_obj.months,
            day = datetime_obj.days,
            hour = datetime_obj.hours)

    # dunders for calculations and comparisons
    def __add__(self, other):
        x = self.datetime
        if isinstance(other, dt):
            y = relativedelta(  years = int(other.year or 0),
                                months = int(other.month or 0),
                                days = int(other.day or 0),
                                hours = int(other.hour or 0))
        elif isinstance(other, relativedelta):
            y = other
        output = x+y
        return dt.from_datetime(output)

    def __iadd__(self, other):
        self = self + other
        return self

    def __sub__(self, other):
        x = self.datetime
        if isinstance(other, dt):
            y = relativedelta(  years = int(other.year or 0),
                                months = int(other.month or 0),
                                days = int(other.day or 0),
                                hours = int(other.hour or 0))
        elif isinstance(other, relativedelta):
            y = other
        output = x-y
        return dt.from_datetime(output)

    def __isub__(self, other):
        self = self - other
        return self

    def __eq__(self, other):
        if isinstance(other, dt):
            return self.datetime == other.datetime
        if isinstance(other, datetime):
            return self.datetime == other
        if isinstance(other, str) or isinstance(other, int):
            return self.datetime == dt(other).datetime

    def __lt__(self, other):
        if isinstance(other, dt):
            return self.datetime < other.datetime
        if isinstance(other, datetime):
            return self.datetime < other
        if isinstance(other, str) or isinstance(other, int):
            return self.datetime < dt(other).datetime

    def __le__(self, other):
        if isinstance(other, dt):
            return self.datetime <= other.datetime
        if isinstance(other, datetime):
            return self.datetime <= other
        if isinstance(other, str) or isinstance(other, int):
            return self.datetime <= dt(other).datetime

    def __gt__(self, other):
        if isinstance(other, dt):
            return self.datetime > other.datetime
        if isinstance(other, datetime):
            return self.datetime > other
        if isinstance(other, str) or isinstance(other, int):
            return self.datetime > dt(other).datetime

    def __ge__(self, other):
        if isinstance(other, dt):
            return self.datetime >= other.datetime
        if isinstance(other, datetime):
            return self.datetime >= other
        if isinstance(other, str) or isinstance(other, int):
            return self.datetime >= dt(other).datetime

    def __hash__(self):
        return hash(int(self))

    def time_between(self, other):
        if not isinstance(other, dt):
            other = dt(other)
        rd = relativedelta( other.datetime,
                            self.datetime
                            )
        return rd

    def hours_between(self, other):
        if not isinstance(other, dt):
            other = dt(other)
        seconds = (
            (self.datetime - other.datetime)
            .total_seconds()
            )
        hours = seconds / 3600
        return abs(hours)

    def iter_until(self, end_dt, dtype = None):
        if not isinstance(end_dt, dt):
            end_dt = dt(end_dt)
        current = copy.deepcopy(self)
        
        yield (current if dtype is None else dtype(current))
            
        while current != end_dt:
            current += dt.H(1)
            yield (current if dtype is None else dtype(current))
                
    def iter_for(   self,
                    years = 0,
                    months = 0,
                    days = 0,
                    hours = 0,
                    include_last = False,
                    dtype = None):
        rd = relativedelta( years = years,
                            months = months,
                            days = days,
                            hours = hours
        )
        end_dt = self + rd
        current = copy.deepcopy(self)
        while current != end_dt:
            yield (current if dtype is None else dtype(current))
            current += dt.H(1)
        if (current == end_dt) and include_last:
            yield (current if dtype is None else dtype(current))
            

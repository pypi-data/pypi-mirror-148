"""some additional helpers for trackunit"""

from datetime import datetime, timedelta
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.dates
from  dateutil.parser.isoparser import isoparse

def plot_can_val(_data,valname,filename=None):
    """plot value from getCanData"""
    data = filter(lambda x:x['name'] == valname,_data)
    plot_val(data,'value',filename)

def get_datetime(time_string):
    """transforms trackunit time string to datetime"""
    #return datetime.strptime(time_string.split('.')[0],"%Y-%m-%dT%H:%M:%S")
    return isoparse(time_string)

def plot_val(_data,valname,filename=None):
    """plots a value from data (expected format from getHistory)"""
    data = (map(lambda x: (x['time'],x[valname]),_data))
    data = (set(data))
    data = (map(lambda x: (get_datetime(x[0]),float(x[1])),data))
    data = list(data)
    data.sort(key=lambda x: x[0])
    dates = list(map(lambda x: x[0], data))
    dates = matplotlib.dates.date2num(dates)
    fig, _ax = plt.subplots()#marker='', linestyle='-'
    values = list(map(lambda x: x[1], data))
    _ax.plot_date(dates, values ,fmt=",-")
    _ax.locator_params(axis="y", nbins=10)
    fig.autofmt_xdate()
    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

def get_next_section(data,finsec,fendsec=None,min_insec_len=None,min_endsec_len=0):
    """
    returns the next section wich fulfills finsec with at least min_insec_len datapoints
    and ends with data wich fulfills fendsec which is at least min_endsec_len long
    """
    data.sort(key=lambda x: datetime.strptime(x['time'].split('.')[0],"%Y-%m-%dT%H:%M:%S"))
    out = []
    in_section = False
    off_sec_cnt = 0
    for datapoint in data:
        if not in_section and finsec(datapoint):
            out = []
            off_sec_cnt = 0
            out.append(datapoint)
            in_section = True
        elif in_section and finsec(datapoint):
            out.append(datapoint)
        elif in_section and not finsec(datapoint):
            if (min_insec_len is None or len(out) >= min_insec_len) and \
                (fendsec is None or fendsec(datapoint)):
                if off_sec_cnt >= min_endsec_len:
                    return out
                off_sec_cnt += 1
                in_section = False
            else:
                in_section = False
                out = []
        elif not in_section and len(out) > 0:
            if fendsec(datapoint):
                off_sec_cnt += 1
                if off_sec_cnt >= min_endsec_len:
                    return out
            else:
                out = []
                off_sec_cnt = 0
    if (fendsec is None or min_endsec_len <= 0) and \
        (min_insec_len is None or len(out) >= min_insec_len):
        return out
    return None

def get_time_diff(timepoint_1,timepoint_2):
    """returns the diffrence between two trackunit timestrings"""
    dtt1 = datetime.strptime(timepoint_1.split('.')[0],"%Y-%m-%dT%H:%M:%S")
    dtt2 = datetime.strptime(timepoint_2.split('.')[0],"%Y-%m-%dT%H:%M:%S")
    return dtt1-dtt2

def moving_avg(data,valname,alpha=0.01,in_same = False):
    """
    creates a copy of data where the valname index has a moving avg with alpha applied
    """
    if in_same:
        data2 = data
    else:
        data2 = deepcopy(data)
    def fma(_x,last):
        return alpha*_x+(1-alpha)*last
    last = float(data[0][valname])
    for datapoint in data2:
        last = fma(float(datapoint[valname]),last)
        datapoint[valname] = str(last)
    return data2

def start_end_from_tdelta(tdelta, preset_end=None):
    """
    returns start and end (as datetime) from a given timedelta
        (either type timedelta or and integer with days)
    if preset_end is set to a datetime, the end will be set to this value
    in any case it will return an end with hours, minutes, second, microseconds set to zero
    """
    if preset_end is None:
        end = datetime.now()
    else:
        end = preset_end
    end = end.replace(hour=0,minute=0,second=0,microsecond=0)
    if isinstance(tdelta,timedelta):
        start = end-tdelta
    else:
        irange = int(tdelta)
        if irange <= 0:
            return end, end
        start = end-timedelta(days=irange)
    return start, end

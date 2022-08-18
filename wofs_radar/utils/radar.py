import os
from datetime import timedelta
from Config import settings

def __utc2local__ (utc):
    # epoch = time.mktime(utc.timetuple())
    # offset = datetime.fromtimestamp (epoch) - datetime.utcfromtimestamp (epoch)
    # return utc + offset
    # head node is set to UTC, so hardcode this TODO: fix this!!
    return utc - timedelta(hours=9)

def __get_radar_path__(start_time):
    local_time = __utc2local__(start_time)
    return os.path.join(settings.default_grid_info, ("radars.%s.csh" % local_time.strftime("%Y%m%d")))

def getFromFile(start_time):
    """
        Returns list of radars for the given start_time by parsing the radars.csh file.
        start_time should be in UTC, which will get converted to local time
    """
    try:
        with open(__get_radar_path__(start_time)) as fhandle:
            all_lines  = fhandle.readlines()
            radar_list = all_lines[6].split("(")[1].split(")")[0].split()
    except:
        print("NO RADAR FILE OR BAD FORMAT FOR UTC DATE: %s" % start_time.strftime("%Y%m%d"))
        return None

    return radar_list

def getLatLonFromFile(start_time):
    """
        Returns center (lat, lon) for the given start_time by parsing the radars.csh file.
        start_time should be in UTC, which will get converted to local time
    """    
    try:
        with open(__get_radar_path__(start_time)) as fhandle:
            all_lines  = fhandle.readlines()
            lat = float(all_lines[7].split(" ")[2])
            lon = float(all_lines[8].split(" ")[2])
    except:
        print("NO RADAR FILE OR BAD FORMAT FOR UTC DATE: %s" % start_time.strftime("%Y%m%d"))
        return None

    return (lat, lon)


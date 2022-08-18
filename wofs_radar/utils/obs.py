
import os
import netCDF4 as ncdf
import numpy as np
import datetime as DT
import xarray as xr
import pandas as pd

#=========================================================================================
# Defines the data frame for each observation type
#
def obs_seq_xarray(len):
    return (np.recarray(len,
                    dtype = [
                             ('value',               'f8'),
                             ('lat',                 'f8'),
                             ('lon',                 'f8'),
                             ('height',              'f8'),
                             ('error_var',           'f4'),
                             ('utime',               'f8'),
                             ('date',                'S128'),
                             ('day',                 'i8'),
                             ('second',              'i8'),
                             ('platform_lat',        'f8'),
                             ('platform_lon',        'f8'),
                             ('platform_hgt',        'f8'),
                             ('platform_dir1',       'f8'),
                             ('platform_dir2',       'f8'),
                             ('platform_dir3',       'f8'),
                             ('platform_nyquist',    'f8')
                            ]), \
                         {
                           'lat':   ["degrees", "latitude of observation"],
                           'lon':   ["degrees", "longitude of observation (deg. west)"],
                           'height':["meters",  "height above sea level"],
                           'utime': ["seconds since 1970-01-01 00:00:00", "time of observation"],
                           'date':  ["", "date and time of obsevation"]
                          })

def write_obs_seq_xarray(field, radar, filename=None, obs_error=3., volume_name=None):

    _time_units    = 'seconds since 1970-01-01 00:00:00'
    _calendar      = 'standard'

    if filename == None:
        print("\n WRITE_DATA_XARRAY:  No output file name is given, writing to %s" % "obs_seq.txt")
        filename = "obs_seq.nc"
    else:
        dirname = os.path.dirname(filename)
        basename = "%s_%s.nc" % ("obs_seq", os.path.basename(filename))
        filename =  os.path.join(dirname, basename)

    _stringlen     = 8
    _datelen       = 19

    # Extract data.city data

    fld           = field.data.data[:,:,:]
    mask          = field.data.mask[:,:,:]
    lats          = field.lats
    lons          = field.lons
    xgrid         = field.xg[:]
    ygrid         = field.yg[:]
    zgrid         = field.zg[:,:,:]
    msl_hgt       = field.zg[:,:,:] + field.radar_hgt

    platform_lat  = field.radar_lat
    platform_lon  = field.radar_lon
    platform_hgt  = field.radar_hgt

    # Use the volume mean time for the time of the volume

    utime   = ncdf.num2date(field.time['data'].mean(), field.time['units'])
    secs    = ncdf.date2num(utime, units = _time_units)
    # Retain DART time stamps
    days    = ncdf.date2num(utime, units = "days since 1601-01-01 00:00:00")
    seconds = np.int(86400.*(days - np.floor(days)))

    print("\n -->  Writing %s as the radar file..." % (filename))
    #  mask_check = data.mask && numpy.isnan().any()

    nobs = np.sum(mask==False)
    print("\n -----> Number of good observations for xarray:  %d" % nobs)

    # Create numpy rec array that can be converted to a pandas table.

    out, attributes = obs_seq_xarray(nobs)

    # There is a far better way to do this but this is fast enough for now...

    n = 0

    for k in np.arange(fld.shape[0]):
        for j in np.arange(fld.shape[1]):
            for i in np.arange(fld.shape[2]):

                if mask[k,j,i] == True: continue

                dx    = xgrid[i]
                dy    = ygrid[j]
                dz    = zgrid[k,j,i]
                range = np.sqrt(dx**2 + dy**2 + dz**2)
                dir1  = dx / range
                dir2  = dy / range
                dir3  = dz / range

                out.value[n]              = fld[k,j,i]
                out.error_var[n]          = obs_error**2
                out.lon[n]                = lons[i]
                out.lat[n]                = lats[j]
                out.height[n]             = msl_hgt[k,j,i]
                out.date[n]               = utime
                out.utime[n]              = secs
                out.day[n]                = days
                out.second[n]             = seconds
                out.platform_lon[n]       = platform_lon
                out.platform_lat[n]       = platform_lat
                out.platform_hgt[n]       = platform_hgt
                out.platform_dir1[n]      = dir1
                out.platform_dir2[n]      = dir2
                out.platform_dir3[n]      = dir3
                out.platform_nyquist[n]   = field.nyquist[k]

                n = n + 1
    
    # Create an xarray dataset for file I/O
    xa = xr.Dataset(pd.DataFrame.from_records(out))

    #  # reset index to be a master index across all obs
    xa = xa.rename({'dim_0': 'index'})

    # Write the xarray file out (this is all there is, very nice guys!)
    xa.to_netcdf(filename, mode='w')
    xa.close()

    # Add attributes to the files

    fnc = ncdf.Dataset(filename, mode = 'a')
    fnc.radar_name = radar
    fnc.history = "Created " + DT.datetime.today().strftime("%Y%m%d_%H%M")
    fnc.version = "Version 1.0a by Lou Wicker and Thomas Jones (NSSL)"

    if volume_name != None:
        fnc.version = "Created from the WSR88D radar volume:  %s" % volume_name

    for key in list(attributes.keys()):
        fnc.variables[key].units = attributes[key][0]
        fnc.variables[key].description = attributes[key][1]

    fnc.sync()
    fnc.close()

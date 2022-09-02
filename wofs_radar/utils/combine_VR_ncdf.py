from netcdftime import utime
import sys, os, glob
import time
import datetime as DT
from optparse import OptionParser
from ..Config import AppConfiguration
import xarray as xr
import netCDF4 as ncdf

time_format = "%Y%m%d_%H:%M:%S"
day_utime   = utime("days since 1601-01-01 00:00:00")
sec_utime   = utime("seconds since 1970-01-01 00:00:00")


def combine(input_files, output_file):                  
    dataset = []
    radars = []
    nobs_total = 0

    begin_time = time.time()
        
    for file in input_files:
       try:
          infile = xr.open_dataset(file)
          radars.append((infile.radar_name, nobs_total, nobs_total + len(infile.index)))
          nobs_total = nobs_total + len(infile.index)
          print("%s has %d observations, total is now %d" % (file, len(infile.index), nobs_total))
       except:
          continue

       if len(infile.index) > 0:
           dataset.append(infile)
       infile.close()
            
    end_time = time.time()
    
    print("\n Reading took {0} seconds since the loop started \n".format(end_time - begin_time))
    
    if len(dataset) <= 0:
        print('No valid set of VR observations were found; nothing to combine.')
        return
        
    # Create an xarray dataset for file I/O
    xa = xr.concat(dataset, dim='index')
    
    # Write the xarray file out (this is all there is, very nice guys!)
    xa.to_netcdf(output_file, mode='w')
    xa.close()
    
    #   Add attributes to the files
    fnc = ncdf.Dataset(output_file, mode = 'a')
    fnc.history = "Created " + DT.datetime.today().strftime(time_format)
    
    fnc.createDimension("radar", len(radars))
    rname = fnc.createVariable("radar_name","S4", ("radar",))
    rstart = fnc.createVariable("radar_start","u4", ("radar",))
    rend = fnc.createVariable("radar_end","u4", ("radar",))

    for (i, v) in enumerate(radars):
        rname[i] = v[0]
        rstart[i] = v[1]
        rend[i] = v[2]

    fnc.sync()  
    fnc.close()

def combine_from_pattern(searchPattern, directory):
    wild = os.path.abspath(directory)+"/obs_seq_K*"+searchPattern
    print(wild)
    rawlist = glob.glob(wild)
    print(rawlist)
    
    files = sorted( rawlist, key = lambda file: os.path.getmtime(file))
    
    print("\n Obs_seq.final files sorted by modification time\n")
    for file in files:
        print(" {} - {}".format(file, time.ctime(os.path.getmtime(file))) )
    
    # Fix in case we picked up some none obs_seq files
    for n, file in enumerate(files):
        if file.find(".out") != -1:  
            print("\n Removing file:  %s from list" % file)
            del files[n]

    print("\n Dart_cc:  Processing %d files in the directory:  %s" % (len(files), directory))

    if len(files) <= 0:
        print('No valid set of VR observations were found; nothing to combine.')
        return

    print(" Dart_cc:  First file is %s" % (files[0]))
    print(" Dart_cc:  Last  file is %s" % (files[-1]))
    
    tmp         = os.path.basename(files[0])
    netcdf_file = os.path.join(directory, "%s%s" % (tmp[0:7], tmp[12:]))

    print("\n Dart_cc:  netCDF4 file to be written is %s\n" % (netcdf_file))

    combine(files, netcdf_file)

#=========================================================================================
# Write out obs_seq files to netCDF for faster inspection
#-------------------------------------------------------------------------------
# Main function defined to return correct sys.exit() calls

def main(argv=None):
    if argv is None:
           argv = sys.argv

    # Command line interface for DART_cc
    
    parser = OptionParser()

    parser.add_option("-d", "--dir",  dest="dir",  default=None, type="string",
                       help = "Directory of files to process ")

    parser.add_option("-f", "--file",  dest="file",  default=None, type="string",
                       help = "wildcard of files to process ")

    parser.add_option("-p", "--prefix", dest="fprefix",  default=None, type="string",
                       help = "Preappend this string to the netcdf object filename")

                       
    (options, args) = parser.parse_args()
    
    if options.dir == None:
        settings = AppConfiguration.get()
        options.dir = settings.opaws_obs_seq

    combine_from_pattern(options.file, options.dir)

#-------------------------------------------------------------------------------
# Main program for testing...
#
if __name__ == "__main__":
    sys.exit(main())

# End of file

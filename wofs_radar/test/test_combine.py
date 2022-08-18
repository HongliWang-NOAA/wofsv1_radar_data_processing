import unittest, types, sys, os, glob, time
import xarray as xr
import datetime as DT
import netCDF4 as ncdf
from utils.combine_VR_ncdf import combine

class test_combine(unittest.TestCase):
    def test_combine_outputs(self):

        search_pattern = "../../wofs_radar/tests/data/TestCombine/obs_seq_K*.nc"
        output_dir = "out"

        files = sorted(glob.glob(search_pattern), key = lambda file: os.path.getmtime(file))
        
        print("\n Obs_seq.final files sorted by modification time\n")
        for file in files:
            print(" {} - {}".format(file, time.ctime(os.path.getmtime(file))) )
        
        tmp         = os.path.basename(files[0])
        netcdf_file = os.path.join(output_dir, "%s%s" % (tmp[0:7], tmp[12:]))

        combine(files, '../../wofs_radar/tests/data/TestCombine/obs_seq_VR_20200302_2315.nc')

if __name__ == '__main__':
    unittest.main()
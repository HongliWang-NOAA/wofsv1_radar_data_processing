import unittest
import types, calendar, os, datetime
from refl import run_refl_for_radar_time
from Config import settings

class test_refl(unittest.TestCase):

    def test_mrms_opaws(self):
        obj = types.SimpleNamespace()
        #obj.dname = settings.opaws_feed + '/KDMX'
        obj.out_dir = settings.opaws_obs_seq + '/20200302'
        obj.write = True
        #obj.window = '2020,03,03,06,23'
        obj.onlyVR = True
        obj.plot = 0
        obj.dx = 2000.000000
        obj.roi = 1000.000000
        obj.qc = 'Minimal'
        obj.unfold = 'region'
        obj.newse = None
        obj.method = None
        obj.shapefiles = None
        obj.interactive = None

        settings.mrms_feed = '../../wofs_radar/RADAR'
        settings.mrms_obs_seq = 'data/output'

        run_refl_for_radar_time(datetime.datetime(2022, 8, 14, 9, 0, 0), -94.5166, 33.465823)

if __name__ == '__main__':
    unittest.main()
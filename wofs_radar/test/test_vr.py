import unittest
import types, calendar, os, datetime
from vr import run_vr_for_radar_time
from Config import AppConfiguration
from multiprocessing import Pool

class test_vr(unittest.TestCase):
    # def test_kohx(self):
    #     obj = types.SimpleNamespace()
    #     obj.out_dir = 'out'
    #     obj.write = True
    #     obj.onlyVR = True
    #     obj.plot = 0
    #     obj.dx = 2000.000000
    #     obj.roi = 1000.000000
    #     obj.newse = None
    #     obj.method = None
    #     obj.shapefiles = None
    #     obj.interactive = None
    #     obj.write_dart = True

    #     settings.rass_input = 'tests/data/TestRASS'
    #     settings.rass_input_refl = 'Reflectivity'
    #     settings.rass_reflectivity_var = 'ReflectivityQC'

    #     run('KOHX', datetime.datetime(2020, 3, 3, 6, 1, 0), obj)

    #     run('KOHX', datetime.datetime(2020, 3, 3, 6, 13, 0), obj)

    #     run('KOHX', datetime.datetime(2020, 3, 3, 6, 15, 0), obj)

    def test_kohx(self):
        settings = AppConfiguration.get()

        settings.default_grid_info = '../../wofs_radar/tests/data/TestMRMS_VR'
        settings.rass_input = '../../wofs_radar/tests/data/TestRASS'
        settings.rass_input_refl = 'Reflectivity'
        settings.rass_reflectivity_var = 'ReflectivityQC'
        settings.rass_output = 'data/output'

        run_vr_for_radar_time(datetime.datetime(2020, 3, 3, 6, 13, 0), 0, 'KOHX')
        
        obj = types.SimpleNamespace()
        obj.out_dir = 'out'
        obj.write = True
        obj.onlyVR = True
        obj.plot = 0
        obj.dx = 2000.000000
        obj.roi = 1000.000000
        obj.newse = None
        obj.method = None
        obj.shapefiles = None
        obj.interactive = None
        obj.write_dart = True

        run_vr_for_radar_time(datetime.datetime(2020, 3, 3, 6, 1, 0), 0, 'KOHX')

        run_vr_for_radar_time(datetime.datetime(2020, 3, 3, 6, 13, 0), 0, 'KOHX')

        run_vr_for_radar_time(datetime.datetime(2020, 3, 3, 6, 15, 0), 0, 'KOHX')


if __name__ == '__main__':
    unittest.main()
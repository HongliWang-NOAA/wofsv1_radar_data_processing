import types, os
from ..Config import settings
from .mrms import run

def run_vr_for_radar_time(start_time, radar):

    print(f'Processing radar {radar}')

    obj = types.SimpleNamespace()
    obj.dname = os.path.join(settings.rass_input.format(start_time.strftime("%Y%m%d")), radar)
    obj.out_dir = settings.rass_output
    obj.write = settings.rass_write
    obj.window = start_time.strftime("%Y,%m,%d,%H,%M")
    obj.onlyVR = settings.rass_onlyvr
    if (settings.rass_plot != ""):
        obj.plot = int(settings.rass_plot)  
    else:
        obj.plot = None
    obj.dx = float(settings.rass_dx)
    obj.roi = float(settings.rass_roi)
    obj.newse = None
    obj.method = None
    obj.shapefiles = None
    obj.interactive = None
    obj.write_dart = settings.rass_write_dart
    run(radar, start_time, obj)
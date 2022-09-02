from datetime import datetime
import types, os
from ..Config import AppConfiguration
from .prep_mrms import run

def run_refl_for_radar_time(start_time: datetime, lon: float, lat: float, config_file: str):
    settings = AppConfiguration.load(config_file)

    obj = types.SimpleNamespace()
    obj.dir = os.path.join(settings.mrms_feed, start_time.strftime("%Y/%m/%d"))
    obj.realtime = start_time.strftime("%Y%m%d%H%M")
    obj.grep = '*.netcdf.gz'
    obj.write = True
    obj.out_dir = settings.mrms_obs_seq
    obj.plot = int(settings.mrms_plot)
    obj.loc = [lat, lon]
    obj.thin = 1    
    run(obj)


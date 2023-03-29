# wofs-obs-radar

## Build

`sudo docker build -t wofs-radar .`

## Run
```
export DATA_PATH=/mnt/c/Joshua/Source/Repos/wofs-obs-radar/data

docker run --mount type=bind,source=$PWD,target=/opt/wofs --mount type=bind,source=$DATA_PATH,target=/mnt/obs wofs-radar -t 202003030615 --longitude -94.5166 --latitude 33.465823 -r KOHX -f app.cfg
```

Note: you must bind the current working directory so that the application can read your app.cfg file. You must also bind the data directory where input/output files reside.

## Testing
```
python3 -m wofs_radar -t 202303242000 --longitude -91.122146 --latitude 33.712886 -r KPOE,KSHV -f app.local.cfg
```
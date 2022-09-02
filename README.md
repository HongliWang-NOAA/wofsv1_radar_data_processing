# wofs-radar-docker

## Build

`sudo docker build -t wofs-radar .`

## Run
```
export DATA_PATH=/mnt/c/Joshua/Linux/wofs-radar-docker/data

docker run --mount type=bind,source=$PWD,target=/opt/wofs --mount type=bind,source=$DATA_PATH,target=/opt/data wofs-radar -t 202003030615 --longitude -94.5166 --latitude 33.465823 -r KOHX -f app.cfg
```

Note: you must bind the current working directory so that the application can read your app.cfg file. You must also bind the data directory where input/output files reside.


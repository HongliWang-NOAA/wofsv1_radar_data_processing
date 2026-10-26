import datetime as DT
import sys, os, time
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import threading


def getradarlist(radar,ctime,noaas3,path):
    
    radarlist = []
    prefix = "%s/%s/" % (ctime.strftime("%Y/%m/%d"), radar)
    radardic = noaas3.list_objects_v2(Bucket='unidata-nexrad-level2', Delimiter='/', Prefix= prefix)
    #print(prefix)
    if "Contents" in radardic:
        for i in radardic['Contents'][:]:
            #if ((i['Key'][-2::] == '06' and i['Key'][-13:-11] == ctime.strftime("%H")) or (i['Key'][-3::] == 'V06' and i['Key'][-10:-8] == ctime.strftime("%H"))):
            if ((i['Key'][-3::] == 'V06' and i ['Key'][-13:-8] == ctime.strftime("%d_%H"))):
                fin = open(path+'/'+radar+'LIST.txt','a')
                fin.write(i['Key']+'\n')
                fin.close()
                radarlist.append(i['Key'])
            else:
                continue

    return(radarlist,prefix)

def downloadradars(radarlist,ctime,noaas3,prefix,radar,outloc):

    #if not os.path.exists(path+'/radars/'+prefix[-5::]):
    #    os.makedirs(path+'/radars/'+prefix[-5::])
    #print(radarlist)
    for i in radarlist:
        noaas3.download_file('unidata-nexrad-level2',i,outloc+'/'+i[-23::])
    
    return 0

def read_radar_files(fpath):

    fin = open(fpath,'r')
    finlines = fin.readlines()
    fin.close()
    radar_name = finlines[6]
    radars = radar_name.lstrip("set rad_name = (").rstrip(' )\n').split(' ')
    
    return radars
def main_process(radar,ctime,noaas3,path,outloc):

    if not os.path.exists(path+'/'+radar):
        os.makedirs(path+'/'+radar)

    while ctime < dtend:
        print(ctime.strftime("%Y%m%d-%H"))
        ##getradarlist()
        radarlist, prefix = getradarlist(radar,ctime,noaas3,path)
        ##downloadradars()
        out = downloadradars(radarlist,ctime,noaas3,prefix,radar,outloc)
        prvTime=ctime.strftime("%Y%m%d")
        ctime = ctime+advancehour
    return 0

if __name__ == '__main__':

    maxcount=10

    advancehour = DT.timedelta(hours=1)

    _region        = 'us-east-1'

    noaas3 = boto3.client('s3', region_name = _region, config=Config(signature_version=UNSIGNED))

    date = str(sys.argv[1])
    radarfilepath = sys.argv[2]
    #startdate = date+'14'
    #date12 = date+'07'
    startdate = date+'8'
    date12 = date+'07'
    outdir = sys.argv[3]
    path = outdir+'/'+date
    dtstart = DT.datetime.strptime(startdate, "%Y%m%d%H") 
    dtend = DT.datetime.strptime(date12, "%Y%m%d%H")+DT.timedelta(days=1)
    #dtend = DT.datetime.strptime(date12, "%Y%m%d%H")
 
    #for reading radar file
    radarfile = os.path.join(
        radarfilepath,
        'radars.' + date + '.csh'
    )

    print("radarfile =", radarfile)
    print("exists =", os.path.exists(radarfile))
    print("absolute path =", os.path.abspath(radarfile))

    radars = read_radar_files(os.path.join(radarfilepath,'radars.'+date+'.csh'))

    print("radars =", radars)
    print("type =", type(radars))
    print("count =", len(radars))

    prvTime=""


    for radar in radars:

        ctime = dtstart
        outloc = path + '/' + radar

        print("================================", flush=True)
        print("ABOUT TO PROCESS:", radar, flush=True)
        print("ctime:", ctime, flush=True)
        print("outloc:", outloc, flush=True)

        main_process(
            radar,
            ctime,
            noaas3,
            path,
            outloc
        )

        print("FINISHED:", radar, flush=True)
        #sys.exit(0)


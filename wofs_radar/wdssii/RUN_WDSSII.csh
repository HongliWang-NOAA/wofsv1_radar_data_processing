#!/bin/csh 

# For wof-post machines
#setenv PATH ./:/work2/wof/realtime/OBSGEN/MRMS_20230802/bin:$PATH
#setenv W2_CONFIG_LOCATION /work2/wof/realtime/OBSGEN/MRMS_20230802/WDSS2/w2/w2config

# For wof-epyc machines
setenv PATH ./:/work2/wof/realtime/OBSGEN/MRMS_20240523/bin:$PATH
setenv W2_CONFIG_LOCATION /work2/wof/realtime/OBSGEN/MRMS_20240523/WDSS2/w2/w2config

foreach event ( 20260916 )

#Change to current directory
#cd /home/wofuser/wofs-obs-radar/wofs_radar/wdssii
cd /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/frdd-wofs-obs-radar_OSTI/wofs_radar/wdssii

set eventd2 = `date -d "${event} 1 day" "+%Y%m%d"`
set l2dir_aws =  /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/realtime/OBSGEN/NEXRAD #Parent path of NEXRAD download location
set l2dir =  /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/wof/realtime/OBSGEN/NEXRAD/${event} #Location of event NEXRAD data
set wdssdir =  /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/realtime/OBSGEN/WDSSII/${event} #Location of WDSS-II processed files
set clouddir =  /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/realtime/OBSGEN/CLOUD_OBS #Final location of WDSS-II netCDF files ready to process

set yyyy = `echo ${event} | cut -c1-4`

#setenv radfileloc /work/rt_obs/radar_files #Location of ${event}_radars.csh file (contains list of radars for event)
setenv radfileloc /scratch4/NCEPDEV/fv3-cam/Hongli.Wang/WoFS/test/frdd-wofs-obs-radar_OSTI/wofs_radar/wdssii

echo 'starting' $event '\n'
echo "python getradaraws.py $event $radfileloc $l2dir_aws"
python getradaraws.py $event $radfileloc $l2dir_aws
echo 'done ' $event '\n'
exit 

rm ${l2dir_aws}/${event}/K*LIST.txt

if ( ! -d ${wdssdir} ) then
   mkdir -p ${wdssdir}
endif

echo "Running WDSSII to convert L2 data to MRMS format"
python runwdssii.py ${event} ${l2dir} ${wdssdir} ${wdssdir} K

sleep 2

if ( ! -d ${clouddir}/${event} ) then
   mkdir ${clouddir}/${event}
endif

if ( ! -d ${clouddir}/${eventd2} ) then
   mkdir ${clouddir}/${eventd2}
endif

if ( -d $clouddir/${event} ) then
   mkdir ${clouddir}/${event}
endif

if ( -d $clouddir/${event}/Radar ) then
   mkdir ${clouddir}/${event}/Radar 
endif

if ( -d $clouddir/${eventd2} ) then
   mkdir ${clouddir}/${eventd2}
endif

if ( -d $clouddir/${eventd2}/Radar ) then
   mkdir ${clouddir}/${eventd2}/Radar
endif

cd $wdssdir

set rad_sites = `ls -d K*`

echo $rad_sites

foreach rad ( $rad_sites ) 
        mkdir -p $clouddir/${event}/Radar/${rad}
        rsync -arq $wdssdir/${rad}/Velocity $clouddir/${event}/Radar/${rad}/
        rsync -arq $wdssdir/${rad}/ReflectivityQC $clouddir/${event}/Radar/${rad}/
        rm $clouddir/${event}/Radar/${rad}/Velocity/*/${eventd2}*.netcdf
        rm $clouddir/${event}/Radar/${rad}/ReflectivityQC/*/${eventd2}*.netcdf

        mkdir -p $clouddir/${eventd2}/Radar/${rad}
        rsync -arq $wdssdir/${rad}/Velocity $clouddir/${eventd2}/Radar/${rad}/
        rsync -arq $wdssdir/${rad}/ReflectivityQC $clouddir/${eventd2}/Radar/${rad}/
        rm $clouddir/${eventd2}/Radar/${rad}/Velocity/*/${event}*.netcdf
        rm $clouddir/${eventd2}/Radar/${rad}/ReflectivityQC/*/${event}*.netcdf
        
        sleep 1
end

end

exit(0)

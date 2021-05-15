#!/bin/bash

#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_WGS84.nc -src gadm36,FRA,0

#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie -list -bounds
#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie

python3 exec.py -i examples/params_LambertIIcarto.txt -o output/mask_France_LambertII.nc -src gadm36,FRA,0 -bounds
#python3 exec.py -i examples/params_LambertIIcarto.txt -o output/mask_France_LambertII.nc -src gadm36,FRA,0

#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,DNK,1,NAME_1=Occitanie --not-verbose -list




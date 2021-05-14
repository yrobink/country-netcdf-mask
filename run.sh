#!/bin/bash

#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_WGS84.nc -src gadm36,FRA,0 --not-verbose -list
python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie --not-verbose -list -bounds
#python3 exec.py -i examples/params_WGS84.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,DNK,1,NAME_1=Occitanie --not-verbose -list




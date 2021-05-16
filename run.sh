#!/bin/bash

## France, with lat/lon coordinates
#python3 exec.py -i examples/params_WGS84_FRA.txt -o output/mask_France_WGS84.nc -src gadm36,FRA,0

## Print list of regions, and bounds of Occitanie
#python3 exec.py -i examples/params_WGS84_FRA.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie -list -bounds

## Occitanie, in France, with lat/lon coordinates
#python3 exec.py -i examples/params_WGS84_FRA.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie

## France, in Lambert II carto, just print bounds
#python3 exec.py -i examples/params_LambertIIcarto_FRA.txt -o output/mask_France_LambertII.nc -src gadm36,FRA,0 -bounds

## France, in Lambert II carto
#python3 exec.py -i examples/params_LambertIIcarto_FRA.txt -o output/mask_France_LambertII.nc -src gadm36,FRA,0

## Italy, and Sicily in WGS84 coordinates
#python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_WGS84.nc -src gadm36,ITA,0 -bounds
#python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_WGS84.nc -src gadm36,ITA,0
#python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_Sicily_WGS84.nc -src gadm36,ITA,1,NAME_1=Sicily -list
#python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_Sicily_WGS84.nc -src gadm36,ITA,1,NAME_1=Sicily




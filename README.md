# country-netcdf-mask
Script and examples to build a netcdf mask of a country

## Description

## Dataset used

### GADM 3.6

This package use the GADM data to build the netcdf mask, available [here](https://gadm.org/data.html).

The GADM data use the ISO 3166-1 alpha-3 norm to describe countries, see [here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3).


## Requirement

Packages used:

- urllib
- zipfile
- numpy
- geopandas
- xarray
- shapely

Use your package manager or pip to install them.

## Usage


## Examples

### France with WGS84 projection

Run the command:

~~~bash
python3 exec.py -i examples/params_WGS84_FRA.txt -o output/mask_France_WGS84.nc -src gadm36,FRA,0
python3 exec.py -i examples/params_WGS84_FRA.txt -o output/mask_France_Occitanie_WGS84.nc -src gadm36,FRA,1,NAME_1=Occitanie
~~~

![Alt](/figures/France_WGS84.png)


### France with Lambert II projection

Run the command:

~~~bash
python3 exec.py -i examples/params_LambertIIcarto_FRA.txt -o output/mask_France_LambertII.nc -src gadm36,FRA,0
python3 exec.py -i examples/params_LambertIIcarto_FRA.txt -o output/mask_France_Occitanie_LambertII.nc -src gadm36,FRA,1,NAME_1=Occitanie
~~~

![Alt](/figures/France_LambertII.png)


### Italy with WGS84 projection

Run the command:

~~~bash
python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_WGS84.nc -src gadm36,ITA,0
python3 exec.py -i examples/params_WGS84_ITA.txt -o output/mask_Italy_Sicily_WGS84.nc -src gadm36,ITA,1,NAME_1=Sicily
~~~
![Alt](/figures/Italy_WGS84.png)



## Citation and acknowledgement

The script proposed here is based on the following [tutorial](https://www.wemcouncil.org/wp/wemc-tech-blog-3-calculating-eu-country-averages-with-era5-and-nuts/)


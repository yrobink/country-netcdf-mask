# country-netcdf-mask

This package is deprecated and not maintened, in favour of [shp2ncmask](https://github.com/yrobink/Shp2ncmask), which is more generic.


## Description

Script and examples to build a netcdf mask of a country

## Requirement

Packages used:

- urllib
- zipfile
- pathlib
- texttable
- datetime
- numpy
- pandas
- xarray
- geopandas
- shapely

Use your package manager or pip to install them.

## Usage

The generic command to use is:

~~~bash
python3 exec.py -i "gridfile_definition.txt" -o output.nc -src gadm36,country,level,subselect
~~~

Where:

- `-i`: the grid file, see the examples folder, the choice of the projection is fixed by the EPSG,
- `-o`: the netcdf output file,
- `-src`: the source, currently only GADM 3.6 is supported (see below)

Furthermore:

- `-list`: if `level > 0`, print a list of zone,
- `-bounds`: print the bounds in lat/lon coordinates, and in the projection defined by the EPSG in the grid file.


## Dataset used

### GADM 3.6

- This package use the GADM data to build the netcdf mask, available [here](https://gadm.org/data.html).
- The GADM data use the ISO 3166-1 alpha-3 norm to describe countries, see [here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3).

The arguments of `-src` options take the form `gadm36,country,level,subselect`, where:
- `country` is the ISO 3166-1 alpha-3 code,
- `level` is the "administrative" level, e.g. for France 0 is the country, 1 is the regions, 2 the departments, etc,
- `subselect` permits to select a particular element of a level. See examples below.


## Examples

In all figures below, the "False" values of the mask is represented by blue
zone, and the "True" values are replaced by the function $\sin(x^2+y^2)$.

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

